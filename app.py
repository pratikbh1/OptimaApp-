import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import random

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

if "steps_log" not in st.session_state:
    st.session_state.steps_log = []

if "sleep_log" not in st.session_state:
    st.session_state.sleep_log = []

# =============================
# DATABASES
# =============================
FOOD_DB = {
    "Rohu Fish": [97, 17, 4, 1],
    "Mutton (Goat)": [143, 27, 0, 6],
    "Chicken Breast": [165, 31, 0, 3.6],
    "Chicken Leg": [180, 28, 0, 7],
    "Chicken Thigh": [209, 26, 0, 10],
    "Paneer": [265, 18, 3, 21],
    "Milk (cow)": [67, 3, 4, 4],
    "Yogurt (plain)": [59, 10, 4, 0],
    "Ghee": [900, 0, 0, 100],
    "Boiled Egg (1 egg ~50g)": [70, 6, 0.5, 5],
    "Black Chana (boiled)": [164, 9, 27, 3],
    "White Chana (boiled)": [164, 9, 27, 3],
    "Bhatmas / Soybeans (dry)": [446, 36, 30, 20],
    "Masoor Dal (cooked)": [116, 9, 20, 0],
    "Rajma (cooked)": [127, 9, 22, 1],
    "Rice (cooked)": [130, 3, 28, 0],
    "White Rice (uncooked)": [365, 7, 80, 0.6],
    "Oats (dry)": [389, 17, 66, 7],
    "Chapati (whole wheat, 1 medium ~40g)": [120, 4, 20, 3],
    "Spinach (cooked)": [23, 3, 3, 0],
    "Broccoli": [55, 4, 7, 1],
    "Carrot": [41, 1, 11, 0],
    "Radish": [33, 1, 8, 0],
    "Cucumber": [16, 1, 4, 0],
    "Tofu": [76, 8, 5, 5],
}

EXERCISE_DB = {
    "Chest": ["Bench Press", "Incline Bench Press", "Decline Bench Press", "Cable Fly", "Pecdeck Fly",
              "Incline Dumbbell Press", "Flat Dumbbell Press", "Decline Dumbbell Press", "Seated Chest Press",
              "Incline Smith Press"],
    "Back": ["T Bar Row", "Seated Rowing", "Lat Pull-Down", "Single Hand Row", "Plate Loaded Lat Pull Down",
             "Kneeling Cable Pull-Down"],
    "Arms": ["Cable Push Down", "Straight Bar Push Down", "DB Bicep Curl", "Straight Arm Extension", "Cable Curl",
             "Hammer Curl", "Preacher Curl", "Overhead Tricep Extension", "Face Pull"],
    "Legs": ["Smith Machine Squat", "Hamstring Curl", "Stiff Leg", "Leg Extension", "Leg Press",
             "Standing Calf Raise", "Abductor Machine"],
    "Shoulders": ["Dumbbell Shoulder Press", "Shoulder Press Machine", "Reverse Flies"]
}

PRESET_SETS = {
    # Chest
    "Bench Press": ["15-12", "17.5-10", "20-7"],
    "Incline Bench Press": ["15-12", "17.5-8", "20-6"],
    "Decline Bench Press": ["15-12", "17.5-10", "20-7"],
    "Cable Fly": ["3-15", "4-10", "5-7"],
    "Pecdeck Fly": ["8-15", "9-10", "10-9"],
    "Incline Dumbbell Press": ["15-12", "17.5-10", "20-10"],
    "Flat Dumbbell Press": ["15-12", "20-6", "20-7"],
    "Decline Dumbbell Press": ["15-12", "15-10", "15-9"],
    "Seated Chest Press": ["22.5-12", "25-10", "27.5-9"],
    "Incline Smith Press": ["15-12", "17.5-10", "20-8"],
    # Back
    "T Bar Row": ["35-12", "40-10", "45-8"],
    "Seated Rowing": ["8-15", "9-12", "10-10"],
    "Lat Pull-Down": ["7-15", "8-12", "9-11"],
    "Single Hand Row": ["17.5-12", "20-11", "25-8"],
    "Plate Loaded Lat Pull Down": ["40-12", "50-10", "55-8"],
    "Kneeling Cable Pull-Down": ["6-12", "7-7"],
    # Arms
    "Cable Push Down": ["6-15", "7-10", "8-8"],
    "Straight Bar Push Down": ["6-12", "7-12", "8-10"],
    "DB Bicep Curl": ["10-12", "10-12", "12.5-8"],
    "Straight Arm Extension": ["5-15", "6-10", "7-8"],
    "Cable Curl": ["5-12", "6-10", "7-9"],
    "Hammer Curl": ["10-12", "12.5-10", "15-10"],
    "Preacher Curl": ["20-12", "22.5-10", "25-9"],
    "Overhead Tricep Extension": ["3-15", "4-15", "5-13"],
    "Face Pull": ["5-12", "6-11", "7-10"],
    # Legs
    "Smith Machine Squat": ["25-12", "30-8", "35-6"],
    "Hamstring Curl": ["10-15", "12-12"],
    "Stiff Leg": ["10-12", "15-10", "20-7"],
    "Leg Extension": ["6-15", "7-12"],
    "Leg Press": ["115-15", "120-11", "130-8"],
    "Standing Calf Raise": ["60-15", "70-15"],
    "Abductor Machine": ["48-12", "54-10", "60-10"],
    # Shoulders
    "Dumbbell Shoulder Press": ["12.5-12", "15-10", "20-7"],
    "Shoulder Press Machine": ["25-12", "27.5-10", "30-9"],
    "Reverse Flies": ["6-15", "7-12", "8-8"]
}

