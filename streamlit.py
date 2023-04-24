import streamlit as st
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objs as go

# Set up the home page
def home():
    st.title("CALORIE TRACKER")
    st.write("Welcome to the Calorie Tracker! Use the sidebar to navigate to different pages.")
    
# Set up the food log page
def food_log():
    st.title("Food Log")
    
    # Create the form for adding a new food entry
    st.write("Add a new entry")
    with st.form("new_entry_form"):
        food_name = st.text_input("Food name")
        calories = st.number_input("Calories", min_value=0, step=1)
        date_consumed = st.date_input("Date consumed")
        submit_button = st.form_submit_button("Submit")
    
    # Add the new entry to the food log file
    if submit_button:
        new_entry = {"Food": food_name, "Calories": calories, "Date": date_consumed.strftime("%m/%d/%Y")}
        with open("food_log.csv", "a") as f:
            f.write(f"{new_entry['Food']},{new_entry['Calories']},{new_entry['Date']}\n")
    
    # Load the food log file into a DataFrame and display it
    try:
        df = pd.read_csv("food_log.csv", names=["Food", "Calories", "Date"])
        st.write(df)
    except FileNotFoundError:
        st.write("No food entries yet.")
        
# Set up the exercise log page - laxya add this
def exercise_log():
    st.title("Exercise Log")

# Set up the sidebar navigation
sidebar_options = {
    "Home": home,
    "Food Log": food_log,
    "Exercise Log": exercise_log
}

# Set up the page layout
def page_layout():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("", list(sidebar_options.keys()))
    sidebar_options[page]()

# Run the Streamlit app
if __name__ == '__main__':
    page_layout()
