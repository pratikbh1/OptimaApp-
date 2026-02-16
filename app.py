import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="OPTIMA ELITE", layout="wide", page_icon="⚡")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8F9FB; }
    .card { background: white; padding: 24px; border-radius: 24px; box-shadow: 0 8px 30px rgba(0,0,0,0.04); border: 1px solid #F0F0F0; margin-bottom: 20px; text-align: center; }
    .metric-value { font-size: 30px; font-weight: 800; color: #111; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-weight: 700; width: 100%; background: #000; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE DATABASES ---
FOOD_DB = {
    "Soya Chunks (Dry)": [345, 52.0, 33.0, 0.5, 13.0], 
    "Chicken Breast (Cooked)": [165, 31.0, 0.0, 3.6, 0.0],
    "Paneer": [265, 18.0, 2.6, 21.0, 0.0],
    "Boiled Egg": [155, 12.6, 1.1, 10.6, 0.0],
    "White Rice (Cooked)": [130, 2.7, 28.0, 0.3, 0.4]
}

EXERCISE_DB = {
    "Chest": ["Bench Press", "Incline DB Press", "Cable Fly"],
    "Back": ["Lat Pulldown", "Seated Row", "Deadlift"],
    "Legs": ["Squat", "Leg Press", "Hamstring Curl"],
    "Shoulders": ["Military Press", "Lateral Raise", "Face Pulls"],
    "Arms": ["Bicep Curl", "Tricep Pushdown"]
}

# --- 3. DASHBOARD LOGIC ---
st.title("⚡ Optima Elite Dashboard")
m1, m2, m3 = st.columns(3)
with m1: st.markdown('<div class="card">🍎 Consumed<div class="metric-value">1240 kcal</div></div>', unsafe_allow_html=True)
with m2: st.markdown('<div class="card">🚶 Steps<div class="metric-value">8500</div></div>', unsafe_allow_html=True)
with m3: st.markdown('<div class="card">🔥 Streak<div class="metric-value">12 Days</div></div>', unsafe_allow_html=True)

# --- 4. THE INTERACTIVE TABS ---
tabs = st.tabs(["🍎 NUTRITION LOG", "🏋️ WORKOUT LAB", "🧬 SPLITS"])

with tabs[0]: # NUTRITION LOG
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f_item = st.selectbox("Search Food", list(FOOD_DB.keys()))
    f_grams = st.number_input("Grams", min_value=1, value=100)
    
    # Calculation Preview
    r = f_grams / 100
    cals = int(FOOD_DB[f_item][0] * r)
    prot = round(FOOD_DB[f_item][1] * r, 1)
    st.info(f"📊 Preview: {cals} kcal | {prot}g Protein")
    
    if st.button("LOG FOOD ITEM"):
        st.success(f"Successfully logged {f_grams}g of {f_item}!")
        st.balloons() # Visual reaction
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]: # WORKOUT LAB
    st.markdown('<div class="card">', unsafe_allow_html=True)
    w_muscle = st.selectbox("Select Muscle Group", list(EXERCISE_DB.keys()))
    w_ex = st.selectbox("Select Exercise", EXERCISE_DB[w_muscle])
    w_weight = st.number_input("Weight (kg)", value=40.0)
    w_reps = st.number_input("Reps", value=10)
    
    if st.button("LOG WORKOUT SET"):
        # This is the "Reaction" code that was missing!
        st.toast(f"Logged {w_ex}: {w_weight}kg x {w_reps}", icon="🏋️")
        st.success(f"Set saved for {w_ex}!")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # SPLITS
    st.markdown('<div class="card">🧬 Training Architecture Active</div>', unsafe_allow_html=True)
