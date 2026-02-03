import streamlit as st
import requests
from datetime import datetime
import time

# --- 1. Configuration & API Keys ---
# Store these in your Streamlit Secrets for deployment
WEATHER_KEY = st.secrets.get("WEATHER_KEY", "YOUR_OPENWEATHER_KEY")
NEWS_KEY = st.secrets.get("NEWS_KEY", "YOUR_NEWSAPI_KEY")
CITY = "Tripoli"

st.set_page_config(page_title="Vision Signage Hub", layout="wide")

# --- 2. Professional Signage CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;700&display=swap" rel="stylesheet">
    <style>
    header, footer, .stDeployButton {visibility:hidden !important;}
    * { font-family: 'Alexandria', sans-serif !important; }
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Signage Grid Tiles */
    .tile {
        background: #111111;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #222;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .accent { color: #0084ff; font-weight: 700; }
    .big-stat { font-size: 70px; font-weight: 700; line-height: 1; margin: 10px 0; }
    .headline-item { font-size: 18px; padding: 10px 0; border-bottom: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Data Extraction Functions ---
def fetch_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_KEY}&units=metric"
        data = requests.get(url).json()
        return f"{int(data['main']['temp'])}°", data['weather'][0]['description'].upper()
    except: return "--°", "CONNECTION ERROR"

def fetch_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=4&apiKey={NEWS_KEY}"
        data = requests.get(url).json()
        return [article['title'] for article in data['articles']]
    except: return ["Loading news headlines..."]

# --- 4. The Signage Display ---
# Main Header: Time and Date
now = datetime.now()
t_col1, t_col2 = st.columns([2, 1])
with t_col1:
    st.markdown(f"<div style='font-size: 100px; font-weight: 700; color: #0084ff;'>{now.strftime('%H:%M')}</div>", unsafe_allow_html=True)
with t_col2:
    st.markdown(f"<div style='font-size: 30px; margin-top: 40px; text-align: right;'>{now.strftime('%A')}<br>{now.strftime('%d %B %Y')}</div>", unsafe_allow_html=True)

st.write("---")

# Content Grid
col1, col2 = st.columns([1, 1.5])

with col1:
    # Weather Tile
    temp, desc = fetch_weather()
    st.markdown(f"""
        <div class="tile">
            <span class="accent">CURRENT WEATHER</span>
            <div class="big-stat">{temp}</div>
            <div style="font-size: 20px; color: #888;">{CITY.upper()} | {desc}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Optional Sports Placeholder
    st.markdown(f"""
        <div class="tile">
            <span class="accent">LIVE SCORES</span>
            <div style="font-size: 24px; margin-top: 15px;">Upcoming Match:</div>
            <div style="color: #888;">Live data feed connecting...</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # News Headlines Tile
    headlines = fetch_news()
    news_list = "".join([f"<div class='headline-item'>• {h}</div>" for h in headlines])
    st.markdown(f"""
        <div class="tile">
            <span class="accent">GLOBAL HEADLINES</span>
            <div style="margin-top: 10px;">{news_list}</div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. Automation Logic ---
# This ensures the screen updates automatically every 5 minutes
time.sleep(300)
st.rerun()