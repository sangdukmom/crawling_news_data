import requests
from bs4 import BeautifulSoup
import json
import os
import time
import schedule
import re

# 저장 파일명 (중복 URL 및 결과)
SEEN_FILE = "gartner_seen_urls.json"
RESULT_FILE = "gartner_news_results.json"

# 이미 수집한 URL 목록 불러오기
def load_seen_urls():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

# 수집한 URL 목록 저장하기
def save_seen_urls(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=4)

# 저장된 결과 불러오기
def load_results():
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 결과 저장하기
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

# Gartner 검색페이지 HTML에서 뉴스룸 기사 링크 추출 (href에 '/en/newsroom/' 포함된 링크)
def parse_gartner(html, keyword):
    soup = BeautifulSoup(html, "html.parser")
    news_items = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # 상대경로라면 절대경로로 변환
        if href.startswith("/"):
            href = "https://www.gartner.com" + href
        # 뉴스룸 관련 기사로 판단 (URL에 '/en/newsroom/' 포함)
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

# Gartner 검색 결과를 크롤링하는 함수
def crawl_gartner():
    seen = load_seen_urls()
    results = load_results()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for keyword in keywords:
        url = SEARCH_URL_TEMPLATE.format(keyword=keyword)
        print(f"Searching Gartner for keyword '{keyword}' => {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue
        
        items = parse_gartner(response.text, keyword)
        print(f"Found {len(items)} items for keyword '{keyword}'")
        for item in items:
            if item["link"] not in seen:
                results.append(item)
                seen.add(item["link"])
        time.sleep(1)  # 요청 간 간격을 주어 서버 부담 완화

    save_seen_urls(seen)
    save_results(results)
    print(f"Crawling complete. Total unique results: {len(results)}")

# 주기적으로 크롤링 실행 (예: 6시간마다)
def run_scheduler():
    schedule.every(6).hours.do(crawl_gartner)
    print("Scheduler started: running crawl every 6 hours.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # 테스트 실행: 한 번 크롤링 수행
    crawl_gartner()
    # 실제 서비스 시 아래 주석 해제하여 스케줄러 실행
    # run_scheduler()
