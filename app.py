import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# =====================================================
# PAGE SETUP
# =====================================================
st.set_page_config(page_title="Optima Elite", layout="wide")
st.title("⚡ Optima Elite Fitness Tracker")

# =====================================================
# LOAD OR CREATE DATA
# =====================================================
if "activity_log" not in st.session_state:
    if os.path.exists("data.csv"):
        st.session_state.activity_log = pd.read_csv("data.csv").to_dict("records")
    else:
        st.session_state.activity_log = []

if "weight_log" not in st.session_state:
    if os.path.exists("weight.csv"):
        st.session_state.weight_log = pd.read_csv("weight.csv").to_dict("records")
    else:
        st.session_state.weight_log = []

def save_data():
    pd.DataFrame(st.session_state.activity_log).to_csv("data.csv", index=False)
    pd.DataFrame(st.session_state.weight_log).to_csv("weight.csv", index=False)

# =====================================================
# DATABASES
# =====================================================
FOOD_DB = {
    "Chicken Breast": [165, 31, 0, 3.6],
    "Paneer": [265, 18, 3, 21],
    "Soya Chunks": [345, 52, 33, 0.5],
    "Egg": [155, 13, 1, 11],
    "Rice (Cooked)": [130, 2.5, 28, 0.3]
}

EXERCISE_DB = {
    "Chest": ["Bench Press", "Pushups", "Cable Fly"],
    "Back": ["Rows", "Pulldown"],
    "Legs": ["Squat", "Leg Press"],
    "Arms": ["Bicep Curl", "Tricep Pushdown"]
}

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.subheader("User Info for BMR")
age = st.sidebar.number_input("Age", value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height = st.sidebar.number_input("Height (cm)", value=170)
weight_now = st.sidebar.number_input("Current Weight (kg)", value=70)
body_fat = st.sidebar.number_input("Body Fat % (optional)", value=20)

# Calculate BMR (Mifflin-St Jeor)
if gender == "Male":
    bmr = 10*weight_now + 6.25*height - 5*age + 5
else:
    bmr = 10*weight_now + 6.25*height - 5*age - 161

st.sidebar.metric("BMR (Calories/day)", f"{int(bmr)} kcal")

# =====================================================
# TABS
# =====================================================
tabs = st.tabs(["Dashboard", "Nutrition", "Workout", "Steps", "Weight & Body Fat", "Weekly Charts", "History"])

# =====================================================
# DASHBOARD
# =====================================================
with tabs[0]:
    st.subheader("Today's Summary")

    if st.session_state.activity_log:
        df = pd.DataFrame(st.session_state.activity_log)
        total_cal = df["Calories"].sum()
        total_pro = df.get("Protein", 0).sum()
        total_carbs = df.get("Carbs", 0).sum()
        total_fat = df.get("Fat", 0).sum()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Calories", f"{total_cal} kcal")
        c2.metric("Protein", f"{total_pro} g")
        c3.metric("Carbs", f"{total_carbs} g")
        c4.metric("Fat", f"{total_fat} g")

        st.progress(min(total_cal / bmr, 1.0))

    else:
        st.info("Start logging food, workouts, and steps.")

# =====================================================
# NUTRITION
# =====================================================
with tabs[1]:
    st.subheader("Log Food")
    food = st.selectbox("Food", list(FOOD_DB.keys()))
    grams = st.number_input("Grams", value=100)

    if st.button("Add Food"):
        factor = grams / 100
        cals = FOOD_DB[food][0] * factor
        protein = FOOD_DB[food][1] * factor
        carbs = FOOD_DB[food][2] * factor
        fat = FOOD_DB[food][3] * factor

        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Food",
            "Details": f"{grams}g {food}",
            "Calories": round(cals),
            "Protein": round(protein,1),
            "Carbs": round(carbs,1),
            "Fat": round(fat,1)
        })

        save_data()
        st.success("Food logged!")

# =====================================================
# WORKOUT
# =====================================================
with tabs[2]:
    st.subheader("Log Workout")
    muscle = st.selectbox("Muscle Group", list(EXERCISE_DB.keys()))
    exercise = st.selectbox("Exercise", EXERCISE_DB[muscle])
    weight = st.number_input("Weight (kg)", value=40)
    reps = st.number_input("Reps", value=10)
    sets = st.number_input("Sets", value=3)

    if st.button("Log Workout"):
        burned = int(weight * reps * sets * 0.1)
        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Workout",
            "Details": f"{exercise} | {weight}kg × {reps} × {sets}",
            "Calories": -burned,
            "Protein": 0,
            "Carbs": 0,
            "Fat": 0
        })
        save_data()
        st.success(f"Workout logged! Burned {burned} kcal")

# =====================================================
# STEPS
# =====================================================
with tabs[3]:
    st.subheader("Daily Steps")
    steps = st.number_input("Steps Walked", value=0)
    if st.button("Log Steps"):
        burned = int(steps * 0.04)
        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Steps",
            "Details": f"{steps} steps",
            "Calories": -burned,
            "Protein": 0,
            "Carbs": 0,
            "Fat": 0
        })
        save_data()
        st.success(f"Steps logged! Burned {burned} kcal")

# =====================================================
# WEIGHT & BODY FAT
# =====================================================
with tabs[4]:
    st.subheader("Log Weight & Body Fat")
    w = st.number_input("Weight (kg)", value=weight_now)
    bf = st.number_input("Body Fat %", value=body_fat)

    if st.button("Log Weight"):
        st.session_state.weight_log.append({
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Weight": w,
            "Body Fat %": bf
        })
        save_data()
        st.success("Weight & body fat logged!")

    if st.session_state.weight_log:
        st.line_chart(pd.DataFrame(st.session_state.weight_log)[["Weight","Body Fat %"]])

# =====================================================
# WEEKLY CHARTS
# =====================================================
with tabs[5]:
    st.subheader("Weekly Summary")
    if st.session_state.activity_log:
        df = pd.DataFrame(st.session_state.activity_log)
        df["Date"] = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
        st.bar_chart(df.groupby("Type")["Calories"].sum())
    else:
        st.info("No logs to display")

# =====================================================
# HISTORY
# =====================================================
with tabs[6]:
    st.subheader("History")
    if st.session_state.activity_log:
        st.dataframe(pd.DataFrame(st.session_state.activity_log))
        if st.button("Clear All Data"):
            st.session_state.activity_log = []
            st.session_state.weight_log = []
            save_data()
            st.experimental_rerun()
    else:
        st.info("No history yet.")
