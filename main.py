# EBS "명의" 시청자 게시판 댓글 크롤링
from bs4 import BeautifulSoup as bs
import urllib
import re

# 각 게시글의 링크주소를 추출
def ebs_bestdoctor_href(page):
    params1=[]
    for i in range(1,page+1):
        # 해당 사이트 주소 입력
        list_url = "https://bestdoctors.ebs.co.kr/bestdoctors/board/6/510093/list?c.page="+str(i)+"&fileClsCd=ANY&hmpMnuId=101&searchCondition=&searchConditionValue=0&searchKeywordValue=0&searchKeyword=&bbsId=510093&"
        url = urllib.request.Request(list_url)
        html = urllib.request.urlopen(url).read().decode("utf-8")
        soup = bs(html,'html.parser')
        params2 = []
        notice = 0
        for j in  soup.find_all('div',class_='txtcut'): #공지사항 7개 제외
            if notice >= 7:       
                for k in j.find_all('a'):
                    # 기본 주소에 각 링크 주소 패턴을 결합하여 최종 주소를 리스트에 추가
                    params2.append("https://bestdoctors.ebs.co.kr"+k.get("href"))
            notice += 1
        params1 += params2
    return params1

# 링크 주소의 게시글 내용을 파일로 저장
def ebs_bestdoctor_text(url_list):
    f = open("d:\\data\\ebs_bestdoctor.txt","w")
    cnt = 1   # 텍스트에 저장할 때 순번 부여
    for i in url_list:
        url = urllib.request.Request(i)
        html = urllib.request.urlopen(url).read().decode("utf8")
        soup = bs(html, "html.parser")
        for j in soup.find_all('div', class_ = "con_txt"):
            f.write(str(cnt)+": "+re.sub('[\xa0\n\t\r]', "", j.get_text(" ", strip=True))+'\n')
            cnt += 1   # 게시글 추가할 때마다 순번을 하나씩 올림
    f.close()
    
# 함수 실행
url_list = ebs_bestdoctor_href(1)   # 페이지수 입력
ebs_bestdoctor_text(url_list)