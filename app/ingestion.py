import feedparser

# Dictionary of target feeds (Native Language Versions)
# We use native feeds so your AI has real work to do (translation) later.
NEWS_SOURCES = {
    # --- ORIGINAL (The East-West Core) ---
    "China_Xinhua": "http://www.xinhuanet.com/politics/news_politics.xml",
    "Russia_Kommersant": "https://www.kommersant.ru/RSS/news.xml",

    # --- MIDDLE EAST ---
    # WAFA: Palestine News & Info Agency (Official State News)
    "Palestine_WAFA": "https://www.wafa.ps/ar/rss.xml",
    # Iran: Mehr News (Semi-official, conservative analysis)
    "Iran_Mehr": "https://www.mehrnews.com/rss",

    # --- EUROPE ---
    # France: Le Monde (Center-left, intellectual record of record)
    "France_LeMonde": "https://www.lemonde.fr/rss/une.xml",
    # Poland: RMF24 (Major Polish news)
    "Poland_RMF24": "https://www.rmf24.pl/feed",
    # Germany: Tagesschau (ARD - National Public Broadcaster)
    "Germany_Tagesschau": "https://www.tagesschau.de/xml/rss2",

    # --- AMERICAS ---
    # Canada: CBC (National Public Broadcaster)
    "Canada_CBC": "https://www.cbc.ca/cmlink/rss-topstories",
    # Mexico: El Universal (Major influential daily)
    "Mexico_ElUniversal": "https://www.eluniversal.com.mx/rss/mundo.xml",
    # Brazil: Folha de S.Paulo (Largest circulation)
    "Brazil_Folha": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml",

    # --- ASIA ---
    # Japan: NHK (Japan Broadcasting Corp - National)
    "Japan_NHK": "https://www.nhk.or.jp/rss/news/cat0.xml",
    # India: Times of India (English - Largest circulation in India)
    "India_Times": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
}


def fetch_latest_news(limit=3):
    """
    Fetches the top 'limit' articles from each defined source.
    Returns a list of dictionaries containing title, link, and summary.
    """
    collected_articles = []

    print(f"📡 Contacting {len(NEWS_SOURCES)} Global RSS Feeds...")

    for source_name, url in NEWS_SOURCES.items():
        try:
            print(f"   - Scanning {source_name}...")
            feed = feedparser.parse(url)

            # Check if the feed actually worked
            if feed.bozo:
                print(
                    f"     ⚠️ Warning: Potential issue with {source_name} feed data.")

            # Loop through the first few entries
            for entry in feed.entries[:limit]:
                article = {
                    "source": source_name,
                    "title": entry.title,
                    "link": entry.link,
                    # Some feeds use 'summary', others 'description'. We try both.
                    "summary": entry.get('summary', entry.get('description', 'No summary available'))
                }
                collected_articles.append(article)

        except Exception as e:
            print(f"     ❌ Error fetching {source_name}: {e}")

    print(f"✅ Ingestion complete. Found {len(collected_articles)} articles.")
    return collected_articles
