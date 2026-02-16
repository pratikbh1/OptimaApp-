import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 1. MEMORY SETUP ---
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []

# --- 2. THEME & STYLING ---
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

# --- 3. DATABASES ---
FOOD_DB = {"Soya Chunks (Dry)": [345, 52.0], "Chicken Breast": [165, 31.0], "Paneer": [265, 18.0], "Boiled Egg": [155, 12.6], "White Rice": [130, 2.7]}
EXERCISE_DB = {"Chest": ["Bench Press", "Cable Fly"], "Back": ["Lat Pulldown", "Rows"], "Legs": ["Squat", "Leg Press"], "Shoulders": ["Military Press"], "Arms": ["Bicep Curl"]}

# --- 4. DASHBOARD HEADER ---
st.title("⚡ Optima Elite Dashboard")
c1, c2, c3 = st.columns([1, 2, 1])

# Calculate Totals from Log
df_log = pd.DataFrame(st.session_state.activity_log) if st.session_state.activity_log else pd.DataFrame(columns=["Type", "Calories"])
consumed = df_log[df_log['Type'] == "Food"]['Calories'].sum()
burned_gym = abs(df_log[df_log['Type'] == "Workout"]['Calories'].sum())

with c3:
    input_steps = st.number_input("Sync Steps", value=8000, step=500)
    burned_steps = int(input_steps * (75 / 70) * 0.045)
    st.markdown(f'<div class="card">🚶 <strong>Steps Burned</strong><div class="metric-value">-{burned_steps}</div></div>', unsafe_allow_html=True)

with c1:
    st.markdown(f'<div class="card">🍎 <strong>Consumed</strong><div class="metric-value">{consumed}</div><small>kcal</small></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card">🔥 <strong>Gym Burn</strong><div class="metric-value">-{burned_gym}</div><small>kcal</small></div>', unsafe_allow_html=True)

with c2:
    net_cals = consumed - (burned_steps + burned_gym)
    fig = go.Figure(go.Indicator(mode="gauge+number", value=net_cals, title={'text': "Net Calories"}, gauge={'axis': {'range': [0, 2400]}, 'bar': {'color': "black"}}))
    fig.update_layout(height=300, margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# --- 5. TABS ---
tabs = st.tabs(["🍎 NUTRITION", "🏋️ WORKOUT", "📜 HISTORY", "🧬 SPLITS"])

with tabs[0]: # NUTRITION
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f_item = st.selectbox("Search Food", list(FOOD_DB.keys()))
    f_grams = st.number_input("Grams", min_value=1, value=100)
    if st.button("LOG FOOD"):
        cals = int(FOOD_DB[f_item][0] * (f_grams/100))
        st.session_state.activity_log.append({"Time": datetime.now().strftime("%H:%M"), "Type": "Food", "Details": f"{f_grams}g {f_item}", "Calories": cals})
        st.success(f"Logged {f_item}!")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]: # WORKOUT
    st.markdown('<div class="card">', unsafe_allow_html=True)
    w_muscle = st.selectbox("Muscle Group", list(EXERCISE_DB.keys()))
    w_ex = st.selectbox("Exercise", EXERCISE_DB[w_muscle])
    w_wgt = st.number_input("Weight (kg)", value=60.0)
    w_reps = st.number_input("Reps", value=10) # REPS ARE BACK
    if st.button("LOG SET"):
        burned = int((w_wgt * w_reps) * 0.01) # Volume-based burn estimate
        st.session_state.activity_log.append({"Time": datetime.now().strftime("%H:%M"), "Type": "Workout", "Details": f"{w_ex}: {w_wgt}kg x {w_reps}", "Calories": -burned})
        st.toast(f"Logged {w_ex}!")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # HISTORY
    if not df_log.empty:
        st.table(df_log)
        if st.button("Clear Today's Log"):
            st.session_state.activity_log = []
            st.rerun()
    else:
        st.info("Log your first meal or set to see history!")
