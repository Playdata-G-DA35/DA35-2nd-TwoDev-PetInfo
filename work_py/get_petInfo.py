from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os

#working directory 변경
# c:\\classes\\project\\mini-project\\DA35-2nd-TwoDev-PetInfo\\work_py
os.chdir(r"c:\classes\project\mini-project\DA35-2nd-TwoDev-PetInfo\work_py")

driver_path = ChromeDriverManager().install()
print(type(driver_path))
print(driver_path) ## 여기에 크롬 드라이버가 있다

service = Service(executable_path=driver_path)
browser = webdriver.Chrome(service=service)#이것이 웹브라우저를 컨트롤 하므로 그냥 브라우져라고 생각해도 됨

#브라우저 뜰때까지 5초 대기
browser.implicitly_wait(5)

# 특정 url로 이동
dog_breeds_url = "https://www.akc.org/dog-breeds/{}"

popup_close_selector = "body > div.fancybox-overlay.fancybox-overlay-fixed > div > div > a"
breed_img_seletor = "body > div.cmw.bgc-white.page-single-breed > div:nth-child(2) > div > div.breed-page__sectional-wrapper > div.breed-page__sectional-standard-marking-wrapper > div.breed-page__section.breed-page__section--small.breed-page__standard.my4.bpm-my6 > div > div.breed-page__standard__image > img"
breed_info_selector = "body > div.cmw.bgc-white.page-single-breed > div:nth-child(2) > div > div.breed-page__about > div > div > div > div.breed-page__about__read-more__text__less"
# 파일에서 읽어온 견종을 dog_breeds_list에 담는다
data_path = r"..\work_csv\test_data.csv"
df = pd.read_csv(data_path)
dog_breeds_list = df['Breed']
urls = [dog_breeds_url.format(breed) for breed in dog_breeds_list]
img_src_list = []
breed_info_all = []
for idx, url in enumerate(urls, start=1):
    print(url)
    browser.get(url)
    browser.implicitly_wait(5)

    #pop up 닫기
    try:
        close_btn = browser.find_element(By.CSS_SELECTOR, popup_close_selector)
        if close_btn != None:
            close_btn.click()
    except:
        print("팝업 없음")

    # 견종 이미지 url 가져오기
    # df['img-src'] = urls
    
    breeds_image_ele = browser.find_element(By.CSS_SELECTOR, breed_img_seletor)
    if breeds_image_ele != None:
        img_src = breeds_image_ele.get_attribute("data-src")
        img_src_list.append(img_src)
        print(img_src)
        # 이미지 다운로드
        res = requests.get(img_src) #user-agent 없어도 됨
        split_file_name = img_src.split("/")[-1]
        if res.status_code == 200:
            file = res.content
            file_name = "..\work_img\{0}_{1}".format(idx, split_file_name)
            with open(file_name, "wb") as fo:
                fo.write(file)

    # 견종정보 가져오기
    breeds_info_ele = browser.find_elements(By.CSS_SELECTOR, breed_info_selector)
    # print("요소길이: ", len(breeds_image_ele))
    print("견종정보: ", breeds_info_ele[0])
    breed_info_list = ""
    for info in breeds_info_ele:
        print(info.text)
        breed_info_list += info.text
        
    breed_info_all.append(breed_info_list)
    time.sleep(4)

df['Img_src'] = img_src_list
df['Breed_info'] = breed_info_all
df.to_csv(r"..\work_csv\happy_puppy_info.csv", index=False)
browser.close()