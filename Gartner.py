import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 가트너 검색 URL
BASE_URL = "https://www.gartner.com/en/search?keyword="

# 검색할 키워드
KEYWORD = "TSMC"

# 데이터 저장 리스트
articles = []

def crawl_gartner_news(keyword):
    """Gartner에서 키워드 검색 결과를 크롤링하여 뉴스 제목, 링크, 날짜, 본문을 저장하는 함수"""
    try:
        # 키워드 검색 URL
        search_url = f"{BASE_URL}{keyword}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # 검색 결과 페이지 요청
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ {search_url} 접속 실패 (status: {response.status_code})")
            return

        # HTML 파싱
        soup = BeautifulSoup(response.text, "html.parser")

        # 뉴스 기사 리스트 찾기 (사이트 구조에 맞게 태그 수정 필요)
        news_list = soup.find_all("div", class_="search-results__item")  # 가트너 검색 결과 페이지의 뉴스 리스트 태그

        for news in news_list:
            try:
                title_tag = news.find("a", class_="search-results__title-link")
                title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
                link = title_tag["href"] if title_tag else None

                date_tag = news.find("span", class_="search-results__date")
                date = date_tag.get_text(strip=True) if date_tag else "날짜 없음"

                # 상세 본문 크롤링 (뉴스 링크로 접속)
                article_content = ""
                if link:
                    full_link = f"https://www.gartner.com{link}" if link.startswith("/") else link
                    article_response = requests.get(full_link, headers=headers, timeout=10)
                    if article_response.status_code == 200:
                        article_soup = BeautifulSoup(article_response.text, "html.parser")
                        content_tag = article_soup.find("div", class_="article-content")  # 본문 태그 (수정 필요할 수도 있음)
                        article_content = content_tag.get_text(strip=True) if content_tag else "본문 없음"

                # 기사 정보 저장
                articles.append({
                    "keyword": keyword,
                    "title": title,
                    "link": full_link,
                    "date": date,
                    "content": article_content
                })
                time.sleep(1)  # 크롤링 속도 조절

            except Exception as e:
                print(f"❌ 개별 뉴스 크롤링 오류: {e}")

    except Exception as e:
        print(f"❌ 크롤링 오류: {e}")

# 크롤링 실행
print(f"🔍 Gartner에서 '{KEYWORD}' 키워드 뉴스 크롤링 중...")
crawl_gartner_news(KEYWORD)

# 데이터프레임 변환 및 저장
df = pd.DataFrame(articles)
df.to_csv("gartner_news.csv", index=False, encoding="utf-8-sig")

print("✅ 크롤링 완료! gartner_news.csv 저장됨")
