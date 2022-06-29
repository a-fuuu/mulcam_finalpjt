import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

###### 함수
# 링크 추출하는 함수 search_word에 검색어, page_start ~ page_end 범위의 페이지들의 게시글 링크를 추출하여 return.
# 기본적으로 페이지는 833 까지 설정한다.
def get_href(search_word, page_start, page_end):
    href = []
    for i in range(int(page_start),int(page_end) + 1):
        try:
            res = requests.get(f'https://www.daangn.com/search/{search_word}/more/flea_market?page={i}')
            soup = BeautifulSoup(res.text,'html.parser')
            link_lst = soup.select('a.flea-market-article-link')
            for j in link_lst:
                try:
                    href.append(j.attrs['href'])
                except:
                    pass
            time.sleep(1)
        except:
            print('에러 발생')
        
    return href


def daangn_crawler(href_list):
    df = None
    for h in href_list:
        time.sleep(0.5)
        try:
            res = requests.get(f'https://www.daangn.com{h}')
            soup = BeautifulSoup(res.text,'html.parser')

            code = int(h.split('/')[-1])
            title = soup.select_one('#article-title').text
            price = int(soup.select_one('#article-price').text.strip().replace(',','').replace('원','').replace('만',''))
            category = soup.select_one('#article-category').text.strip().replace('\n          \n           ','').split(' ∙ ')[0]
            elapsed_time = soup.select_one('#article-category').text.strip().replace('\n          \n           ','').split(' ∙ ')[1]
            crawl_time = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
            content = soup.select_one('#article-detail > p').text.replace('\n','')
            like = int(soup.select_one('#article-counts').text.split('∙')[0].strip().split(' ')[1])
            chat = int(soup.select_one('#article-counts').text.split('∙')[1].strip().split(' ')[1])
            view = int(soup.select_one('#article-counts').text.split('∙')[2].strip().split(' ')[1])
            lst = [code, title, price, category, crawl_time, elapsed_time, content, like, chat, view]
            df = pd.concat([df,pd.DataFrame([lst],
                                            columns = ['code' ,'title', 'price', 'category', 'crawl_time', 'elapsed_time', 'content', 'like', 'chat', 'view'])])
        except:
            pass
    return df


if __name__ == "__main__":
    search_word = input('검색할 기종은? ex) 아이폰 / 갤럭시 : ')
    page_start = input('검색할 페이지 시작 지점을 설정해주세요 ex) 1 ~ 833 : ')

    if int(page_start) > 833:
        page_start = input('검색할 페이지 시작 지점을 다시 설정해주세요 ex) 1 ~ 833 : ')

    
    page_end = input(f'검색할 페이지 종료 지점을 설정해주세요 {page_start}보다 커야합니다. ex) 1 ~ 833 : ')

    if int(page_end) < int(page_start):
        page_end = input(f'검색할 페이지 종료 지점을 다시 설정해주세요 {page_start}보다 커야합니다. ex) 1 ~ 833 : ')
    elif int(page_end) > 833:
        page_end = input(f'검색할 페이지 종료 지점을 설정해주세요 833보다 작아야합니다. ex) 1 ~ 833 : ')

    href_list = get_href(search_word, page_start, page_end)
    
    result = daangn_crawler(href_list)

    result.to_csv('result.csv')
    
    print('크롤링 완료')