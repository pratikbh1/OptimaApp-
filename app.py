import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- THEME & STYLING ---
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

# --- 100g PRECISION DATABASE ---
FOOD_DB = {
    "Soya Chunks (Dry)": [345, 52.0, 33.0, 0.5, 13.0], # Precise Protein
    "Chicken Breast (Cooked)": [165, 31.0, 0.0, 3.6, 0.0],
    "Paneer": [265, 18.0, 2.6, 21.0, 0.0],
    "Boiled Egg": [155, 12.6, 1.1, 10.6, 0.0],
    "White Rice (Cooked)": [130, 2.7, 28.0, 0.3, 0.4],
    "Lentils (Dal)": [116, 9.0, 20.0, 0.4, 7.9],
    "Boiled Chana": [164, 15.0, 27.0, 2.6, 7.6],
    "Oats (Uncooked)": [389, 16.9, 66.0, 6.9, 10.0]
}

# --- CALCULATIONS ---
USER_WEIGHT = 75 
CAL_GOAL = 2400
current_consumed = 1240 # Placeholder for total logged

def get_burned_cals(steps):
    # Burn rate adjusted for weight
    return int(steps * (USER_WEIGHT / 70) * 0.045)

# --- HEADER: THE NET CALORIE RING ---
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
    # Net Calorie Visual Ring
    net_cals = current_consumed - burned
    remaining = CAL_GOAL - net_cals
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = net_cals,
        title = {'text': "Net Calories (Consumed - Burned)"},
        gauge = {
            'axis': {'range': [0, CAL_GOAL]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 1800], 'color': "#E8F5E9"},
                {'range': [1800, 2400], 'color': "#FFF9C4"}],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': CAL_GOAL}
        }
    ))
    fig.update_layout(height=350, margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# --- FUNCTIONAL TABS ---
tabs = st.tabs(["🍎 NUTRITION LOG", "🏋️ WORKOUT LAB", "📊 TRENDS"])

with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        food = st.selectbox("Search Food", list(FOOD_DB.keys()))
        grams = st.number_input("Weight (Grams)", min_value=1, value=100)
        r = grams / 100
        val = FOOD_DB[food]
        c, p, crb, fib = int(val[0]*r), round(val[1]*r,1), round(val[2]*r,1), round(val[4]*r,1)
        st.info(f"📊 {grams}g of {food}: **{c} kcal | {p}g Protein | {crb}g Carbs**")
        if st.button("LOG TO CLOUD"): st.success("Data Synced Successfully!")
    with f2:
        st.subheader("Daily Macros")
        st.progress(0.6)
        st.caption("Protein: 95g / 160g")
        st.progress(0.4)
        st.caption("Carbs: 120g / 300g")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="card"><h3>Gym Split: PPL Active</h3><p>Today is <strong>Push Day</strong></p></div>', unsafe_allow_html=True)
    st.button("Open Training Architecture")
