from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, json, os, re, schedule

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

# Selenium으로 페이지 로딩 후 HTML 추출 함수
def get_page_source(url):
    options = Options()
    options.headless = True  # 백그라운드 실행
    # ChromeDriver 경로가 PATH에 있거나, 직접 지정해야 합니다.
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # 동적 콘텐츠 로딩을 위해 충분한 시간 대기 (사이트에 따라 조정)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    return html

# 동적 로딩된 Gartner 검색 결과에서 뉴스룸 기사 추출
def parse_gartner_dynamic(html, keyword):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    news_items = []
    # 예제에서는 href에 '/en/newsroom/'가 포함된 링크를 결과로 판단합니다.
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/"):
            href = "https://www.gartner.com" + href
        # 뉴스룸 관련 결과 판단 (필요시 정규식을 수정하세요)
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

# Selenium을 사용한 동적 크롤링 함수
def crawl_gartner_dynamic():
    seen = load_seen_urls()
    results = load_results()

    for keyword in keywords:
        url = SEARCH_URL_TEMPLATE.format(keyword=keyword)
        print(f"[Gartner] Searching for keyword '{keyword}' => {url}")
        try:
            html = get_page_source(url)
        except Exception as e:
            print(f"Error loading {url}: {e}")
            continue
        
        items = parse_gartner_dynamic(html, keyword)
        print(f"Found {len(items)} items for keyword '{keyword}'")
        for item in items:
            if item["link"] not in seen:
                results.append(item)
                seen.add(item["link"])
        time.sleep(1)  # 요청 사이 딜레이

    save_seen_urls(seen)
    save_results(results)
    print(f"Crawling complete. Total unique results: {len(results)}")

# 주기적으로 크롤링 실행 (예: 6시간마다)
def run_scheduler():
    schedule.every(6).hours.do(crawl_gartner_dynamic)
    print("Scheduler started: running crawl every 6 hours.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # 테스트: 한 번 실행해보기
    crawl_gartner_dynamic()
    # 실제 서비스 시 아래 줄의 주석을 해제하여 스케줄러 실행
    # run_scheduler()
