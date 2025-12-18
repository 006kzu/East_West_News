# East-West News Analyst 🌍

A Python-based AI agent that bridges the information gap between Eastern and Western media. This tool ingests news from Chinese and Russian sources (via RSS), translates them, and uses an LLM to provide cultural context and "spin" analysis for English-speaking readers.

## 🚀 Features

- **Multi-Source Ingestion:** Fetches real-time headlines from sources like Xinhua and Kommersant.
- **Smart Translation:** Goes beyond literal translation to capture nuance.
- **Contextual Analysis:** Identifies potential bias, propaganda, or cultural references Westerners might miss.
- **Daily Briefing:** (Planned) Automates a daily summary report.

## 🛠️ Installation

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/YOUR_USERNAME/East_West_News.git](https://github.com/YOUR_USERNAME/East_West_News.git)
    cd East_West_News
    ```

2.  **Set up the Virtual Environment**

    ```bash
    python -m venv venv

    # Windows:
    venv\Scripts\activate

    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your keys:
    ```text
    OPENAI_API_KEY=your_key_here
    ```

## 🏃 Usage

Run the main agent script:

```bash
python main.py
```
