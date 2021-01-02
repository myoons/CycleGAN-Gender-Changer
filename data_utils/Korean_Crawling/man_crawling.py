from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

# 132 명의 남자 연예인들
man_list = [
    '장근석',
    '유아인',
    '유동근',
    '이서진',
    '송일국',
    '최재성',
    '장혁',
    '김민종',
    '지창욱',
    '주진모',
    '안성기',
    '이순재',
    '신영균',
    '이정재',
    '공유',
    '이영하',
    '권상우',
    '이승기',
    '김우빈',
    '최수종',
    '강석우',
    '차승원',
    '이민호',
    '차인표',
    '소지섭',
    '유승호',
    '박근형',
    '송중기',
    '송승헌',
    '고수',
    '현빈',
    '남궁원',
    '김수현',
    '강신성',
    '배용준',
    '강동원',
    '조인성',
    '정우성',
    '원빈',
    '장동건',
    '강다니엘',
    '지민',
    '백현',
    '뷔',
    '정국',
    '디오',
    '찬열',
    '진',
    '슈가',
    '카이',
    '수호',
    '세훈',
    '첸',
    '시우민',
    '제이홉',
    '레이',
    'RM ',
    '김우석',
    '박지훈',
    '옹성우',
    '닉쿤',
    '탑',
    '서강준',
    '김선호',
    '차은우',
    '김현중',
    '엘',
    '박형식',
    '임시완',
    '김재중',
    '최시원',
    '정용화',
    '황민현',
    '동해',
    '강인',
    '태민',
    '남태현',
    '우지',
    '예성',
    '지코',
    '정지훈',
    '양요섭',
    '온유',
    '은혁',
    '마크',
    '루카스',
    '태양',
    '박해진',
    '김범',
    '박유천',
    '김준수',
    '이준기',
    '헨리',
    '이홍기',
    '박보검',
    '준호',
    '김지석',
    '김강우',
    '이상엽',
    '박서준',
    '이선균',
    '정일우',
    '변요한',
    '이준',
    '지성',
    '최강창민',
    '유노윤호',
    '이동욱',
    '이지훈',
    '우도환',
    '김래원',
    '장기용',
    '남주혁',
    '박시후',
    '주지훈',
    '서인국',
    '윤계상',
    '유연석',
    '조승우',
    '정해인',
    '하석진',
    '이제훈',
    '규현',
    '윤두준',
    '키',
    '윤시윤',
    '신성록',
    '안재현',
    '옥택연',
    '하정우',
    '류준열',
    '조정석'
    ]

count = 0

driver = webdriver.Chrome('C:/Users/grand/Desktop/ML/CycleGAN/data_utils/chromedriver.exe')
driver.get('https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl')

for man in man_list:
    
    try:
        elem = driver.find_element_by_name("q") # Get Search Bar
        elem.send_keys('{} 얼굴 사진'.format(man)) # Type search words
        elem.send_keys(Keys.RETURN) # Press Enter

        time.sleep(3)

        try:   
            images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
        except:
            print('{} Passed'.format(man))
            continue

        if len(images) == 0 :
            print('{} No Images'.format(man))
            continue
        
        time.sleep(1)

        for image in images:
            
            inner_count = 0

            try:
                image.click()
                time.sleep(3)
                
                imgUrl = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img").get_attribute('src')

                if imgUrl[:4] != 'http':
                    continue
                else:
                    urllib.request.urlretrieve(imgUrl, 'C:/Users/grand/Desktop/ML/CycleGAN/data/man/image_{}.jpg'.format(str(count)))
                    inner_count += 1
                    count += 1

                if inner_count == 25 :
                    break
            except:
                continue
        
        elem = driver.find_element_by_name("q")
        elem.clear()

    except:
        print('{} Passed'.format(man))
        continue