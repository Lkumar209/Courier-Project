import streamlit as st
from datetime import date, timedelta
import pandas as pd
import plotly.graph_objs as go

from PIL import Image
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup

#data logo identifiers
model = load_model('FV.h5')
labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango', 'Orange',
          'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']

#gets calories from google
def fetch_calories(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        print(scrap)
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        st.error("Can't fetch the Calories")
        print(e)

#processes the image through the model
def processed_img(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()

# Set up the home page
def home():
    st.title("CALORIE TRACKER")
    st.write("Welcome to the Calorie Tracker! Use the sidebar to navigate to different pages.")
    st.image("logo.png")
    
# Set up the add food page
def add_food():
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
        
def checkCalories():
    st.title("Upload")
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((300, 250))
        st.image(img, use_column_width=False)
        save_image_path = './upload_images/' + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result = processed_img(save_image_path)
            print(result)
            if result in vegetables:
                st.info('**Category : Vegetables**')
            else:
                st.info('**Category : Fruit**')
            st.success("**Predicted : " + result + '**')

            cal = 50
            #cal = fetch_calories(result)
            if cal:
               st.warning('**' + str(cal) + '(100 grams)**')

            today = date.today()
            d1 = today.strftime("%d/%m/%Y")

            new_entry = {"Food": result, "Calories": cal, "Date": d1}
            with open("food_log.csv", "a") as f:
                f.write(f"{new_entry['Food']},{new_entry['Calories']},{new_entry['Date']}\n")



#food log to show all the food
def food_log():
    st.title("Food Log")
    # Load the food log file into a DataFrame and display it
    try:
        df = pd.read_csv("food_log.csv", names=["Food", "Calories", "Date"])
        st.write(df)
    except FileNotFoundError:
        st.write("No food entries yet.")

# Set up the sidebar navigation
sidebar_options = {
    "Home": home,
    "Add Food": add_food,
    "Upload Food": checkCalories,
    "Food Log": food_log
}

# Set up the page layout
def page_layout():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("", list(sidebar_options.keys()))
    sidebar_options[page]()

# Run the Streamlit app
if __name__ == '__main__':
    page_layout()
