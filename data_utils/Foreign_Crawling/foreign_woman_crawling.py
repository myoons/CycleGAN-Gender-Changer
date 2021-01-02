from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
    
driver = webdriver.Chrome('data_utils/chromedriver.exe')
driver.get('https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl')

elem = driver.find_element_by_name("q") # Get Search Bar
elem.send_keys('외국 여자 얼굴 사진') # Type search words
elem.send_keys(Keys.RETURN) # Press Enter

time.sleep(2)

SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    
    try:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height
    except:
        continue

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 0

for image_idx, image in enumerate(images):
    try: 
        image.click()
        time.sleep(3)    
        imgURL = driver.find_element_by_css_selector(".n3VNCb").get_attribute('src')
        urllib.request.urlretrieve(imgURL, 'data/foreign_woman/image_{}.jpg'.format(str(count)))
        count += 1
    except:
        pass


driver.close()