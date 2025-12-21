import sqlite3
import datetime

DB_NAME = "peripheral_news.db"


def init_db():
    """Creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # We make 'paper_id' the PRIMARY KEY.
    # This guarantees we can NEVER have duplicates.
    c.execute('''
        CREATE TABLE IF NOT EXISTS academic_papers (
            paper_id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT,
            field TEXT,
            score INTEGER,
            is_major BOOLEAN,
            summary TEXT,
            published_date TEXT,
            added_date TEXT
        )
    ''')
    conn.commit()
    conn.close()


def paper_exists(paper_id):
    """Checks if we already processed this paper."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM academic_papers WHERE paper_id = ?", (paper_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists


def save_paper(paper_data, review_data, field):
    """Saves a REVIEWED paper to the DB."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute('''
            INSERT INTO academic_papers 
            (paper_id, title, url, field, score, is_major, summary, published_date, added_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            paper_data['paperId'],
            paper_data['title'],
            paper_data['url'],
            field,
            review_data['score'],
            review_data['is_major'],
            review_data['layman_summary'],
            paper_data['publicationDate'],
            datetime.datetime.now().strftime("%Y-%m-%d")
        ))
        conn.commit()
        print(f"✅ Saved: {paper_data['title'][:30]}...")
    except sqlite3.IntegrityError:
        print(f"⚠️ Duplicate skipped: {paper_data['title'][:30]}...")
    finally:
        conn.close()


def get_feed(field):
    """Retrieves only the MAJOR papers for a specific field."""
    conn = sqlite3.connect(DB_NAME)
    # Return dictionary-like rows
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Only get papers marked as 'is_major' (True)
    c.execute('''
        SELECT * FROM academic_papers 
        WHERE field = ? AND is_major = 1 
        ORDER BY published_date DESC 
        LIMIT 20
    ''', (field,))

    rows = c.fetchall()
    conn.close()
    return rows
