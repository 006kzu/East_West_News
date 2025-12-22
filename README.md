# Peripheral News 🧬

**Global Bio-Engineering Intelligence Dashboard**

Peripheral News is an open-source intelligence (OSINT) dashboard built with Python and Streamlit. It aggregates, filters, and visualizes high-impact developments in biomedical engineering and global biotech policy.

Unlike standard news aggregators, this system uses **Google Gemini (GenAI)** to read, score, and summarize technical papers and foreign news feeds before they ever reach the dashboard.

## 🚀 Features

- **Split-State "Command Center":** A unified home view that tracks two distinct intelligence streams:
  - **Global Intelligence:** Monitoring foreign policy and market shifts (via RSS feeds from sources like Xinhua & Kommersant).
  - **Academic Feed:** Tracking high-impact peer-reviewed literature (via Semantic Scholar).
- **AI-Powered Curator:**
  - **Scoring Engine:** Automatically rates academic papers (1-10) based on innovation and venue prestige.
  - **Summarizer:** Translates foreign headlines and simplifies complex abstracts into one-sentence "news hooks."
- **Secure Visualization:** Uses **Altair** for data visualization (Impact Rings) and native Streamlit components, ensuring zero dependency on unsafe HTML injection.
- **Persistent Memory:** All data is stored in a local SQLite database (`peripheral_news.db`), preventing data loss between sessions.

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Altair
- **Backend Logic:** Python (Feedparser, Requests)
- **AI Engine:** Google GenAI SDK (Gemini Flash)
- **Database:** SQLite3
- **Data Sources:** Semantic Scholar API, RSS Feeds

## 📦 Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/yourusername/peripheral-news.git](https://github.com/yourusername/peripheral-news.git)
    cd peripheral-news
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Secrets:**
    Create a `.env` file in the root directory and add your Google API key:
    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

## 🚦 Usage

This system consists of two parts: the **Ingestion Scripts** (which fetch data) and the **Dashboard** (which displays it).

### 1. Populate the Database

Run these scripts to fetch fresh content. You can run them manually or set them up as cron jobs.

- **Fetch Global News:**
  ```bash
  python run_news.py
  ```
- **Fetch & Score Academic Papers:**
  ```bash
  python run_academic.py
  ```

### 2. Launch the Dashboard

Once data is in the database, launch the UI:

```bash
streamlit run app.py
```
