from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime   
import json

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")

# 한글 지역명과 영어 지역명 대응하는 딕셔너리 생성
region_dict = {
   "seoul": {
        "강남구": "Gangnam-gu",
        "강동구": "Gangdong-gu",
        "강북구": "Gangbuk-gu",
        "강서구": "Gangseo-gu",
        "관악구": "Gwanak-gu",
        "광진구": "Gwangjin-gu",
        "구로구": "Guro-gu",
        "금천구": "Geumcheon-gu",
        "노원구": "Nowon-gu",
        "도봉구": "Dobong-gu",
        "동대문구": "Dongdaemun-gu",
        "동작구": "Dongjak-gu",
        "마포구": "Mapo-gu",
        "서대문구": "Seodaemun-gu",
        "서초구": "Seocho-gu",
        "성동구": "Seongdong-gu",
        "성북구": "Seongbuk-gu",
        "송파구": "Songpa-gu",
        "양천구": "Yangcheon-gu",
        "영등포구": "Yeongdeungpo-gu",
        "용산구": "Yongsan-gu",
        "은평구": "Eunpyeong-gu",
        "종로구": "Jongno-gu",
        "중구": "Jung-gu",
        "중랑구": "Jungnang-gu"
    }
}

# 웹드라이브 설치
service = ChromeService(executable_path=ChromeDriverManager().install())

# 각 지역에 대한 정보를 가져와서 파일로 저장
for region in region_dict:
    # 영어 지역명 가져오기
    region_en = region_dict[region]

    # 지역명을 URL에 포함하여 URL 생성
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={region}+여행"
    filename = f"chart_travel_{region_en}-{current_date}.json"

    # 웹드라이버 초기화
    options = ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(url)

    # 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "main_pack")))

    # 업데이트된 페이지 소스를 변수에 저장
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 데이터 추출
    travel_data = []
    travels_list = soup.select("#nxTsDo > div > div > div.do_content > div > div:nth-child(5) > div.ScrollBox-mso6a.Poi_filteredPoi-vqFVt.Poi_filteredPoi-HVLwu > div.information-iiK8v > ul > li.item-wJaHc")
    for travel in travels_list:
        ranking = travel.find('div', class_='rank-kEDoI').text.strip()
        title = travel.find('span', class_='name-K_anJ').text.strip()
        img_tag = travel.find('img', class_='img-q5u9H')['src']
        link_tag = travel.find('a', class_='anchor-X0MS6')['href']
        travel_data.append({
            'ranking': ranking,
            'title': title,
            'image_url': img_tag,
            'link': link_tag
        })
        
    # 데이터를 JSON 파일로 저장
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(travel_data, f, ensure_ascii=False, indent=4)
