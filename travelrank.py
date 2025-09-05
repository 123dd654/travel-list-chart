from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
import re

# 수집 시작일과 종료일 설정
START_DATE = datetime(2024, 9, 10)
END_DATE = datetime(2025, 9, 4)  # 종료일 포함

# 한글-영어 지역명 딕셔너리
korean_administrative_units_list = {
    "Seoul": {
        "서울강남구": "Gangnam-gu",
        "서울강동구": "Gangdong-gu",
        "서울강북구": "Gangbuk-gu",
        "서울강서구": "Gangseo-gu",
        "서울관악구": "Gwanak-gu",
        "서울광진구": "Gwangjin-gu",
        "서울구로구": "Guro-gu",
        "서울금천구": "Geumcheon-gu",
        "서울노원구": "Nowon-gu",
        "서울도봉구": "Dobong-gu",
        "서울동대문구": "Dongdaemun-gu",
        "서울동작구": "Dongjak-gu",
        "서울마포구": "Mapo-gu",
        "서울서대문구": "Seodaemun-gu",
        "서울서초구": "Seocho-gu",
        "서울성동구": "Seongdong-gu",
        "서울성북구": "Seongbuk-gu",
        "서울송파구": "Songpa-gu",
        "서울양천구": "Yangcheon-gu",
        "서울영등포구": "Yeongdeungpo-gu",
        "서울용산구": "Yongsan-gu",
        "서울은평구": "Eunpyeong-gu",
        "서울종로구": "Jongno-gu",
        "서울중구": "Jung-gu",
        "서울중랑구": "Jungnang-gu"
    },
    "Busan": {
        "부산기장군": "Gijang-gun",
        "부산강서구": "Gangseo-gu",
        "부산금정구": "Geumjeong-gu",
        "부산남구": "Nam-gu",
        "부산동구": "Dong-gu",
        "부산동래구": "Dongnae-gu",
        "부산부산진구": "Busanjin-gu",
        "부산북구": "Buk-gu",
        "부산사상구": "Sasang-gu",
        "부산사하구": "Saha-gu",
        "부산서구": "Seo-gu",
        "부산수영구": "Suyeong-gu",
        "부산연제구": "Yeonje-gu",
        "부산영도구": "Yeongdo-gu",
        "부산중구": "Jung-gu",
        "부산해운대구": "Haeundae-gu"
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


# 크롬 서비스와 옵션
service = ChromeService(ChromeDriverManager().install())
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 데이터 수집 함수
def collect_travel_data(target_date: datetime):
    date_str = target_date.strftime("%Y-%m-%d")
    base_folder_path = os.path.join(os.getcwd(), "travelrank_list", date_str)
    os.makedirs(base_folder_path, exist_ok=True)

    for city, districts in korean_administrative_units_list.items():
        city_folder_path = os.path.join(base_folder_path, city)
        os.makedirs(city_folder_path, exist_ok=True)

        for district_korean, district_english in districts.items():
            filename = os.path.join(city_folder_path, f"chart_travel_{district_english}-{date_str}.json")
            # 이미 수집한 파일은 건너뛰기
            if os.path.exists(filename):
                print(f"Already exists: {filename}, skipping...")
                continue

            url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={district_korean}+여행"
            browser = webdriver.Chrome(service=service, options=options)
            browser.get(url)

            # 페이지 로딩 대기
            WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "main_pack")))

            soup = BeautifulSoup(browser.page_source, 'html.parser')

            travel_data = []
            travels_list = soup.select("#nxTsDo > div > div > div.do_content > div > div:nth-child(5) > div.ScrollBox-mso6a.Poi_filteredPoi-vqFVt.Poi_filteredPoi-HVLwu > div.information-iiK8v > ul > li.item-wJaHc")
            for travel in travels_list:
                ranking = travel.find('div', class_='rank-kEDoI').text.strip()
                title = travel.find('span', class_='name-K_anJ').text.strip()
                img_tag = travel.find('img', class_='img-q5u9H')['src']
                link_tag = travel.find('a', class_='anchor-X0MS6')['href']
                place_id_match = re.search(r'place/(\d+)', link_tag)
                place_id = place_id_match.group(1) if place_id_match else ""

                travel_data.append({
                    'ranking': ranking,
                    'title': title,
                    'image_url': img_tag,
                    'link': place_id
                })

            # 상세 페이지
            for travel in travel_data:
                place_id = travel['link']
                if not place_id:
                    continue
                new_url = f"https://pcmap.place.naver.com/place/{place_id}/home"
                browser.get(new_url)
                WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.ID, "app-root")))
                detail_soup = BeautifulSoup(browser.page_source, 'html.parser')

                span_element = detail_soup.find('span', class_='lnJFt')
                title_cate = span_element.text.strip() if span_element else ""

                reviews = detail_soup.find_all('span', class_='PXMot')
                human_review = blog_review = ""
                for review in reviews:
                    a_tag = review.find('a')
                    if a_tag:
                        text = ''.join(a_tag.stripped_strings)
                        if '방문자리뷰' in text:
                            human_review = text.replace('방문자리뷰','').strip()
                        elif '블로그리뷰' in text:
                            blog_review = text.replace('블로그리뷰','').strip()

                addr_element = detail_soup.find('span', class_='LDgIH')
                addresses = addr_element.text.strip() if addr_element else ""

                travel.update({
                    'title_cate': title_cate,
                    'human_review': human_review,
                    'blog_review': blog_review,
                    'addresses': addresses
                })

            # JSON 저장
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(travel_data, f, ensure_ascii=False, indent=4)

            browser.quit()
            print(f"Saved: {filename}")

# 메인 실행
def main():
    next_date = START_DATE
    today = datetime.now()
    while next_date <= END_DATE and next_date <= today - timedelta(days=1):
        collect_travel_data(next_date)
        next_date += timedelta(days=1)

if __name__ == "__main__":
    main()
