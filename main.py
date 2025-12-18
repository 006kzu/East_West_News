# main.py
from app.ingestion import fetch_latest_news


def main():
    print("--- East-West News Agent Starting ---")

    # Step 1: Ingest
    raw_articles = fetch_latest_news()

    # Temporary: Print them out to prove it works
    # (Since we haven't built the translator yet, these will be in Chinese/Russian)
    print("\n--- RAW DATA PREVIEW ---")
    for article in raw_articles:
        print(f"[{article['source']}] {article['title']}")
        print(f"Link: {article['link']}\n")


if __name__ == "__main__":
    main()
