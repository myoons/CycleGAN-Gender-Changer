from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

# 128 명의 여자 연예인들
woman_list = [
    '한지민',
    '신세경',
    '전지현',
    '문채원',
    '정은지',
    '윤아',
    '솔라',
    '미나',
    '장원영',
    '쯔위',
    '지수',
    '다현',
    '아린',
    '화사',
    '정채연',
    '최유정',
    '오하영',
    '조이',
    '이성경',
    '휘인',
    '조유리',
    '박초롱',
    '혜리',
    '보나',
    '박하선',
    '김민주',
    '최예나',
    '손나은',
    '세정',
    '윤보미',
    '이연희',
    '서은수',
    '강혜원',
    '혜정',
    '찬미',
    '정예인',
    '이영애',
    '크리스탈',
    '사나',
    '나연',
    '제니',
    '지효',
    '문별',
    '전소미',
    '채영',
    '초아',
    '정연',
    '주결경',
    '하니',
    '낸시',
    '예린',
    '연우',
    '케이',
    '선미',
    '은하',
    '로제',
    '설리',
    '백지현',
    '유지애',
    '리사',
    '조현',
    '신혜선',
    '한예슬',
    '공승연',
    '유리',
    '유라',
    '유아',
    '경리',
    '이미주',
    '성소',
    '루다',
    '서지수',
    '소진',
    '나나',
    '수애',
    '송지은',
    '여름',
    '페이',
    '송하영',
    '이채영',
    '박은혜',
    '송지효',
    '지호',
    '한효주',
    '희진',
    '김윤진',
    '박보영',
    '나라',
    '주은',
    '김민희',
    '설아',
    '나영',
    '소희',
    '한승연',
    '시연',
    '이새롬',
    '엑시',
    '솔빈',
    '이민정',
    '최지우',
    '성유리',
    '손예진',
    '설현',
    '김태희',
    '윤은혜',
    '유진',
    '슬기',
    '구혜선',
    '웬디',
    '전효성',
    '강민경',
    '이효리',
    '서현',
    '태연',
    '예은',
    '소희',
    '한가인',
    '고아라',
    '한혜진',
    '예리',
    '박신혜',
    '김유정',
    '서현진',
    '김태리',
    '송혜교',
    '아이유',
    '수지',
    '아이린'
    ]

count = 0

driver = webdriver.Chrome('C:/Users/grand/Desktop/ML/CycleGAN/data_utils/chromedriver.exe')
driver.get('https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl')


for woman in woman_list:

    try:
        elem = driver.find_element_by_name("q") # Get Search Bar
        elem.send_keys('{} 얼굴 사진'.format(woman)) # Type search words
        elem.send_keys(Keys.RETURN) # Press Enter

        time.sleep(3)
        
        try:   
            images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
        except:
            print('{} Find Error'.format(woman))
            continue

        if len(images) == 0 :
            print('{} No Images'.format(woman))
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
                    urllib.request.urlretrieve(imgUrl, 'C:/Users/grand/Desktop/ML/CycleGAN/data/woman/image_{}.jpg'.format(str(count)))
                    inner_count += 1
                    count += 1

                if inner_count == 25 :
                    break
            except:
                continue

        elem = driver.find_element_by_name("q")
        elem.clear()

    except:
        print('{} Passed'.format(woman))
        continue