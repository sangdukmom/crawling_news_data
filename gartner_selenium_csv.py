import os
import re
import time
import json
import pandas as pd
import schedule

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# 파일명 설정 (중복 URL과 전체 결과 저장)
SEEN_FILE = "gartner_seen_urls.json"
RESULT_FILE = "gartner_news_results.json"

# 이미 저장된 URL 목록 불러오기
def load_seen_urls():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

# URL 목록 저장하기
def save_seen_urls(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=4)

# 기존 결과 불러오기
def load_results():
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 결과 저장하기 (JSON 형식)
def save_results(results):
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

# Gartner 검색 URL 템플릿 (뉴스룸 콘텐츠 필터 적용)
SEARCH_URL_TEMPLATE = ("https://www.gartner.com/en/search?filter1=Content%20type%7C"
                       "emt%3Apage%2Fcontent-type%2Fnewsroom&keywords={keyword}")

# 검색할 키워드 목록
keywords = [
    "Dram", "Nand", "Hbm", "Tsmc", "Smic", "Globalfoundries",
    "Automotive", "Electric vehicle", "Smartphone", "Pc", "Notebook",
    "Server", "Ai server", "Semiconductor", "Microsoft", "Google",
    "Aws", "Meta", "Coreweave", "Openai", "Sic"
]

# Selenium을 이용해 동적으로 렌더링된 페이지의 HTML을 반환하는 함수
def get_page_source(driver, url, wait_time=5):
    try:
        driver.get(url)
        time.sleep(wait_time)  # 동적 로딩 대기 (필요시 조절)
        return driver.page_source
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return ""

# 검색 결과 페이지(동적)에서 뉴스기사(제목, 링크) 추출
def parse_gartner_search(html, keyword):
    soup = BeautifulSoup(html, "html.parser")
    news_items = []
    # 검색 결과에서 모든 <a> 태그 중 href에 '/en/newsroom/'가 포함된 경우를 뉴스기사로 판단
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/"):
            href = "https://www.gartner.com" + href
        if re.search(r"/en/newsroom/", href):
            title = a.get_text(strip=True)
            if title and href:
                news_items.append({
                    "site": "Gartner",
                    "keyword": keyword,
                    "title": title,
                    "link": href
                })
    return news_items

# 기사 상세 페이지에서 본문 텍스트 추출 (우선 <article> 태그, 없으면 content/body 관련 div)
def get_article_detail(driver, url, wait_time=5):
    html = get_page_source(driver, url, wait_time)
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    # 우선 <article> 태그 내 텍스트 추출
    article_tag = soup.find("article")
    if article_tag:
        return article_tag.get_text(separator="\n", strip=True)
    # 없으면 "content"나 "body"가 포함된 div 중 가장 긴 텍스트 선택
    candidates = soup.find_all("div", class_=re.compile("(content|body)", re.I))
    if candidates:
        contents = [div.get_text(separator="\n", strip=True) for div in candidates]
        return max(contents, key=len)
    return ""

# 전체 크롤링 함수: 검색 페이지에서 뉴스기사 목록을 추출한 후, 각 기사 상세 페이지에서 본문 텍스트 수집
def crawl_gartner():
    seen = load_seen_urls()
    results = load_results()

    # Selenium 드라이버 옵션 설정 (headless 모드)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)  # ChromeDriver가 PATH에 있어야 함

    for keyword in keywords:
        search_url = SEARCH_URL_TEMPLATE.format(keyword=keyword)
        print(f"[Gartner] Searching for keyword '{keyword}' => {search_url}")
        search_html = get_page_source(driver, search_url, wait_time=5)
        items = parse_gartner_search(search_html, keyword)
        print(f"Found {len(items)} search items for keyword '{keyword}'")
        for item in items:
            if item["link"] in seen:
                continue  # 이미 수집된 기사 건너뛰기
            print(f"Processing article: {item['title']}")
            content = get_article_detail(driver, item["link"], wait_time=5)
            item["content"] = content
            results.append(item)
            seen.add(item["link"])
            # 상세 페이지 요청 후 딜레이
            time.sleep(1)
        # 검색 페이지 요청 간 딜레이
        time.sleep(1)

    driver.quit()
    save_seen_urls(seen)
    save_results(results)
    print(f"Crawling complete. Total unique articles: {len(results)}")

    # DataFrame으로 변환하여 CSV 파일로 저장 (UTF-8 BOM 포함)
    df = pd.DataFrame(results)
    df.to_csv("gartner_news_results.csv", index=False, encoding="utf-8-sig")
    print("CSV file 'gartner_news_results.csv' saved.")

# 주기적 크롤링 실행 (예: 6시간마다)
def run_scheduler():
    schedule.every(6).hours.do(crawl_gartner)
    print("Scheduler started: running crawl every 6 hours.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # 테스트: 한 번 실행
    crawl_gartner()
    # 실제 서비스 시, 아래 스케줄러 실행 (주석 해제)
    # run_scheduler()
