# News_Sentimental_Analysis 
This is a Streamlit-based web application that fetches real-time news headlines using the NewsAPI, performs sentiment analysis using TextBlob, and presents the data through interactive visualizations such as sentiment distribution, word clouds, and emoji clouds.

**Ideal for understanding public sentiment around trending topics like politics, AI, finance, etc., over a specified time range.**


🔧 Features
🔍 Search real-time news by topic (e.g., "technology", "finance", "elections")

🗓️ Filter by date range (last 24 hours, 7 days, or 30 days)

📈 Sentiment analysis (positive, neutral, negative) using TextBlob

☁️ Word cloud of frequently used terms in headlines

😀 Emoji frequency cloud (if present in headlines)

📋 View and export full sentiment data as CSV

| Component    | Details                                      |
| ------------ | -------------------------------------------- |
| **Frontend** | [Streamlit](https://streamlit.io)            |
| **NLP**      | [TextBlob](https://textblob.readthedocs.io/) |
| **News API** | [NewsAPI.org](https://newsapi.org)           |
| **Visuals**  | Matplotlib, WordCloud, Emoji                 |
| **Language** | Python 3.x                                   |


🚀 How It Works
1. News Retrieval
The app fetches live news headlines and descriptions based on the user-entered topic using the NewsAPI.

2. Sentiment Classification
Each headline is analyzed using TextBlob to determine:

Polarity score (from -1 to +1)

Sentiment label: Positive / Negative / Neutral

3. Visualization
Bar chart showing distribution of sentiments

Word cloud showing most common words in news

Emoji frequency visualization (if present)

Expandable table to view all headlines and download CSV

🧪 Example Use Case
Search Keyword: "AI"

Output:

65% Positive

25% Neutral

10% Negative

Average polarity: 0.32

 Run It Locally
🔐 Prerequisite: Get a free NewsAPI key
Register at https://newsapi.org and get your API_KEY.

Installation
git clone https://github.com/chayanika/news-sentiment-tracker.git
cd news-sentiment-tracker
pip install -r requirements.txt

Add your NEWSAPI_KEY in the Python script:
NEWSAPI_KEY = "your_actual_key_here"
🚀 Launch the App
 streamlit run app.py
 
  news-sentiment-tracker
 ┣ 📜 app.py                  # Main Streamlit application
 ┣ 📜 requirements.txt        # All dependencies


