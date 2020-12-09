from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

import face_recognition

woman_list = [
    '김유정',
    '전소민',
    '김태희',
    '한채영',
    '이나영',
    '김현주',
    '김남주',
    '문근영',
    '박보영',
    '아이유',
    '신민아',
    '수애',
    '이민정',
    '김하늘',
    '한예슬',
    '하지원',
    '한지민',
    '고아라',
    '김성령',
    '문채원',
    '배수지',
    '심은하',
    '전지현',
    '고소영',
    '한가인',
    '김희애',
    '김혜수',
    '고현정',
    '손예진',
    '송혜교',
    '송지효',
    '이영애',
    '김희선'
]

count = 146

for man in woman_list:

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
            urllib.request.urlretrieve(imgURL, 'data/celebrity_woman/image_{}.jpg'.format(str(count)))
            
            count += 1
            if image_idx == 20 :
                break
        except:
            pass

    driver.close()