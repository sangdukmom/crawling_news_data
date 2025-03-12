from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 가트너 검색 URL
BASE_URL = "https://www.gartner.com/en/search?keywords="

# 검색할 키워드
KEYWORD = "TSMC"

# 데이터 저장 리스트
articles = []

def crawl_gartner_news(keyword):
    """Selenium을 사용하여 Gartner 검색 결과에서 키워드 뉴스 크롤링"""
    try:
        # Chrome 드라이버 설정 (백그라운드 실행 옵션 추가)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # 웹드라이버 실행
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 검색 결과 페이지 열기
        search_url = f"{BASE_URL}{keyword}"
        print(f"🔍 검색 페이지 접속: {search_url}")
        driver.get(search_url)

        # 페이지가 완전히 로드될 때까지 대기
        time.sleep(5)

        # 뉴스 리스트 가져오기
        news_list = driver.find_elements(By.CLASS_NAME, "search-results__item")

        print(f"🔍 '{keyword}' 검색 결과 개수: {len(news_list)}")

        for news in news_list:
            try:
                title_tag = news.find_element(By.CLASS_NAME, "search-results__title-link")
                title = title_tag.text.strip()
                link = title_tag.get_attribute("href")

                date_tag = news.find_element(By.CLASS_NAME, "search-results__date")
                date = date_tag.text.strip() if date_tag else "날짜 없음"

                articles.append({"keyword": keyword, "title": title, "link": link, "date": date})
                print(f"✅ 크롤링 성공: {title}")

            except Exception as e:
                print(f"❌ 개별 뉴스 크롤링 오류: {e}")

        # 드라이버 종료
        driver.quit()

    except Exception as e:
        print(f"❌ 크롤링 오류: {e}")

# 실행
crawl_gartner_news(KEYWORD)

# 데이터 저장
df = pd.DataFrame(articles)
df.to_csv("gartner_news.csv", index=False, encoding="utf-8-sig")
print("✅ 크롤링 완료! gartner_news.csv 저장됨")
