
# coding: utf-8

# In[12]:

import pandas as pd
import requests
import os
import datetime, time
import string
from time import localtime, strftime
from datetime import timedelta
from tqdm import tqdm


# In[2]:

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
        cat_url = self.request_url(cat)
        df = pd.read_html(cat_url)[0]
        df['search_term']=cat
        return df
    
    def get_bidurl(self,bidnum):
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
        #add a slight delay betweeen scrapes: time.sleep(1)
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


# In[3]:

def txt_reader(name):
    with open(name+".txt",'rb') as f:
        line = f.readline()
        return line.decode('utf-8').split('/')


# In[4]:

#load the categories
category_list = txt_reader('category')

#scrape!
myscraper = KoreaPageScraper()

df = myscraper.scrape_categories(category_list)


# In[5]:

def clean_up(df):
    #Delete duplicates (more than two keywords together)
    df = df[~df.duplicated(['공고명'])].copy()
    #Divide the register date and due date
    df['register_date'],df['duedate'] = df['입력일시(입찰마감일시)'].str.split('(', 1).str
    df['duedate']=df['duedate'].str.replace(')','').replace('-','')
    df = df.drop('입력일시(입찰마감일시)',axis=1)
    df = df.sort_values(by='duedate',ascending=False)
    return df


# In[6]:

def filter_prioritize(df,filter_list,column):
    new_df = df[df[column].isin(filter_list)].copy()
    new_df[str(column+"_sorted")] = pd.Categorical(new_df[column],categories=filter_list,ordered=True)
    new_df = new_df.sort_values(column+"_sorted")
    return new_df


# In[7]:

def to_excel(df,subtitle):
    #Next step, format the excel file
    print("saving the "+subtitle+" list...")
    docname = "RMS-나라장터_입찰공고-"+subtitle+"-"+str(strftime("%y%m%d(%H%M%S)", localtime()))+".xlsx"
    writer = pd.ExcelWriter(docname)
    df.to_excel(writer,index=False,sheet_name='Sheet1')
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Set the column width and format.
    columns=['A:A','B:B','D:D','H:H','L:L','M:M']
    widths=[4,15,60,8,15,15]
    for c,w in zip(columns,widths):
        worksheet.set_column(c, w)

    #Formatting for putting in the header titles
    table_headers = [{'header':c} for c in  df.columns]
    #Getting the last column
    lastcol = list(string.ascii_uppercase)[len(df.columns)-1]

    worksheet.add_table('A1:%c%d'%(lastcol,len(df)+1),{'columns' : table_headers})
    writer.save()
    return


# In[8]:

clean_df = clean_up(df)


# In[9]:

#Get the target organization list
org_list = txt_reader('orgs')


# In[10]:

org_df = filter_prioritize(clean_df,org_list,'공고기관')


# In[15]:

to_excel(clean_df,'all')


# In[13]:

to_excel(org_df,'orgs')


# In[14]:

print ('All done! Please hit Enter to exit this command prompt. ')
input()


# In[ ]:



