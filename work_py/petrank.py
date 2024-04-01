from bs4 import BeautifulSoup
import requests
import pandas as pd
# 1. url 분석(url, 요청파라미터,)
url = 'https://www.akc.org/expert-advice/news/most-popular-dog-breeds-2023/'

# user-agent 설정
## 검색 : 개발자도구 > 콘솔 : navigator.userAgent 실행.
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

## 요청 
res = requests.get(url, headers={'user-agent':user_agent})
html = res.text
## 응답 데이터 처리 
if res.status_code == 200:
    # 2. 내가 필요한 데이터를 어떻게 가져올지(css selector)
    ### BeautifulSoup을 이용해서 원하는 정보 조회 
    #### 녹색으로 표시된 이름들.
    soup = BeautifulSoup(html, 'lxml')
    breed_list = soup.select('#main-content > div.article-body > div.content-body > div > div > table > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2)')
    search_names = []
    for tag in breed_list: 
        # print(tag)
        search_names.append(tag.text)
else:
    print("실패:", res.status_code)

print(search_names)
    # 테스팅 해보고 200 뜨면, table 접근방식으로 해보자
    # 200 떠서 이름 가져왔음. html 테이블 방식 확인해서 pandas 로 csv 변환 가져오기


# reference code 

# if __name__ == "__main__": # 메인모듈이니 서브모듈이니.. import가 서브모듈 
#     result = get_daum_news_list()
#    
#    
#     from datetime import datetime
#     os.makedirs("daum_news_list",exist_ok=True)
#     # 저장할 파일명 - 특정 주기마다 크롤링 수행할 경우 실행 날짜/시간을 이용해서 만들어 준다. 
#     d = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
#     file_path = f"daum_news_list/{d}.csv" # 이런식으로 저장해야겠다
#     # dataframe 생성
#     result_df = pd.DataFrame(result,columns=["제목","링크주소"] )
#     # save as csvfile 
#     result_df.to_csv(file_path, index=False ) # file_path에 저장할거