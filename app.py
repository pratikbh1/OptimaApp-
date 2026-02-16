import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZE MEMORY (SESSION STATE) ---
# This prevents the app from "forgetting" when it refreshes
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
FOOD_DB = {"Soya Chunks (Dry)": [345, 52.0], "Chicken Breast": [165, 31.0], "Paneer": [265, 18.0]}
EXERCISE_DB = {"Chest": ["Bench Press", "Cable Fly"], "Back": ["Lat Pulldown", "Rows"], "Legs": ["Squat", "Leg Press"]}

# --- 4. DASHBOARD ---
st.title("⚡ Optima Elite Dashboard")
tabs = st.tabs(["🏠 DASHBOARD", "🍎 NUTRITION", "🏋️ WORKOUT", "📜 HISTORY"])

with tabs[1]: # NUTRITION
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f_item = st.selectbox("Search Food", list(FOOD_DB.keys()))
    f_grams = st.number_input("Grams", min_value=1, value=100)
    if st.button("LOG FOOD"):
        # Calculate macros
        cals = int(FOOD_DB[f_item][0] * (f_grams/100))
        # Save to memory
        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Food",
            "Details": f"{f_grams}g {f_item}",
            "Calories": cals
        })
        st.success("Food Logged!")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # WORKOUT
    st.markdown('<div class="card">', unsafe_allow_html=True)
    w_muscle = st.selectbox("Muscle", list(EXERCISE_DB.keys()))
    w_ex = st.selectbox("Exercise", EXERCISE_DB[w_muscle])
    w_wgt = st.number_input("Weight (kg)", value=60)
    if st.button("LOG SET"):
        # Estimate calories (Simple MET estimate)
        burned = 50 
        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Workout",
            "Details": f"{w_ex} @ {w_wgt}kg",
            "Calories": -burned
        })
        st.toast("Set Logged!")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]: # THE NEW HISTORY TAB
    st.subheader("Your Daily Log")
    if st.session_state.activity_log:
        df = pd.DataFrame(st.session_state.activity_log)
        st.table(df) # Shows everything logged so far
        
        total_net = df['Calories'].sum()
        st.metric("Net Calorie Impact", f"{total_net} kcal")
    else:
        st.info("No logs for today yet. Start logging to see your history!")
