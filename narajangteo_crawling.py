
# coding: utf-8

# # <center> 나라장터 입찰공고 크롤링 with Python3</center>
# 
# 나라장터에 올라오는 입찰공고를 모니터링하기 위해 개발된 간단한 프로그램으로, 검색어 리스트를 설정하면 그에 따라 최근 7일간 공고된 입찰공고 리스트를 가져와 엑셀파일로 정리해줍니다. 크롤링 프로그램이지만, BeautifulSoup을 사용하지 않습니다.

# In[18]:

import pandas as pd
import numpy as np
import requests
import os
import datetime, time
import string
from time import localtime, strftime
from datetime import timedelta
from tqdm import tqdm
from xlsxwriter.utility import xl_col_to_name, xl_range
from lxml import html


# In[6]:

class KoreaPageScraper(object):
    def __init__(self):
        pass
    
    def request_url(self,cat):
        '''returns url for a  category'''
        d = datetime.date.today()
        fromtd = d - timedelta(days=7)
        start_date = str(fromtd.strftime("%Y/%m/%d"))
        end_date =str(d.strftime("%Y/%m/%d"))
        fromBidDt = requests.utils.quote(start_date, safe='')
        toBidDt = requests.utils.quote(end_date, safe='')
        bidNm = requests.utils.quote(cat.encode('euc-kr'))
        url = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?taskClCds=&bidNm=" + bidNm + "&searchDtType=1&fromBidDt=" + fromBidDt + "&toBidDt=" + toBidDt + "&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&exceptEnd=Y&area=&regYn=Y&bidSearchType=1&searchType=1&recordCountPerPage=1000"
        return url

    def scrape_cat(self,cat):
        '''searches for each category'''
        cat_url = self.request_url(cat)
        df = pd.read_html(cat_url)[0]
        df['search_term']=cat
        return df
    
    def get_bidurl(self,bidnum):
        '''gets the bid url based on the bid registration number 
        (ones that do not have a proper bid registration number usually doesn't have a corresponding link and would ask the user to go to the organization website for more informatioin)'''
        num_split = str(bidnum).split(sep='-')
        bidno = num_split[0]
        if len(bidno) == 11:
            bidseq = num_split[-1]
            bidurl = "http://www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do?bidno="+bidno+"&bidseq="+bidseq
            return bidurl
        else: 
            return "Check organization website (공고기관) for details"
        bidseq = refnum_split[-1]
        bidurl = "http://www.g2b.go.kr:8081/ep/invitation/publish/bidInfoDtl.do?bidno="+bidno+"&bidseq="+bidseq
        return bidurl

    def scrape_categories(self, categories):
        '''scrapes each keyword and compiles it into a list. 
        There is a 1 second delay between each search term to prevent getting blocked out of the site'''
        appended_df = []
        for category in tqdm(categories):
            one_df = self.scrape_cat(category)
            appended_df.append(one_df)
            time.sleep(1)
        appended_df = pd.concat(appended_df, axis = 0)
        urlist=[]
        for index,row in appended_df.iterrows():
            urlist.append(self.get_bidurl(row['공고번호-차수']))
            
        appended_df['url']=urlist
        return appended_df


# In[7]:

#function to read txt files and parse the list
def txt_reader(name):
    with open(name+".txt",'rb') as f:
        line = f.readline()
        return line.decode('utf-8').split('/')


# In[8]:

#load the categories with the txt_reader function
category_list = txt_reader('category')
print("Getting the list of given keywords: " +str(category_list).replace('[','').replace(']','').replace("'",""))

#scrape with the "KoreaPageScraper" class
myscraper = KoreaPageScraper()

df = myscraper.scrape_categories(category_list)


# In[42]:

print(str(len(df))+" results have been found. ")


# In[11]:

#Load the excluding keywords
with open('exclude.txt','rb') as f:
    line = f.readline()
    contains_excluding = line.decode('utf-8').replace('/','|')


# In[40]:

print("Excluding the list of given keywords: "+str(txt_reader('exclude')).replace('[','').replace(']','').replace("'",""))


# In[43]:

#Deleting the excluding keywords and informing how many lines were deleted. 
og = len(df)
df = df[-df.공고명.str.contains(contains_excluding).fillna(True)]
print("Deleted "+str(og-len(df))+" entries with keywords to exclude. (Currently at "+str(len(df))+" entries)")


# In[53]:

