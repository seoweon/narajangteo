# [나라장터](http://www.g2b.go.kr/index.jsp) 입찰공고 크롤링 프로그램
<br><br>
<sub>(English version below)</sub><br><br>
나라장터에 올라오는 입찰공고를 모니터링하기 위해 개발된 간단한 프로그램으로, 검색어 리스트를 설정하면 그에 따라 최근 7일간 공고된 입찰공고 리스트를 가져와 엑셀파일로 정리해줍니다. 크롤링 프로그램이지만, BeautifulSoup을 사용하지 않습니다. 

Credit: 본 프로젝트의 Inspiration이 된 포스트입니다: 
- http://az001a.blog.me/220897788511
- http://ifyourfriendishacker.tistory.com/2

#### 최근 업데이트 사항 | Latest updates
- [exclude.txt](https://github.com/seoweon/narajangteo/blob/master/exclude.txt) 파일을 추가하여 제외하고자 하는 키워드를 설정할 수 있습니다. (Added [exclude.txt](https://github.com/seoweon/narajangteo/blob/master/exclude.txt) so that you can define keywords that you would want to exclude from the results)
- command line print message를 추가하여 프로그램이 무엇을 하고 있는지 확인할 수 있습니다 (삭제되는 entry의 수 등) (Added command line print messages to monitor what's going on while the program is running (like how many entries are being deleted and such))

## 선행 프로그램
파이썬 (3.x) 을 구동하기 위해서 [Anaconda](https://www.continuum.io/downloads) 패키지 다운로드를 추천합니다. 파이썬 3.x 버전을 받아야 문제없이 작동됩니다. 

## 이 프로그램에 사용된 라이브러리
- [pandas](http://pandas.pydata.org/pandas-docs/stable/) 
- [requests](http://docs.python-requests.org/en/master/) 
- [os](https://docs.python.org/2/library/os.html) 
- [datetime](https://docs.python.org/2/library/datetime.html) 
- [time](https://docs.python.org/2/library/time.html) 
- [string](https://docs.python.org/2/library/string.html) 
- [tqdm](https://pypi.python.org/pypi/tqdm) (필수는 아니고, 기왕이면 다홍치마 :))
- (개발 예정) [sqlite3](https://docs.python.org/3/library/sqlite3.html) 

## 이용 방법
1. 다음 repository 를 클론합니다. 
2. [requirements 파일](https://github.com/seoweon/narajangteo/blob/master/requirements.txt)를 이용해 필요한 라이브러리를 설치합니다. (`pip install -r requirements.txt`)
3. 검색하고자 하는 검색어를 [카테고리 텍스트파일](https://github.com/seoweon/narajangteo/blob/master/category.txt)에 추가합니다. (검색어는 "/"로 구분하며, 스페이스나 행바꿈을 하지 않도록 합니다)
4. 특히 관심이 있는 기관이 따로 있다면 [기관 텍스트파일](https://github.com/seoweon/narajangteo/blob/master/orgs.txt)에 같은 방법으로 추가합니다. 순서도 관심도가 높은 순서로 넣어주면 그대로 정렬됩니다. 
5. command line을 열고 `python narajangteo_crawling.py` 명령을 넣어줍니다. 
6. 프로그램이 작동되고 결과물로 엑셀파일이 두 개 생성됩니다. 
	- 입력된 검색어에 따른 전체 리스트
	- 전체 리스트에서 관심 기관명을 따로 필터링해 기관명 순서대로 나열된 리스트

# Korean procurement system ([Narajangteo](http://www.g2b.go.kr/index.jsp)) crawling program
<br><br>
This is a simple program for scraping Korea's government bidding marketplace and returning an excel file with results of RFPs within 7 days, with selected key words. This does <b>not</b> use BeautifulSoup. 

Credit: This project was inspired by the following blog posts: 
- http://az001a.blog.me/220897788511
- http://ifyourfriendishacker.tistory.com/2

## Prerequisites

If you don't have it already, please download Python (3.x recommended) from [Anaconda](https://www.continuum.io/downloads). 
You will need Python (3.x)

## Specific libraries: 
- [pandas](http://pandas.pydata.org/pandas-docs/stable/) 
- [requests](http://docs.python-requests.org/en/master/) 
- [os](https://docs.python.org/2/library/os.html) 
- [datetime](https://docs.python.org/2/library/datetime.html) 
- [time](https://docs.python.org/2/library/time.html) 
- [string](https://docs.python.org/2/library/string.html) 
- [tqdm](https://pypi.python.org/pypi/tqdm) (just for the extra flair :))
- (planned for future) [sqlite3](https://docs.python.org/3/library/sqlite3.html) 

## How to use
1. Clone this repository.
2. Install all required libraries with the [requirements file](https://github.com/seoweon/narajangteo/blob/master/requirements.txt) `pip install -r requirements.txt`
3. Put keywords that you want to search for in the [category text file](https://github.com/seoweon/narajangteo/blob/master/category.txt). (each keyword is separated with "/" and avoid using spaces or line breaks after keywords)
4. If there are organizations that you are particularly interested in, you can add those names to the [org text file](https://github.com/seoweon/narajangteo/blob/master/orgs.txt) in the same way. The final list will be ordered to match the order of this list.  
5. Open your command line prompt and type `python narajangteo_crawling.py` 
6. Once the program runs, you will end up with two excel files in the same file location: 
	- The full list of results from search keywords
	- The filtered list of organizations of interest, ordered respectively

