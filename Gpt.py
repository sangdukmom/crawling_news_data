import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# 크롤링 대상 사이트 리스트
URLS = [
    "https://www.gartner.com/en/newsroom",
    "https://www.techinsights.com/resources/blogs",
    "https://omdia.tech.informa.com/pr",
    "https://semi.org",
    "https://www.trendforce.com/presscenter",
    "https://digitimes.com.tw",
    "https://digitimes.com",
    "https://www.thelec.kr/",
    "https://www.reuters.com/",
    "https://www.bloomberg.com/asia",
    "https://biz.chosun.com/",
    "https://www.techdaily.co.kr/",
    "https://www.idc.com/resource-center/press-releases",
    "https://www.counterpointresearch.com/",
    "https://zdnet.co.kr/",
    "https://www.trendforce.com/presscenter",
    "https://semiengineering.com",
    "https://eetimes.com",
    "https://epnc.co.kr",
    "https://icsmart.cn/",
    "https://pc.watch.impress.co.jp",
    "https://9to5mac.com",
    "https://nikkei.com",
    "https://theverge.com",
    "https://thebell.co.kr",
    "https://donga.com",
    "https://mk.co.kr",
    "https://sankei.com",
    "https://laoyaoba.com",
    "https://yna.co.kr",
    "https://yomiuri.co.jp",
    "https://edaily.co.kr",
    "https://electronicsweekly.com",
    "https://etnews.com",
    "https://yicai.com",
    "https://joongang.co.kr",
    "https://fpdisplay.com",
    "https://hankyung.com",
    "https://imidex.org",
    "https://powerelectronicsnews.com",
    "https://powerelectronicsworld.net",
    "https://compoundsemiconductor.net"
]

# 키워드 리스트
KEYWORDS = [
    "DRAM", "NAND", "HBM", "TSMC", "SMIC", "Globalfoundries",
    "Automotive", "Electric Vehicle", "Smartphone", "PC", "Notebook", "Server", "AI Server",
    "Semiconductor", "Microsoft", "Google", "AWS", "Meta", "CoreWeave", "Nvidia", "openAI", "SiC"
]

# 데이터 저장 리스트
articles = []

def crawl_news(url):
    """특정 사이트에서 뉴스 타이틀과 URL을 가져오는 함수"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ {url} 접속 실패 (status: {response.status_code})")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 사이트마다 뉴스 리스트를 감싸는 태그가 다를 수 있음
        articles_on_page = soup.find_all("a")  # 일반적으로 기사 링크는 <a> 태그에 포함됨
        
        for article in articles_on_page:
            title = article.get_text(strip=True)
            link = article.get("href")

            # 키워드가 제목에 포함된 경우만 저장
            if link and any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                # 상대 경로 처리
                if link.startswith("/"):
                    link = url + link
                articles.append({"site": url, "title": title, "link": link})

    except Exception as e:
        print(f"❌ 오류 발생: {url} - {e}")

# 크롤링 실행
for url in URLS:
    print(f"🔍 {url}에서 뉴스 크롤링 중...")
    crawl_news(url)
    time.sleep(random.uniform(1, 3))  # 서버 부하 방지를 위해 랜덤 딜레이

# 데이터프레임 변환 및 저장
df = pd.DataFrame(articles)
df.to_csv("news_data.csv", index=False, encoding="utf-8-sig")
print("✅ 크롤링 완료! news_data.csv 저장됨")
