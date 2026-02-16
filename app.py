import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# =============================
# PAGE SETUP
# =============================
st.set_page_config(page_title="Optima Elite", layout="centered")
st.title("⚡ Optima Elite Fitness Tracker")

# =============================
# INITIALIZE MEMORY
# =============================
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

if "weight_log" not in st.session_state:
    st.session_state.weight_log = []

def save_data():
    pd.DataFrame(st.session_state.activity_log).to_csv("data.csv", index=False)
    pd.DataFrame(st.session_state.weight_log).to_csv("weight.csv", index=False)

# =============================
# FOOD DATABASE (per 100g or per unit)
# =============================
FOOD_DB = {
    # Fish & Meat
    "Rohu Fish": [97, 17, 4, 1],
    "Mutton (Goat)": [143, 27, 0, 6],
    "Chicken Breast": [165, 31, 0, 3.6],
    "Chicken Leg": [180, 28, 0, 7],
    "Chicken Thigh": [209, 26, 0, 10],
    # Dairy
    "Paneer": [265, 18, 3, 21],
    "Milk (cow)": [67, 3, 4, 4],
    "Yogurt (plain)": [59, 10, 4, 0],
    "Ghee": [900, 0, 0, 100],
    # Eggs
    "Boiled Egg (1 egg ~50g)": [70, 6, 0.5, 5],
    # Legumes / Pulses
    "Black Chana (boiled)": [164, 9, 27, 3],
    "White Chana (boiled)": [164, 9, 27, 3],
    "Bhatmas / Soybeans (dry)": [446, 36, 30, 20],
    "Masoor Dal (cooked)": [116, 9, 20, 0],
    "Rajma (cooked)": [127, 9, 22, 1],
    # Grains / Cereals
    "Rice (cooked)": [130, 3, 28, 0],
    "White Rice (uncooked)": [365, 7, 80, 0.6],
    "Oats (dry)": [389, 17, 66, 7],
    "Chapati (whole wheat, 1 medium ~40g)": [120, 4, 20, 3],
    # Vegetables
    "Spinach (cooked)": [23, 3, 3, 0],
    "Broccoli": [55, 4, 7, 1],
    "Carrot": [41, 1, 11, 0],
    "Radish": [33, 1, 8, 0],
    "Cucumber": [16, 1, 4, 0],
    # Others
    "Tofu": [76, 8, 5, 5],
}

# =============================
# EXERCISE DATABASE
# =============================
EXERCISE_DB = {
    "Chest": [
        "Bench Press", "Incline Bench Press", "Decline Bench Press",
        "Cable Fly", "Pecdeck Fly", "Incline Dumbbell Press",
        "Flat Dumbbell Press", "Decline Dumbbell Press", "Seated Chest Press",
        "Incline Smith Press"
    ],
    "Back": [
        "T Bar Row", "Seated Rowing", "Lat Pull-Down",
        "Single Hand Row", "Plate Loaded Lat Pull Down",
        "Kneeling Cable Pull-Down"
    ],
    "Arms": [
        "Cable Push Down", "Straight Bar Push Down", "DB Bicep Curl",
        "Straight Arm Extension", "Cable Curl", "Hammer Curl",
        "Preacher Curl", "Overhead Tricep Extension", "Face Pull"
    ],
    "Legs": [
        "Smith Machine Squat", "Hamstring Curl", "Stiff Leg",
        "Leg Extension", "Leg Press", "Standing Calf Raise",
        "Abductor Machine"
    ],
    "Shoulders": [
        "Dumbbell Shoulder Press", "Shoulder Press Machine",
        "Reverse Flies"
    ]
}

# Preset sets for each exercise
PRESET_SETS = {
    "Bench Press": ["15-12", "17.5-10", "20-7"],
    "Incline Bench Press": ["15-12", "17.5-8", "20-6"],
    "Decline Bench Press": ["15-12", "17.5-10", "20-7"],
    "Cable Fly": ["3-15", "4-10", "5-7"],
    "Pecdeck Fly": ["8-15", "9-10", "10-9"],
    "Cable Push Down": ["6-15", "7-10", "8-8"],
    "Straight Bar Push Down": ["6-12", "7-12", "8-10"],
    "Incline Dumbbell Press": ["15-12", "17.5-10", "20-10"],
    "Flat Dumbbell Press": ["15-12", "20-6", "20-7"],
    "Decline Dumbbell Press": ["15-12", "15-10", "15-9"],
    "Seated Chest Press": ["22.5-12", "25-10", "27.5-9"],
    "Incline Smith Press": ["15-12", "17.5-10", "20-8"],
    "T Bar Row": ["35-12", "40-10", "45-8"],
    "Seated Rowing": ["8-15", "9-12", "10-10"],
    "Lat Pull-Down": ["7-15", "8-12", "9-11"],
    "Single Hand Row": ["17.5-12", "20-11", "25-8"],
    "Plate Loaded Lat Pull Down": ["40-12", "50-10", "55-8"],
    "Kneeling Cable Pull-Down": ["6-12", "7-7"],
    "DB Bicep Curl": ["10-12", "10-12", "12.5-8"],
    "Straight Arm Extension": ["5-15", "6-10", "7-8"],
    "Cable Curl": ["5-12", "6-10", "7-9"],
    "Hammer Curl": ["10-12", "12.5-10", "15-10"],
    "Preacher Curl": ["20-12", "22.5-10", "25-9"],
    "Overhead Tricep Extension": ["3-15", "4-15", "5-13"],
    "Face Pull": ["5-12", "6-11", "7-10"],
    "Smith Machine Squat": ["25-12", "30-8", "35-6"],
    "Hamstring Curl": ["10-15", "12-12"],
    "Stiff Leg": ["10-12", "15-10", "20-7"],
    "Leg Extension": ["6-15", "7-12"],
    "Leg Press": ["115-15", "120-11", "130-8"],
    "Standing Calf Raise": ["60-15", "70-15"],
    "Abductor Machine": ["48-12", "54-10", "60-10"],
    "Dumbbell Shoulder Press": ["12.5-12", "15-10", "20-7"],
    "Shoulder Press Machine": ["25-12", "27.5-10", "30-9"],
    "Reverse Flies": ["6-15", "7-12", "8-8"]
}

