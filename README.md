Peripheral News 🧬
Global Bio-Engineering Intelligence Dashboard

Peripheral News is an open-source intelligence (OSINT) dashboard built with Python and Streamlit. It aggregates, filters, and visualizes high-impact developments in biomedical engineering, specifically focusing on the intersection of human biology and technology (BCI, Bionics, Medical Devices).

🆕 New Architecture (v2.0)
The application has been restructured to support a Split-State Navigation system. It now distinguishes between two primary data streams:

Global Intelligence: Policy, market movements, and geopolitical shifts in biotech.

Academic Feed: Hard science, peer-reviewed literature, and pre-prints.

Features
Split-Screen Home: A "Command Center" view that offers a side-by-side preview of both global news and academic papers, allowing users to choose their focus immediately.

Session-Based Navigation: Seamless state management allows users to switch contexts (e.g., from Home to the Academic Feed) via on-page buttons without losing their place.

Grid Layout: A modern, space-efficient 3-column grid system for browsing article cards.

"Soft" UI Design: Custom CSS injection overrides standard Streamlit styling to create a professional, rounded aesthetic (15px radius on all elements) using a specific color palette (British Racing Green, Teal, Platinum).

AI-Ready Parsing: Built-in regex helper functions to parse structured AI summaries (Headline vs. Body).

Installation
Clone the repository:

Bash

git clone https://github.com/yourusername/peripheral-news.git
cd peripheral-news
Create a virtual environment (Recommended):

Bash

python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
Install dependencies:

Bash

pip install streamlit
Usage
Run the dashboard locally:

Bash

streamlit run app.py
Navigation Guide
Home: The landing page. View top-level metrics and a preview of both feeds. Click "View Full Feed" in either column to enter that specific mode.

Sidebar: Use the radio menu to jump between views or filter data by date.

Article Cards: Click on any card in the grid to expand the summary. Click the "Source Link" to view the original external document.

Customization

1. Styling (CSS)
   All visual styling is contained in the st.markdown block at the top of app.py.

Primary Color (Headings): #004225 (British Racing Green)

Accent Color (Links/Borders): #008080 (Teal)

Backgrounds: #A3AABE (Purple-Grey for Sidebar/Headers)

2. Data Sources
   The app currently uses mock data functions (get_global_news() and get_academic_feed()). To connect your real backend:

Import your database connector in app.py.

Replace the mock lists with SQL queries or API calls.

Ensure your data dictionaries match the keys expected by the renderer: {'id', 'title', 'source', 'added_date', 'link'}.

File Structure
Plaintext

peripheral-news/
├── app.py # Main application entry point (UI & Logic)
├── README.md # Documentation
└── requirements.txt # Dependencies (streamlit)
License
MIT
