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

# ==========================
# 📊 DASHBOARD METRICS
# ==========================


def get_dashboard_stats(target_date):
    """
    Returns the counts needed for the top dashboard metrics.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. Global News Stats
    c.execute("SELECT COUNT(*) FROM global_news")
    global_total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM global_news WHERE added_date = ?",
              (target_date,))
    global_today = c.fetchone()[0]

    # 2. Academic Stats
    c.execute("SELECT COUNT(*) FROM academic_papers")
    academic_total = c.fetchone()[0]

    c.execute(
        "SELECT COUNT(*) FROM academic_papers WHERE added_date = ?", (target_date,))
    academic_today = c.fetchone()[0]

    conn.close()

    return {
        "global_total": global_total,
        "global_today": global_today,
        "academic_total": academic_total,
        "academic_today": academic_today
    }


def get_latest_academic_preview():
    """Fetches the single most recent academic paper for the dashboard card."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # Order by added_date so we see what the bot just found
    c.execute("SELECT * FROM academic_papers ORDER BY added_date DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row


def get_latest_news_preview():
    """Fetches the single most recent news article for the dashboard card."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM global_news ORDER BY added_date DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row


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


def get_feed(target=None, limit=50):
    """
    Fetches high-impact papers based on varying filter levels.
    target: Can be None (All), a list (Category), or a string (Specific Topic).
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    base_query = "SELECT * FROM academic_papers WHERE score >= 7"
    params = []

    if target is None or target == "All":
        # 1. FETCH EVERYTHING
        query = f"{base_query} ORDER BY published_date DESC LIMIT ?"
        params.append(limit)

    elif isinstance(target, list):
        # 2. FETCH CATEGORY (List of Topics)
        # Create a string like "?, ?, ?, ?" based on list length
        placeholders = ','.join('?' for _ in target)
        query = f"{base_query} AND field IN ({placeholders}) ORDER BY published_date DESC LIMIT ?"
        params.extend(target)
        params.append(limit)

    else:
        # 3. FETCH SPECIFIC TOPIC (String)
        query = f"{base_query} AND field = ? ORDER BY published_date DESC LIMIT ?"
        params.append(target)
        params.append(limit)

    c.execute(query, tuple(params))
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
