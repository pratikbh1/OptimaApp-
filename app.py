import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PREMIUM UI/UX STYLE ---
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

# --- 2. THE MASTER DATABASES (FOOD & EXERCISES) ---
FOOD_DB = {
    "Soya Chunks (Dry)": [345, 52.0, 33.0, 0.5, 13.0], 
    "Chicken Breast (Cooked)": [165, 31.0, 0.0, 3.6, 0.0],
    "Paneer": [265, 18.0, 2.6, 21.0, 0.0],
    "Boiled Egg": [155, 12.6, 1.1, 10.6, 0.0],
    "White Rice (Cooked)": [130, 2.7, 28.0, 0.3, 0.4],
    "Lentils (Dal)": [116, 9.0, 20.0, 0.4, 7.9],
    "Boiled Chana": [164, 15.0, 27.0, 2.6, 7.6],
    "Oats (Uncooked)": [389, 16.9, 66.0, 6.9, 10.0]
}

EXERCISE_DB = {
    "Chest": ["Bench Press", "Incline DB Press", "Cable Fly", "Dips"],
    "Back": ["Lat Pulldown", "Seated Row", "Deadlift", "Pullups"],
    "Legs": ["Squat", "Leg Press", "Hamstring Curl", "Calf Raise"],
    "Shoulders": ["Military Press", "Lateral Raise", "Face Pulls"],
    "Arms": ["Bicep Curl", "Hammer Curl", "Tricep Pushdown", "Skull Crushers"]
}

GYM_SPLITS = {
    "PPL (Push/Pull/Legs)": {"Push": "Chest/Shoulders/Triceps", "Pull": "Back/Biceps", "Legs": "Quads/Hams"},
    "Bro Split": {"Mon": "Chest", "Tue": "Back", "Wed": "Shoulders", "Thu": "Legs", "Fri": "Arms"},
    "Upper/Lower": {"Day 1": "Upper Body", "Day 2": "Lower Body", "Day 3": "Rest"}
}

# --- 3. LOGIC & DASHBOARD ---
USER_WEIGHT = 75 
CAL_GOAL = 2400
current_consumed = 1240 

def get_burned_cals(steps):
    return int(steps * (USER_WEIGHT / 70) * 0.045)

st.title("⚡ Optima Elite Dashboard")
c1, c2, c3 = st.columns([1, 2, 1])

with c3:
    st.write("##")
    input_steps = st.number_input("Sync Steps", value=8500, step=500)
    burned = get_burned_cals(input_steps)
    st.markdown(f'<div class="card">🚶 <strong>Steps Burned</strong><div class="metric-value">-{burned}</div><small>kcal</small></div>', unsafe_allow_html=True)

with c1:
    st.write("##")
    st.markdown(f'<div class="card">🍎 <strong>Consumed</strong><div class="metric-value">{current_consumed}</div><small>kcal</small></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card">🔥 <strong>Streak</strong><div class="metric-value">12 Days</div></div>', unsafe_allow_html=True)

with c2:
    net_cals = current_consumed - burned
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = net_cals,
        title = {'text': "Net Calories (Consumed - Burned)"},
        gauge = {'axis': {'range': [0, CAL_GOAL]}, 'bar': {'color': "black"}}
    ))
    fig.update_layout(height=350, margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# --- 4. TABS ---
tabs = st.tabs(["🍎 NUTRITION LOG", "🏋️ WORKOUT LAB", "🧬 TRAINING SPLITS"])

with tabs[0]: # NUTRITION
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        food = st.selectbox("Search Food", list(FOOD_DB.keys()))
        grams = st.number_input("Weight (Grams)", min_value=1, value=100)
        r = grams / 100
        val = FOOD_DB[food]
        c, p, crb, fib = int(val[0]*r), round(val[1]*r,1), round(val[2]*r,1), round(val[4]*r,1)
        st.info(f"📊 {grams}g: {c} kcal | P: {p}g | C: {crb}g | Fiber: {fib}g")
        st.button("LOG MEAL")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]: # WORKOUT LAB
    st.markdown('<div class="card">', unsafe_allow_html=True)
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        st.subheader("Log Your Set")
        muscle = st.selectbox("Select Muscle Group", list(EXERCISE_DB.keys()))
        ex = st.selectbox("Select Exercise", EXERCISE_DB[muscle])
        st.number_input("Weight (kg)", value=60.0)
        st.number_input("Reps", value=10)
        st.button("Log Workout Set")
    with w_col2:
        st.subheader("Volume Progress")
        st.line_chart([1000, 1200, 1100, 1500, 1400])
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # SPLITS
    st.markdown('<div class="card">', unsafe_allow_html=True)
    choice = st.selectbox("Select Your Active Split", list(GYM_SPLITS.keys()))
    details = GYM_SPLITS[choice]
    scols = st.columns(len(details))
    for i, (day, routine) in enumerate(details.items()):
        with scols[i]:
            st.markdown(f"**{day}**")
            st.caption(routine)
    st.markdown('</div>', unsafe_allow_html=True)
