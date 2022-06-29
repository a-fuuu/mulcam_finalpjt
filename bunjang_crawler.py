import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from multiprocessing import Pool


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--disable-features=VizDisplayCompositor")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    return driver

def bunjang_crawler(page):
    lst = None
    driver = get_chrome_driver()
    driver.get(f'https://m.bunjang.co.kr/categories/600700001?page={page}&order=date')
    print(f'{page}번째 페이지 크롤링 중')
    for i in range(1,101):
        
        time.sleep(2)
        
        try:
            appo = driver.find_element(by=By.XPATH, value=f'//*[@id="root"]/div/div/div[4]/div/div[3]/div/div[{i}]/a/div[1]/div[1]/div[1]').text
        except:
            appo = False
        
        try:
            elapsed_time = driver.find_element(by=By.XPATH, value=f'//*[@id="root"]/div/div/div[4]/div/div[3]/div/div[{i}]/a/div[2]/div[2]/div[2]/span').text
        except:
            elapsed_time = '광고'
        
        driver.find_element(by=By.CSS_SELECTOR, value=f'#root > div > div > div:nth-child(4) > div > div.sc-erNlkL.fTqyaU > div > div:nth-child({i})').click()
        
        time.sleep(2)
        
        # 제목, 가격, 상품, 판매자 지역, 본문 등등...
        main_image = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[1]/div/div[1]/img[1]').get_attribute("src")
        image_count = len(driver.find_elements(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[1]/div/div[1]/img'))
        title = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[1]').text
        price = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]').text
        status = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[2]').text
        location = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]').text
        main_text = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[4]/div[1]/div[2]/div[1]/div[2]/div[2]').text
        store_info = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/div/a').text
        goods_count = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/a[1]').text
        follower = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[4]/div[1]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/a[2]').text
        crawl_time = time.strftime('%Y-%m-%d-%H:%M', time.localtime())
        
        df = pd.DataFrame(
            [[main_image, image_count ,title, store_info, price, status, location, main_text, appo, goods_count,elapsed_time, crawl_time, follower]], 
            columns = ['main_image', 'image_count', 'title', 'store_info','price', 'status', 'location', 'main_text','appo', 'goods_count','elapsed_time', 'crawl_time', 'follwer']
        )
        
        lst = pd.concat([lst, df])
        elapsed_time = None
        
        appo = None
        main_image = None
        image_count = None
        title = None
        price = None
        status = None
        location = None
        main_text = None
        store_info = None
        goods_count = None
        elapsed_time = None
        crawl_time = None
        driver.back()
        
    lst.to_csv(f'page{page}.csv')
    driver.close()
    print(f'{page}번째 페이지 크롤링 종료')

lost = [41,42,43,44,45,46,47,48,49,50,51,
        52,67,68,69,70,71,72,73,74,75,76,
        77,78,156,167,168,169,186,187,188,
        189,190,191,192,193,194,195,209,210,
        211,212,213,214,215,216,217,218,219,
        220,221,231,232,233,234,286,292,293,
        294,295,296,297,298,299]

if __name__ == '__main__':
    pool = Pool(processes=6)
    pool.map(bunjang_crawler, lost)