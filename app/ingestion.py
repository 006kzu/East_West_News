import feedparser

# Dictionary of target feeds
NEWS_SOURCES = {
    "China_Xinhua": "http://www.xinhuanet.com/politics/news_politics.xml",  # Example Feed
    "Russia_Kommersant": "https://www.kommersant.ru/RSS/news.xml",
}


def fetch_headlines():
    raw_articles = []

    for source, url in NEWS_SOURCES.items():
        print(f"📡 Scanning {source}...")
        feed = feedparser.parse(url)

        # Grab the top 3 articles from each source
        for entry in feed.entries[:3]:
            raw_articles.append({
                "source": source,
                "title": entry.title,
                "link": entry.link,
                # RSS often has a short preview
                "summary": entry.get('summary', '')
            })

    return raw_articles
