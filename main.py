from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib

binary = 'c:/chromedriver/chromedriver.exe'   # 크롬드라이버 파일경로 입력
browser = webdriver.Chrome(binary)   # 브라우저를 인스턴스화
# 크롤링할 페이지 주소 입력, 해당 주소로 크롬 열기
browser.get("https://news.joins.com/Search/JoongangNews?page=1&Keyword=%EB%94%A5%EB%9F%AC%EB%8B%9D&SortType=New&SearchCategoryType=JoongangNews")

# 페이지의 기사제목별 링크 수집
html = browser.page_source   # 해당 페이지의 html 가져오기
soup = bs(html, "html.parser")   #html을 bs로 파싱
href_list = []
for i in soup.find_all('h2',class_='headline mg'):   # html에서 태그와 클래스 이용해서 href 주소 가져오기
    for j in i.find_all('a'):
        href_list.append(j.get('href'))
        
# 각 기사별 댓글 수집
text = []
for i in href_list:
    browser.get(i)
    time.sleep(3)
    html = browser.page_source
    soup = bs(html, 'html.parser')
    for i in soup.find_all('p',class_='content'):
        text.append(i.text.strip())
        
print(text)
browser.quit()   # 브라우저 종료