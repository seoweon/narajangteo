# 나라장터 입찰공고 크롤링 프로그램
[![N|Solid](http://www.g2b.go.kr/gov/koneps/pt/main/image/main/si_koneps_sub.png)](http://www.g2b.go.kr/index.jsp) 
(English version below)
나라장터에 올라오는 입찰공고를 모니터링하기 위해 개발된 간단한 프로그램으로, 검색어 리스트를 설정하면 그에 따라 최근 7일간 공고된 입찰공고 리스트를 가져와 엑셀파일로 정리해줍니다. 

본 프로젝트의 Inspiration이 된 포스트입니다: http://az001a.blog.me/220897788511, http://ifyourfriendishacker.tistory.com/2


# Korean e-procurement system (Narajangteo) crawling program

This is a simple program for scraping Korea's government bidding marketplace and returning an excel file with results of RFPs within 7 days, with selected key words. 

Inspired by: http://az001a.blog.me/220897788511, http://ifyourfriendishacker.tistory.com/2

## Prerequisites

If you don't have it already, please download Python (3.x recommended) from Anaconda (https://www.continuum.io/downloads). 
You will need Python (3.x)

Specific libraries: 
- pandas
- requests
- os
- datetime, time
- tqem
- (Beautifulsoup)
- (sys)