# =============================
# USER INFO SIDEBAR
# =============================
st.sidebar.subheader("User Info (for BMR & Weight)")
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
tabs = st.tabs(["Dashboard", "Nutrition", "Workout", "History", "Weight & Steps", "Weekly Charts"])

# =============================
# SIMULATED AUTO STEPS & SLEEP
# =============================
today = datetime.now().strftime("%Y-%m-%d")
sim_steps = random.randint(3000, 12000)
sim_sleep = round(random.uniform(5, 9), 1)

if not any(log["Time"]==today for log in st.session_state.steps_log):
    st.session_state.steps_log.append({"Time": today, "Steps": sim_steps})
if not any(log["Time"]==today for log in st.session_state.sleep_log):
    st.session_state.sleep_log.append({"Time": today, "SleepHours": sim_sleep})

# =============================
# DASHBOARD TAB
# =============================
with tabs[0]:
    st.subheader("Calorie & Macro Tracker")
    df = pd.DataFrame(st.session_state.activity_log)
    total_cal = df["Calories"].sum() if not df.empty else 0
    total_protein = df["Protein"].sum() if not df.empty else 0
    total_carbs = df["Carbs"].sum() if not df.empty else 0
    total_fat = df["Fat"].sum() if not df.empty else 0

    goal_cal = st.slider("Daily Calorie Goal", 1000, 4000, 2200)
    goal_protein = st.slider("Daily Protein Goal (g)", 50, 300, 150)
    goal_carbs = st.slider("Daily Carbs Goal (g)", 50, 400, 200)
    goal_fat = st.slider("Daily Fat Goal (g)", 20, 150, 50)

    # Calorie gauge
    fig_cal = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_cal,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Calories"},
        gauge={'axis': {'range': [0, goal_cal]},
               'bar': {'color': "#FF4B4B"},
               'steps': [{'range':[0, goal_cal*0.5], 'color':'lightgreen'},
                         {'range':[goal_cal*0.5, goal_cal*0.75], 'color':'yellow'},
                         {'range':[goal_cal*0.75, goal_cal], 'color':'red'}]}
    ))
    st.plotly_chart(fig_cal, use_container_width=True)

    # Macro Rings
    fig_macro = go.Figure()
    fig_macro.add_trace(go.Pie(values=[total_protein, max(goal_protein-total_protein,0)],
                               labels=["Protein", "Remaining"], hole=0.6, name="Protein",
                               marker_colors=["#FF6361", "#E5E5E5"]))
    fig_macro.add_trace(go.Pie(values=[total_carbs, max(goal_carbs-total_carbs,0)],
                               labels=["Carbs", "Remaining"], hole=0.6, name="Carbs",
                               marker_colors=["#FFA600", "#E5E5E5"]))
    fig_macro.add_trace(go.Pie(values=[total_fat, max(goal_fat-total_fat,0)],
                               labels=["Fat", "Remaining"], hole=0.6, name="Fat",
                               marker_colors=["#58508D", "#E5E5E5"]))
    fig_macro.update_layout(title_text="Macro Progress", grid={'rows':1,'columns':3})
    st.plotly_chart(fig_macro, use_container_width=True)

    st.metric("Steps Today", st.session_state.steps_log[-1]["Steps"])
    st.metric("Sleep Hours", st.session_state.sleep_log[-1]["SleepHours"])

# =============================
# NUTRITION TAB
# =============================
with tabs[1]:
    st.subheader("Log Your Meals")
    food_query = st.text_input("Search Food")
    foods_filtered = [f for f in FOOD_DB if food_query.lower() in f.lower()] if food_query else list(FOOD_DB.keys())
    food_choice = st.selectbox("Select Food", foods_filtered)
    grams = st.number_input("Quantity (grams)", min_value=1, value=100)

    if st.button("Log Food"):
        cal, protein, carbs, fat = FOOD_DB[food_choice]
        multiplier = grams / 100
        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Food",
            "Details": f"{grams}g {food_choice}",
            "Calories": int(cal*multiplier),
            "Protein": round(protein*multiplier,1),
            "Carbs": round(carbs*multiplier,1),
            "Fat": round(fat*multiplier,1)
        })
        st.success("Food logged successfully!")

