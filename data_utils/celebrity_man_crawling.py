from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

man_list = [
    '송중기',
    '지창욱',
    '이병헌',
    '장동건',
    '공유',
    '김수현',
    '마동석',
    '하정우',
    '이종석',
    '유아인',
    '이승기',
    '이민호',
    '소지섭',
    '조인성',
    '현빈',
    '조승우',
    '오지호',
    '이선균',
    '이서진',
    '최민식',
    '한석규',
    '송강호',
    '류승룡',
    '장근석',
    '최불암',
    '이종석',
    '장혁',
    '이정재',
    '권상우',
    '이승기',
    '박해진',
    '차승원',
    '차인표',
    '유승호',
    '송승헌',
    '강동원',
    '정우성',
    '원빈'
]

count = 292

for man in man_list:

    driver = webdriver.Chrome('data_utils/chromedriver.exe')
    driver.get('https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl')

    elem = driver.find_element_by_name("q") # Get Search Bar
    elem.send_keys('{} 얼굴 사진'.format(man)) # Type search words
    elem.send_keys(Keys.RETURN) # Press Enter

    time.sleep(2)

    try:   
        images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    except:
        continue

    if len(images) == 0 :
        continue
    
    for image_idx, image in enumerate(images):
        
        try:
            image.click()
            time.sleep(3)
            
            imgURL = driver.find_element_by_css_selector(".n3VNCb").get_attribute('src')
            urllib.request.urlretrieve(imgURL, 'data/celebrity_man/image_{}.jpg'.format(str(count)))
            
            count += 1
            if image_idx == 20 :
                break
        except:
            pass

    driver.close()