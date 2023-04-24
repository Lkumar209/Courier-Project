import streamlit as st
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objs as go
 

data = []

def add_data(name, calories, date):
    new_item = {'Name': name, 'Calories': calories, 'Date': date}
    data.append(new_item)


def calculate_daily_calories(age, gender, height_cm, weight_kg, activity_level):
    if gender == 'Male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    if activity_level == 'Sedentary':
        tdee = bmr * 1.2
    elif activity_level == 'Lightly Active':
        tdee = bmr * 1.375
    elif activity_level == 'Moderately Active':
        tdee = bmr * 1.55
    elif activity_level == 'Very Active':
        tdee = bmr * 1.725
    else:
        tdee = bmr * 1.9
    return tdee

# Define a function to plot the calorie data on a graph
def plot_data():
    df = pd.DataFrame(data)

    daily_calories = df.groupby('Date').sum()['Calories']

    age = st.session_state.age
    gender = st.session_state.gender
    height_cm = st.session_state.height_cm
    weight_kg = st.session_state.weight_kg
    activity_level = st.session_state.activity_level
    tdee = calculate_daily_calories(age, gender, height_cm, weight_kg, activity_level)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_calories.index, y=daily_calories.values, name='Calories'))
    fig.add_trace(go.Scatter(x=daily_calories.index, y=[tdee] * len(daily_calories), name='Recommended'))
    fig.update_layout(title='Calorie Tracker', xaxis_title='Date', yaxis_title='Calories')
    st.plotly_chart(fig)

# Define the Streamlit app
def app():
    st.set_page_config(layout='wide')

    menu = ['Calorie Tracker', 'Food Log', 'Recommended Calorie Intake']

    choice = st.sidebar.selectbox('Select an option', menu)
    
    #calorie tracker where user can add data
    if choice == 'Calorie Tracker':
        st.title('Calorie Tracker')

        name = st.text_input('Food name')
        calories = st.number_input('Calories', step=1, min_value=0)
        date = st.date_input('Date')

        if st.button('Add'):
            add_data(name, calories, date)
            st.success('Food data added successfully!')

    # Define the Food Log section
    elif choice == 'Food Log':
        st.title('Food Log')
        # Add a table to show the food data
        df = pd.DataFrame(data)
        st.dataframe(df)

    # Define the Recommended Calorie Intake section
    elif choice == 'Recommended Calorie Intake':
        st.title('Recommended Calorie Intake')

        age = st.number_input('Age', step=1, min_value=1, max_value=120)
        gender = st.selectbox('Gender', ['Male', 'Female'])
        height_cm = st.number_input('Height (cm)', step=1, min_value=1, max_value=300)
        weight_kg = st.number_input('Weight (kg)', step=0.1, min_value=0.1, max_value=1000.0)
        activity_level = st.selectbox('Activity Level', ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active'])

        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.height_cm = height_cm
        st.session_state.weight_kg = weight_kg
        st.session_state.activity_level = activity_level

        plot_data()

# Run the Streamlit app
if __name__ == '__main__':
    app()