# =============================
# WORKOUT TAB
# =============================
with tabs[2]:
    st.subheader("Log Your Workout")
    muscle_group = st.selectbox("Select Muscle Group", list(EXERCISE_DB.keys()))
    exercise_choice = st.selectbox("Select Exercise", EXERCISE_DB[muscle_group])
    weight = st.number_input("Weight (kg)", value=20)
    reps = st.text_input("Sets x Reps (e.g., 15-12,17.5-10,20-7)", value=",".join(PRESET_SETS.get(exercise_choice,[])))

    if st.button("Log Workout"):
        burned_cal = len(reps.split(",")) * 50  # simple cal estimate
        st.session_state.activity_log.append({
            "Time": datetime.now().strftime("%H:%M"),
            "Type": "Workout",
            "Details": f"{exercise_choice} @ {weight}kg Sets/Reps: {reps}",
            "Calories": -burned_cal,
            "Protein": 0,
            "Carbs": 0,
            "Fat": 0
        })
        st.success("Workout logged successfully!")

# =============================
# HISTORY TAB
# =============================
with tabs[3]:
    st.subheader("Daily Activity Log")
    if st.session_state.activity_log:
        df = pd.DataFrame(st.session_state.activity_log)
        st.dataframe(df)
        st.metric("Net Calories Today", df["Calories"].sum())
    else:
        st.info("No activity logged today.")

# =============================
# WEIGHT & STEPS TAB
# =============================
with tabs[4]:
    st.subheader("Weight & Steps")
    w = st.number_input("Log Weight (kg)", value=weight_now)
    if st.button("Save Weight"):
        st.session_state.weight_log.append({"Time": today, "Weight": w})
        st.success("Weight saved!")

    s = st.number_input("Log Steps manually", value=st.session_state.steps_log[-1]["Steps"])
    if st.button("Save Steps"):
        st.session_state.steps_log.append({"Time": today, "Steps": s})
        st.success("Steps saved!")

    sl = st.number_input("Log Sleep Hours manually", value=st.session_state.sleep_log[-1]["SleepHours"])
    if st.button("Save Sleep"):
        st.session_state.sleep_log.append({"Time": today, "SleepHours": sl})
        st.success("Sleep saved!")

# =============================
# WEEKLY CHARTS TAB
# =============================
with tabs[5]:
    st.subheader("Weekly Progress Charts")
    # Calories
    df_cal = pd.DataFrame(st.session_state.activity_log)
    if not df_cal.empty:
        df_cal["Date"] = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
        cal_chart = df_cal.groupby("Date")["Calories"].sum().reset_index()
        st.line_chart(cal_chart.rename(columns={"Calories":"Net Calories"}).set_index("Date"))

    # Weight
    if st.session_state.weight_log:
        df_w = pd.DataFrame(st.session_state.weight_log)
        df_w["Time"] = pd.to_datetime(df_w["Time"])
        st.line_chart(df_w.set_index("Time")["Weight"])

    # Steps
    if st.session_state.steps_log:
        df_s = pd.DataFrame(st.session_state.steps_log)
        df_s["Time"] = pd.to_datetime(df_s["Time"])
        st.line_chart(df_s.set_index("Time")["Steps"])

    # Sleep
    if st.session_state.sleep_log:
        df_sl = pd.DataFrame(st.session_state.sleep_log)
        df_sl["Time"] = pd.to_datetime(df_sl["Time"])
        st.line_chart(df_sl.set_index("Time")["SleepHours"])

# =============================
# EXPORT BUTTON
# =============================
st.subheader("Export Data")
if st.button("Export Activity Log CSV"):
    df_export = pd.DataFrame(st.session_state.activity_log)
    df_export.to_csv("activity_log.csv", index=False)
    st.success("Activity log exported as activity_log.csv")

if st.button("Export Weight Log CSV"):
    df_export = pd.DataFrame(st.session_state.weight_log)
    df_export.to_csv("weight_log.csv", index=False)
    st.success("Weight log exported as weight_log.csv")

if st.button("Export Steps Log CSV"):
    df_export = pd.DataFrame(st.session_state.steps_log)
    df_export.to_csv("steps_log.csv", index=False)
    st.success("Steps log exported as steps_log.csv")

if st.button("Export Sleep Log CSV"):
    df_export = pd.DataFrame(st.session_state.sleep_log)
    df_export.to_csv("sleep_log.csv", index=False)
    st.success("Sleep log exported as sleep_log.csv")
