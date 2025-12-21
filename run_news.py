import time
from app.ingestion import fetch_latest_news
from app.analysis import analyze_article
from app.database import init_db, news_exists, save_news


def update_news_feed():
    # 1. Ensure DB exists
    init_db()
    print("🌍 Starting Global News Sweep...")

    # 2. Fetch from RSS (The Eyes)
    # We fetch 5 from each source to start populating history
    raw_articles = fetch_latest_news(limit=5)

    new_count = 0
    for article in raw_articles:
        # 3. Check DB (Memory)
        if news_exists(article['link']):
            print(f"   ⏭️ Skipping known article: {article['title'][:20]}...")
            continue

        print(
            f"   📰 Analyzing: {article['source']} - {article['title'][:30]}...")

        # 4. Analyze (The Brain)
        try:
            analysis = analyze_article(article)

            # 5. Save (The Memory)
            save_news(article, analysis)
            new_count += 1
            print("      ✅ Saved to DB.")

            # Rate Limit Protection
            time.sleep(4)

        except Exception as e:
            print(f"      ❌ Failed: {e}")

    print(f"✅ Sweep Complete. Added {new_count} new global articles.")


if __name__ == "__main__":
    update_news_feed()
