import nltk
nltk.download('punkt')

import streamlit as st
import requests
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import emoji
import re

# --- API Key ---
NEWSAPI_KEY = "b62614c69e004467b980cd26d48bc04a"

# --- Function to Get News ---
def get_news(keyword, max_results=40, from_date=None):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keyword,
        "pageSize": max_results,
        "language": "en",
        "apiKey": NEWSAPI_KEY
    }
    if from_date:
        params["from"] = from_date
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "ok":
        articles = data["articles"]
        texts = [article["title"] + " " + str(article.get("description", "")) for article in articles]
        return texts
    else:
        st.error(f"NewsAPI Error: {data.get('message')}")
        return []

# --- Sentiment Analysis ---
def analyze_sentiment(texts):
    sentiment_data = []
    for text in texts:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        sentiment_data.append({"text": text, "sentiment": sentiment, "polarity": polarity})
    return pd.DataFrame(sentiment_data)

# --- Word Cloud Generator ---
def generate_wordcloud(texts):
    text_combined = " ".join(texts)
    wc = WordCloud(width=800, height=400, background_color='white').generate(text_combined)
    return wc

# --- Emoji Cloud ---
def extract_emojis(text):
    return ''.join(c for c in text if c in emoji.EMOJI_DATA)

def generate_emoji_cloud(texts):
    all_emojis = ''.join([extract_emojis(text) for text in texts])
    emoji_freq = {}
    for e in all_emojis:
        emoji_freq[e] = emoji_freq.get(e, 0) + 1
    return emoji_freq

# --- Streamlit App UI ---
st.set_page_config(page_title="🧠 Twitter Sentiment Tracker", layout="wide")
st.title("📰 Advanced Twitter Sentiment Tracker")

# --- User Inputs ---
with st.sidebar:
    st.header("🔍 Search Settings")
    keyword = st.text_input("Enter a topic (e.g. economy, politics, AI)", value="technology")
    date_range = st.selectbox("Date range", ["Past 24 hours", "Past week", "Past month"])
    refresh = st.button("🔄 Refresh Data")

# --- Date Filter ---
if date_range == "Past 24 hours":
    from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
elif date_range == "Past week":
    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
else:
    from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# --- Fetch & Analyze ---
if keyword:
    with st.spinner("Fetching news and analyzing..."):
        news_texts = get_news(keyword, from_date=from_date)
        df_sentiment = analyze_sentiment(news_texts)

    if not df_sentiment.empty:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.subheader("📊 Sentiment Distribution")
            st.bar_chart(df_sentiment["sentiment"].value_counts())

        with col2:
            st.subheader("📈 Sentiment Stats")
            st.metric("Average Polarity", f"{df_sentiment['polarity'].mean():.2f}")
            st.metric("Most Common", df_sentiment["sentiment"].mode()[0])
            st.metric("Total Articles", len(df_sentiment))

        # Word Cloud
        with st.expander("☁️ Word Cloud"):
            wc = generate_wordcloud(df_sentiment["text"])
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)

        # Emoji Cloud
        with st.expander("😄 Emoji Frequency"):
            emoji_freq = generate_emoji_cloud(df_sentiment["text"])
            if emoji_freq:
                sorted_emojis = sorted(emoji_freq.items(), key=lambda x: -x[1])
                top_emojis = ''.join(e * f for e, f in sorted_emojis[:10])
                st.markdown(f"<h1 style='font-size: 2em'>{top_emojis}</h1>", unsafe_allow_html=True)
            else:
                st.info("No emojis found in these headlines.")

        # Raw Data Table + Export
        with st.expander("📋 View All Headlines & Sentiments"):
            st.dataframe(df_sentiment[["sentiment", "polarity", "text"]])
            csv = df_sentiment.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, f"{keyword}_sentiment.csv", "text/csv")
    else:
        st.warning("No news found. Try a different keyword.")
