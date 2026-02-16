import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. PREMIUM UI/UX STYLE (STAYS EXACTLY THE SAME) ---
st.set_page_config(page_title="OPTIMA ELITE", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8F9FB; }
    
    .card {
        background: white; padding: 24px; border-radius: 24px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04);
        border: 1px solid #F0F0F0; margin-bottom: 20px;
    }
    .metric-title { font-size: 13px; font-weight: 700; color: #8C8C8C; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 28px; font-weight: 800; color: #1A1A1A; margin: 4px 0; }
    
    .stButton>button { border-radius: 12px; height: 3.5em; font-weight: 700; transition: 0.3s; width: 100%; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 45px; border-radius: 10px; background: #EEE; border: none; }
    .stTabs [aria-selected="true"] { background: #000 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE MASTER DATABASES (GRAMS + SPLITS) ---
FOOD_DATA = {
    "White Rice": [130, 2.7, 28, 0.3],
    "Lentils (Dal)": [116, 9.0, 20, 0.4],
    "Chicken Breast": [165, 31.0, 0, 3.6],
    "Paneer": [265, 18.0, 3, 20.0],
    "Boiled Egg": [155, 13.0, 1.1, 11.0]
}

GYM_SPLITS = {
    "PPL (Push/Pull/Legs)": {
        "Push": "Chest, Shoulders, Triceps",
        "Pull": "Back, Biceps, Rear Delts",
        "Legs": "Quads, Hams, Calves"
    },
    "Bro Split (Classic)": {
        "Mon": "Chest", "Tue": "Back", "Wed": "Shoulders", "Thu": "Legs", "Fri": "Arms"
    },
    "Upper / Lower": {
        "Upper A": "Push/Pull Focus", "Lower A": "Squat Focus", "Upper B": "Vertical Focus", "Lower B": "Hinge Focus"
    }
}

# --- 3. DASHBOARD METRICS ---
st.title("⚡ Optima Elite")
st.caption("Complete Feature-Integrated Dashboard")

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown('<div class="card"><div class="metric-title">Calories</div><div class="metric-value">1,240</div></div>', unsafe_allow_html=True)
with m2: st.markdown('<div class="card"><div class="metric-title">Protein</div><div class="metric-value">95g</div></div>', unsafe_allow_html=True)
with m3: st.markdown('<div class="card"><div class="metric-title">Workout Day</div><div class="metric-value">Push A</div></div>', unsafe_allow_html=True)
with m4: st.markdown('<div class="card"><div class="metric-title">Streak</div><div class="metric-value">🔥 12</div></div>', unsafe_allow_html=True)

# --- 4. NAVIGATION TABS (ALL FEATURES IN ONE PLACE) ---
tabs = st.tabs(["🏠 DASHBOARD", "🍎 NUTRITION (GRAMS)", "🏋️ WORKOUT LOG", "🧬 TRAINING SPLITS"])

with tabs[0]: # HOME DASHBOARD
    st.write("##")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        df_w = pd.DataFrame({'Date': pd.date_range(start='2026-02-01', periods=10), 'Weight': [75, 74.8, 74.5, 74.2, 74.6, 74.1, 73.8, 73.5, 73.2, 73.0]})
        fig = px.area(df_w, x='Date', y='Weight', title="Weight Progress", color_discrete_sequence=['#000000'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_r:
        st.markdown('<div class="card" style="height: 100%;"><h3>Daily Targets</h3>'
                    '💧 2.5L / 4L Water<br>🚶 8,421 Steps<br>🍗 Protein: 65g left'
                    '<br><br><strong>Badges:</strong><br>🏆 Iron Warrior<br>🥇 Early Bird</div>', unsafe_allow_html=True)

with tabs[1]: # FOOD LOG (BY GRAMS)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        st.subheader("Log by Grams")
        meal = st.radio("Section", ["Breakfast", "Lunch", "Dinner", "Snacks"], horizontal=True)
        item = st.selectbox("Search Food", list(FOOD_DATA.keys()))
        weight = st.number_input("Weight (Grams)", min_value=1, value=100)
        r = weight / 100
        c, p = int(FOOD_DATA[item][0]*r), round(FOOD_DATA[item][1]*r, 1)
        st.info(f"📊 Preview: {c} kcal | P: {p}g")
        if st.button("SYNC MEAL"): st.success("Synced!")
    with f2:
        st.subheader("7-Day Planner Preview")
        st.write("Today: Chicken (200g) + Rice (150g)")
        st.button("Generate Grocery List")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]: # GYM LOG
    st.markdown('<div class="card">', unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        st.subheader("Log Your Set")
        st.selectbox("Muscle", ["Chest", "Back", "Legs", "Shoulders", "Arms"])
        st.text_input("Exercise", placeholder="Bench Press...")
        st.number_input("Weight (kg)", value=60.0)
        st.number_input("Reps", value=10)
        st.button("Log Workout Set")
    with g2:
        st.subheader("Volume Trend")
        # Placeholder for exercise volume chart
        st.line_chart([1000, 1200, 1100, 1500, 1400])
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]: # THE NEW SPLITS FEATURE
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧬 Training Architecture")
    split_choice = st.selectbox("Select Your Active Split", list(GYM_SPLITS.keys()))
    
    # Show the breakdown for the chosen split
    details = GYM_SPLITS[split_choice]
    scols = st.columns(len(details))
    for i, (day, routine) in enumerate(details.items()):
        with scols[i]:
            st.markdown(f"**{day}**")
            st.caption(routine)
    
    st.divider()
    if st.button(f"ACTIVATE {split_choice.upper()} PLAN"):
        st.success(f"System updated to {split_choice}!")
    st.markdown('</div>', unsafe_allow_html=True)