# =============================
# USER INFO SIDEBAR
# =============================
st.sidebar.subheader("User Info (for BMR)")
age = st.sidebar.number_input("Age", value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
height = st.sidebar.number_input("Height (cm)", value=170)
weight_now = st.sidebar.number_input("Current Weight (kg)", value=70)
body_fat = st.sidebar.number_input("Body Fat % (optional)", value=20)

# BMR calculation
if gender == "Male":
    bmr = 10*weight_now + 6.25*height - 5*age + 5
else:
    bmr = 10*weight_now + 6.25*height - 5*age - 161
st.sidebar.metric("BMR (Calories/day)", f"{int(bmr)} kcal")

# =============================
# TABS
# =============================
tabs = st.tabs(["Dashboard", "Nutrition", "Workout", "History"])

# =============================
# DASHBOARD TAB
# =============================
with tabs[0]:
    st.subheader("Calorie Tracker")
    df = pd.DataFrame(st.session_state.activity_log)
    total_cal = df["Calories"].sum() if not df.empty else 0
    goal_cal = st.slider("Daily Calorie Goal", 1000, 4000, 2200)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_cal,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Calories"},
        gauge={
            'axis': {'range': [0, goal_cal]},
            'bar': {'color': "#FF4B4B"},
            'bgcolor': "lightgray",
            'steps': [
                {'range': [0, goal_cal*0.5], 'color': "lightgreen"},
                {'range': [goal_cal*0.5, goal_cal*0.75], 'color': "yellow"},
                {'range': [goal_cal*0.75, goal_cal], 'color': "red"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# =============================
# NUTRITION TAB
# =============================
with tabs[1]:
    st.subheader("Log Food / Macros")
    food = st.selectbox("Select Food", list(FOOD_DB.keys()))
    qty = st.number_input("Quantity (grams or unit for eggs/chapati)", value=100, min_value=1)

    cal = FOOD_DB[food][0]*(qty/100)
    protein = FOOD_DB[food][1]*(qty/100)
    carbs = FOOD_DB[food][2]*(qty/100)
    fat = FOOD_DB[food][3]*(qty/100)

    st.markdown(f"**Calories:** {cal:.1f} kcal | **Protein:** {protein:.1f} g | **Carbs:** {carbs:.1f} g | **Fat:** {fat:.1f} g")

    if st.button("Add Food Log"):
        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Food",
            "Details": f"{qty}g {food}",
            "Calories": cal,
            "Protein": protein,
            "Carbs": carbs,
            "Fat": fat
        })
        save_data()
        st.success("Food logged!")

# =============================
# WORKOUT TAB
# =============================
with tabs[2]:
    st.subheader("Log Workout")
    muscle = st.selectbox("Muscle Group", list(EXERCISE_DB.keys()))
    ex = st.selectbox("Exercise", EXERCISE_DB[muscle])
    preset = PRESET_SETS.get(ex, [])
    st.markdown("**Preset Sets/Reps:** " + ", ".join(preset))

    weight = st.number_input("Weight (kg)", value=15)
    reps = st.number_input("Reps", value=12)
    sets = st.number_input("Sets", value=3)

    if st.button("Log Workout"):
        burned = int(weight * reps * sets * 0.1)
        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Workout",
            "Details": f"{ex} | {weight}kg × {reps} × {sets}",
            "Calories": -burned,
            "Protein": 0,
            "Carbs": 0,
            "Fat": 0
        })
        save_data()
        st.success(f"Workout logged! Burned {burned} kcal")

# =============================
# HISTORY TAB
# =============================
with tabs[3]:
    st.subheader("History")
    if not df.empty:
        st.dataframe(df)
        if st.button("Clear Logs"):
            st.session_state.activity_log = []
            save_data()
            st.experimental_rerun()
    else:
        st.info("No logs yet.")
