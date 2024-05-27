from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import os

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")

# 한글 지역명과 영어 지역명 대응하는 딕셔너리 생성
korean_administrative_units_list = {
    "Seoul": {
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
    },
    "Busan": {
        "기장군": "Gijang-gun",
        "강서구": "Gangseo-gu",
        "금정구": "Geumjeong-gu",
        "남구": "Nam-gu",
        "동구": "Dong-gu",
        "동래구": "Dongnae-gu",
        "부산진구": "Busanjin-gu",
        "북구": "Buk-gu",
        "사상구": "Sasang-gu",
        "사하구": "Saha-gu",
        "서구": "Seo-gu",
        "수영구": "Suyeong-gu",
        "연제구": "Yeonje-gu",
        "영도구": "Yeongdo-gu",
        "중구": "Jung-gu",
        "해운대구": "Haeundae-gu"
    },
    "Daegu": {
        "대구달성군": " Dalseong-gun",
        "대구남구": " Nam-gu",
        "대구달서구": " Dalseo-gu",
        "대구동구": " Dong-gu",
        "대구북구": " Buk-gu",
        "대구서구": " Seo-gu",
        "대구수성구": " Suseong-gu",
        "대구중구": " Jung-gu"
    },
    "Incheon": {
        "인천강화군": "Ganghwa-gun",
        "인천옹진군": "Ongjin-gun",
        "인천계양구": "Gyeyang-gu",
        "인천남구": "Nam-gu",
        "인천남동구": "Namdong-gu",
        "인천동구": "Dong-gu",
        "인천부평구": "Bupyeong-gu",
        "인천서구": "Seo-gu",
        "인천연수구": "Yeonsu-gu",
        "인천중구": "Jung-gu"
    },
    "Gwangju": {
        "광주광산구": "Gwangsan-gu",
        "광주남구": "Nam-gu",
        "광주동구": "Dong-gu",
        "광주북구": "Buk-gu",
        "광주서구": "Seo-gu"
    },
    "Daejeon": {
        "대전대덕구": "Daedeok-gu",
        "대전동구": "Dong-gu",
        "대전서구": "Seo-gu",
        "대전유성구": "Yuseong-gu",
        "대전중구": "Jung-gu"
    },
    "Ulsan": {
        "울산울주군": "Ulju-gun",
        "울산남구": "Nam-gu",
        "울산동구": "Dong-gu",
        "울산북구": "Buk-gu",
        "울산중구": "Jung-gu"
    },
    "Sejong": {
        "세종시": "Sejong"
    },
    "Gyeonggi": {
        "경기도고양시": "Goyang-si",
        "경기도과천시": "Gwacheon-si",
        "경기도광명시": "Gwangmyeong-si",
        "경기도광주시": "Gwangju-si",
        "경기도구리시": "Guri-si",
        "경기도군포시": "Gunpo-si",
        "경기도김포시": "Gimpo-si",
        "경기도남양주시": "Namyangju-si",
        "경기도동두천시": "Dongducheon-si",
        "경기도부천시": "Bucheon-si",
        "경기도성남시": "Seongnam-si",
        "경기도수원시": "Suwon-si",
        "경기도시흥시": "Siheung-si",
        "경기도안산시": "Ansan-si",
        "경기도안성시": "Anseong-si",
        "경기도안양시": "Anyang-si",
        "경기도양주시": "Yangju-si",
        "경기도여주시": "Yeoju-si",
        "경기도오산시": "Osan-si",
        "경기도용인시": "Yongin-si",
        "경기도의왕시": "Uiwang-si",
        "경기도의정부시": "Uijeongbu-si",
        "경기도이천시": "Icheon-si",
        "경기도파주시": "Paju-si",
        "경기도평택시": "Pyeongtaek-si",
        "경기도포천시": "Pocheon-si",
        "경기도하남시": "Hanam-si",
        "경기도화성시": "Hwaseong-si",
        "경기도가평군": "Gapyeong-gun",
        "경기도양평군": "Yangpyeong-gun",
        "경기도연천군": "Yeoncheon-gun"
    },
    "Gangwon": {
        "강원도강릉시": "Gangneung-si",
        "강원도동해시": "Donghae-si",
        "강원도삼척시": "Samcheok-si",
        "강원도속초시": "Sokcho-si",
        "강원도원주시": "Wonju-si",
        "강원도춘천시": "Chuncheon-si",
        "강원도태백시": "Taebaek-si",
        "강원도고성군": "Goseong-gun",
        "강원도양구군": "Yanggu-gun",
        "강원도양양군": "Yangyang-gun",
        "강원도영월군": "Yeongwol-gun",
        "강원도인제군": "Inje-gun",
        "강원도정선군": "Jeongseon-gun",
        "강원도철원군": "Cheorwon-gun",
        "강원도평창군": "Pyeongchang-gun",
        "강원도홍천군": "Hongcheon-gun",
        "강원도화천군": "Hwacheon-gun",
        "강원도횡성군": "Hoengseong-gun"
    },
    "Chungcheongbuk": {
        "충청북도제천시": "Jecheon-si",
        "충청북도청주시": "Cheongju-si",
        "충청북도충주시": "Chungju-si",
        "충청북도괴산군": "Goesan-gun",
        "충청북도단양군": "Danyang-gun",
        "충청북도보은군": "Boeun-gun",
        "충청북도영동군": "Yeongdong-gun",
        "충청북도옥천군": "Okcheon-gun",
        "충청북도음성군": "Eumseong-gun",
        "충청북도증평군": "Jeungpyeong-gun",
        "충청북도진천군": "Jincheon-gun"
    },
    "Chungcheongnam": {
        "충청남도계룡시": "Gyeryong-si",
        "충청남도공주시": "Gongju-si",
        "충청남도논산시": "Nonsan-si",
        "충청남도당진시": "Dangjin-si",
        "충청남도보령시": "Boryeong-si",
        "충청남도서산시": "Seosan-si",
        "충청남도아산시": "Asan-si",
        "충청남도천안시": "Cheonan-si",
        "충청남도금산군": "Geumsan-gun",
        "충청남도부여군": "Buyeo-gun",
        "충청남도서천군": "Seocheon-gun",
        "충청남도예산군": "Yesan-gun",
        "충청남도청양군": "Cheongyang-gun",
        "충청남도태안군": "Taean-gun",
        "충청남도홍성군": "Hongseong-gun"
    },
    "Jeollabuk": {
        "전락북도군산시": "Gunsan-si",
        "전락북도김제시": "Gimje-si",
        "전락북도남원시": "Namwon-si",
        "전락북도익산시": "Iksan-si",
        "전락북도전주시": "Jeonju-si",
        "전락북도정읍시": "Jeongeup-si",
        "전락북도고창군": "Gochang-gun",
        "전락북도무주군": "Muju-gun",
        "전락북도부안군": "Buan-gun",
        "전락북도순창군": "Sunchang-gun",
        "전락북도완주군": "Wanju-gun",
        "전락북도임실군": "Imsil-gun",
        "전락북도장수군": "Jangsu-gun",
        "전락북도진안군": "Jinan-gun"
    },
    "Jeollanam": {
        "전라남도광양시": "Gwangyang-si",
        "전라남도나주시": "Naju-si",
        "전라남도목포시": "Mokpo-si",
        "전라남도순천시": "Suncheon-si",
        "전라남도여수시": "Yeosu-si",
        "전라남도강진군": "Gangjin-gun",
        "전라남도고흥군": "Goheung-gun",
        "전라남도곡성군": "Gokseong-gun",
        "전라남도구례군": "Gurye-gun",
        "전라남도담양군": "Damyang-gun",
        "전라남도무안군": "Muan-gun",
        "전라남도보성군": "Boseong-gun",
        "전라남도신안군": "Sinan-gun",
        "전라남도영광군": "Yeonggwang-gun",
        "전라남도영암군": "Yeongam-gun",
        "전라남도완도군": "Wando-gun",
        "전라남도장성군": "Jangseong-gun",
        "전라남도장흥군": "Jangheung-gun",
        "전라남도진도군": "Jindo-gun",
        "전라남도함평군": "Hampyeong-gun",
        "전라남도해남군": "Haenam-gun",
        "전라남도화순군": "Hwasun-gun"
    },
    "Gyeongsangbuk": {
        "경산북도경산시": "Gyeongsan-si",
        "경산북도경주시": "Gyeongju-si",
        "경산북도구미시": "Gumi-si",
        "경산북도김천시": "Gimcheon-si",
        "경산북도문경시": "Mungyeong-si",
        "경산북도상주시": "Sangju-si",
        "경산북도안동시": "Andong-si",
        "경산북도영주시": "Yeongju-si",
        "경산북도영천시": "Yeongcheon-si",
        "경산북도포항시": "Pohang-si",
        "경산북도고령군": "Goryeong-gun",
        "경산북도군위군": "Gunwi-gun",
        "경산북도봉화군": "Bonghwa-gun",
        "경산북도성주군": "Seongju-gun",
        "경산북도영덕군": "Yeongdeok-gun",
        "경산북도영양군": "Yeongyang-gun",
        "경산북도예천군": "Yecheon-gun",
        "경산북도울릉군": "Ulleung-gun",
        "경산북도울진군": "Uljin-gun",
        "경산북도의성군": "Uiseong-gun",
        "경산북도청도군": "Cheongdo-gun",
        "경산북도청송군": "Cheongsong-gun",
        "경산북도칠곡군": "Chilgok-gun"
    },
    "Gyeongsangnam": {
        "경상남도거제시": "Geoje-si",
        "경상남도김해시": "Gimhae-si",
        "경상남도밀양시": "Miryang-si",
        "경상남도사천시": "Sacheon-si",
        "경상남도양산시": "Yangsan-si",
        "경상남도진주시": "Jinju-si",
        "경상남도창원시": "Changwon-si",
        "경상남도통영시": "Tongyeong-si",
        "경상남도거창군": "Geochang-gun",
        "경상남도고성군": "Goseong-gun",
        "경상남도남해군": "Namhae-gun",
        "경상남도산청군": "Sancheong-gun",
        "경상남도의령군": "Uiryeong-gun",
        "경상남도창녕군": "Changnyeong-gun",
        "경상남도하동군": "Hadong-gun",
        "경상남도함안군": "Haman-gun",
        "경상남도함양군": "Hamyang-gun",
        "경상남도합천군": "Hapcheon-gun"
    },
    "Jeju": {
        "제주도제주시": "Jeju-si"
    }
}

# 현재 날짜로 된 폴더 생성
folder_path = os.path.join(os.getcwd(),"travelrank_list", current_date)
os.makedirs(folder_path, exist_ok=True)

# 웹드라이브 설치
service = ChromeService(executable_path=ChromeDriverManager().install())

for kaul in korean_administrative_units_list:
    def create_travelrank_list(data, parent_folder_name="."):
        folder_path = os.path.join(parent_folder_name, kaul)
        os.makedirs(folder_path, exist_ok=True)
    create_travelrank_list(kaul, folder_path)
    # 각 지역에 대한 정보를 가져와서 파일로 저장
    for region in korean_administrative_units_list[kaul]:
        # 영어 지역명 가져오기
        region_en = korean_administrative_units_list[kaul][region]

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

        filename = os.path.join(folder_path, kaul, f"chart_travel_{region_en}-{current_date}.json")

        # 데이터가 비어있지 않은 경우에만 JSON 파일로 저장
        if travel_data:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(travel_data, f, ensure_ascii=False, indent=4)
        # 브라우저 종료
        browser.quit()
