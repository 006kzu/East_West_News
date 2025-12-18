import time  # <--- 1. Import this
from app.ingestion import fetch_latest_news
from app.analysis import analyze_article


def main():
    print("--- East-West News Agent Starting ---")

    # Step 1: Ingest
    raw_articles = fetch_latest_news(limit=2)  # Keep limit low for testing

    print(f"\n🧠 Analyzing {len(raw_articles)} articles...\n")

    # Step 2: Analyze
    for i, article in enumerate(raw_articles):
        print(
            f"--- Processing {article['source']} ({i+1}/{len(raw_articles)}) ---")

        analysis = analyze_article(article)
        print(analysis)
        print("\n" + "="*50 + "\n")

        # Step 3: Rate Limiting Pause
        print("⏳ Cooling down for 4 seconds to respect API limits...")
        time.sleep(4)


if __name__ == "__main__":
    main()
