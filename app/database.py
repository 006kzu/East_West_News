import sqlite3
import datetime

DB_NAME = "peripheral_news.db"


def init_db():
    """Creates tables for BOTH Academic Papers and Global News."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. Academic Table (Existing)
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

    # 2. Global News Table (New)
    c.execute('''
        CREATE TABLE IF NOT EXISTS global_news (
            link TEXT PRIMARY KEY,
            source TEXT,       -- e.g., "Xinhua", "Kommersant"
            title TEXT,
            summary TEXT,      -- The AI translation/summary
            original_date TEXT,
            added_date TEXT,
            region TEXT        -- "East" (China/Russia)
        )
    ''')

    conn.commit()
    conn.close()

# ==========================
# 🎓 ACADEMIC FUNCTIONS
# ==========================


def paper_exists(paper_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM academic_papers WHERE paper_id = ?", (paper_id,))
    exists = c.fetchone() is not None
    conn.close()
    return exists


def save_paper(paper_data, review_data, field):
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
            paper_data.get('publicationDate', 'Unknown'),
            datetime.datetime.now().strftime("%Y-%m-%d")
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()


def get_feed(field):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT * FROM academic_papers 
        WHERE field = ? 
        ORDER BY published_date DESC 
        LIMIT 20
    ''', (field,))
    rows = c.fetchall()
    conn.close()
    return rows

# ==========================
# 🌍 GLOBAL NEWS FUNCTIONS
# ==========================


def news_exists(link):
    """Checks if we already processed this news link."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM global_news WHERE link = ?", (link,))
    exists = c.fetchone() is not None
    conn.close()
    return exists


def save_news(article_data, analysis_text):
    """Saves a translated/analyzed news article."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO global_news (link, source, title, summary, original_date, added_date, region)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            article_data['link'],
            article_data['source'],
            article_data['title'],
            analysis_text,  # The AI output
            # RSS feeds often lack clean dates, so we use today
            datetime.datetime.now().strftime("%Y-%m-%d"),
            datetime.datetime.now().strftime("%Y-%m-%d"),
            "East"  # Default region for now
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Skip duplicates silently
    finally:
        conn.close()


def get_global_news(limit=20):
    """Fetches the latest global news for the frontend."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM global_news ORDER BY added_date DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# In app/database.py


def get_news_stats():
    """Returns counts of articles in the DB."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Count total articles
    c.execute("SELECT COUNT(*) FROM global_news")
    total = c.fetchone()[0]
    # Count today's articles
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM global_news WHERE added_date = ?", (today,))
    today_count = c.fetchone()[0]
    conn.close()
    return total, today_count


def get_news_by_date(date_str, region=None):
    """Fetches news for a specific date, optionally filtered by region."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT * FROM global_news WHERE added_date = ?"
    params = [date_str]

    if region:
        # We assume 'source' contains the region keywords we saved earlier
        # Or we can filter loosely by source name for now
        if region == "Russia":
            query += " AND (source LIKE '%Kommersant%' OR region = 'Russia')"
        elif region == "China":
            query += " AND (source LIKE '%Xinhua%' OR region = 'China')"

    query += " ORDER BY original_date DESC"

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows
