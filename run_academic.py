import time
from app.academic import fetch_latest_papers, evaluate_paper
from app.database import init_db, paper_exists, save_paper
from app.topics import ALL_TOPICS


def update_feeds():
    init_db()
    print(f"🚀 Starting Massive Academic Sweep ({len(ALL_TOPICS)} topics)...")

    for i, topic in enumerate(ALL_TOPICS):
        print(f"\n[{i+1}/{len(ALL_TOPICS)}] 🔎 Scouting Topic: {topic}...")

        # Fetch papers
        raw_papers = fetch_latest_papers(topic=topic, limit=5)

        if not raw_papers:
            print(f"   ⚠️ No papers found. Skipping...")
            continue

        new_count = 0
        for paper in raw_papers:
            if paper_exists(paper['paperId']):
                continue

            # --- THE REQUESTED CHANGE ---
            pub_date = paper.get('publicationDate') or "Unknown Date"
            print(f"   🧪 Reviewing: {paper['title'][:40]}... ({pub_date})")
            # -----------------------------

            review = evaluate_paper(paper)

            if review:
                save_paper(paper, review, topic)
                new_count += 1

            # If in DEV_MODE, we don't need to sleep much because we aren't calling Gemini!
            time.sleep(0.1)

        print(f"   ✅ Added {new_count} new papers for {topic}.")
        print("   🚚 Moving to next topic...")
        time.sleep(5)  # Still sleep here for Semantic Scholar


if __name__ == "__main__":
    update_feeds()
