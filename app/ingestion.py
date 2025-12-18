import feedparser

# Dictionary of target feeds (Native Language Versions)
# We use native feeds so your AI has real work to do (translation) later.
NEWS_SOURCES = {
    "China_Xinhua_Politics": "http://www.xinhuanet.com/politics/news_politics.xml",
    "Russia_Kommersant_Daily": "https://www.kommersant.ru/RSS/news.xml",
}


def fetch_latest_news(limit=3):
    """
    Fetches the top 'limit' articles from each defined source.
    Returns a list of dictionaries containing title, link, and summary.
    """
    collected_articles = []

    print("📡 Contacting RSS Feeds...")

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