def clean_up(df):
    #Delete duplicates (more than two keywords together)
    og2 = len(df)
    df = df[~df.duplicated(['공고명'])].copy()
    print(str(og2-len(df))+" duplicates were found and deleted (Currently at "+str(len(df))+" entries)")
    #Divide the register date and due date
    df['register_date'],df['duedate'] = df['입력일시(입찰마감일시)'].str.split('(', 1).str
    df['duedate']=df['duedate'].str.replace(')','').replace('-','')
    df = df.drop('입력일시(입찰마감일시)',axis=1)
    #Sort the values by duedate. To sort with a different value, change the following line's 'duedate' with the column name you desire to sort it by. 
    column_sort = 'duedate'
    df = df.sort_values(by=column_sort,ascending=False)
    print("Values are sorted by the column '"+column_sort+"'. To change this, please talk to the tool owner. ")
    return df


# In[45]:

def filter_prioritize(df,filter_list,column):
    new_df = df[df[column].isin(filter_list)].copy()
    new_df[str(column+"_sorted")] = pd.Categorical(new_df[column],categories=filter_list,ordered=True)
    new_df = new_df.sort_values(column+"_sorted")
    return new_df


# In[54]:

#Cleaning up the df to make more sense
clean_df = clean_up(df)


# In[55]:

#Get the target organization list
org_list = txt_reader('orgs')
print("Getting the entries from target organization list: "+str(org_list).replace('[','').replace(']','').replace("'",""))
org_df = filter_prioritize(clean_df,org_list,'공고기관')


# In[56]:

class create_excel(object):
    def get_length(self,column):
        ##
        ##This line is the problem!!
        ##
        valueex = column[~column.isnull()].reset_index(drop=True)[0]
        if type(valueex) == str:
            if valueex.startswith('=HYPERLINK'):
                return len('Click link')
            else: 
                len_list = list(column.dropna().apply(lambda x: len(str(x))))
                maxlen = max(len_list)
                medlen = np.median(len_list)
                meanlen = np.mean(len_list)
                diff = maxlen-medlen
                stdlen = np.std(len_list)
                #min(A,B+C*numchars)
                if maxlen < 10:
                    return maxlen+5
                elif diff > 50:
                    if medlen == 0:
                        return min(55,meanlen+5)
                    return medlen
                elif maxlen < 50:
                    return meanlen+15
                else:
                    return 50
        else:
            return 5

    def to_excel(self,df,name):
        #Next step, format the excel file
        print("saving the "+name+" list...")
        docname = "나라장터_입찰공고-"+name+"-"+str(strftime("%y%m%d(%H%M%S)", localtime()))+".xlsx"
        #make the destination directory, but guard against race condition
        if not os.path.exists(name):
            try:
                os.makedirs(name)
            except OSError as exc: 
                print(exc)
                raise Exception('something failed')
        writer = pd.ExcelWriter("%s/%s"%(name,docname), engine='xlsxwriter')
        df.to_excel(writer,index=False,sheet_name='Sheet1')
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        tablerange = xl_range(0,0,len(df),len(df.columns)-1)
        headerrange = xl_range(0,0,0,len(df.columns)-1)
        contentrange = xl_range(1,0,len(df),len(df.columns)-1)

        #Formatting headers
        header_format = workbook.add_format({'bg_color':'black'})
        column_format = workbook.add_format({'bottom':True,'bg_color':'white'})
        link_format = workbook.add_format({'font_color':'#157993','underline':True})
        
        # Set the column width and format.
        columns = []
        widths = []
        for i in range(0,len(df.columns)):
            a = xl_col_to_name(i)+":"+xl_col_to_name(i)
            columns.append(a)
            widths.append(self.get_length(df[df.columns[i]])) 
        
        for c,w in zip(columns,widths):
            worksheet.set_column(c, w)
        
        worksheet.conditional_format(contentrange,{'type':'no_errors',
                                                   'format':column_format})
        worksheet.conditional_format(headerrange,{'type':'no_errors',
                                                  'format':header_format})
        worksheet.conditional_format(tablerange,{'type':'text',
                                                 'criteria':'containing',
                                                 'value':'Click link',
                                                 'format':link_format})
           
        #Formatting for putting in the header titles
        table_headers = [{'header':c} for c in  df.columns]
        #Create a table with the data
        worksheet.add_table(tablerange,{'columns' : table_headers})         
        
        writer.save()
        return


# In[57]:

go_to_excel = create_excel()


# In[58]:

go_to_excel.to_excel(clean_df,'full')


# In[59]:

go_to_excel.to_excel(org_df,'orgs')


# In[60]:

print ('All done! Please hit Enter to exit this command prompt. ')
input()


# In[ ]:



