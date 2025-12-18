import time
from datetime import datetime
from app.ingestion import fetch_latest_news
from app.analysis import analyze_article


def main():
    print("--- East-West News Agent Starting ---")

    # 1. Generate a filename with today's date (e.g., briefing_2025-12-18.md)
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"briefing_{today}.md"

    # 2. Open the file in 'write' mode
    with open(filename, "w", encoding="utf-8") as f:
        # Write the Header
        f.write(f"# 🌍 Daily Foreign Intelligence Brief\n")
        f.write(f"**Date:** {today}\n\n")
        f.write("---\n\n")

        # Ingest
        raw_articles = fetch_latest_news(limit=3)
        print(f"\n🧠 Analyzing {len(raw_articles)} articles...\n")

        # Analyze & Write
        for i, article in enumerate(raw_articles):
            print(
                f"--- Processing {article['source']} ({i+1}/{len(raw_articles)}) ---")

            # Get the analysis from the Brain
            analysis = analyze_article(article)

            # Write to the file
            f.write(f"## {article['source']}\n")
            f.write(f"{analysis}\n\n")
            f.write(f"[Read Original Source]({article['link']})\n")
            f.write("---\n\n")

            print("✅ Added to report.")

            # Rate Limit Protection
            print("⏳ Cooling down for 4 seconds...")
            time.sleep(4)

    print(f"\n📄 Success! Briefing saved to: {filename}")


if __name__ == "__main__":
    main()
