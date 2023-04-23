import tkinter as tk

class FoodCalorieCounter:
    def __init__(self, master):
        self.master = master
        self.master.title("Food Calorie Counter")

        # Create labels and entries for food and calorie input
        self.food_label = tk.Label(self.master, text="Enter food item: ")
        self.food_label.grid(row=0, column=0)

        self.food_entry = tk.Entry(self.master)
        self.food_entry.grid(row=0, column=1)

        self.calorie_label = tk.Label(self.master, text="Enter calorie count: ")
        self.calorie_label.grid(row=1, column=0)

        self.calorie_entry = tk.Entry(self.master)
        self.calorie_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.master, text="Add", command=self.add_food)
        self.add_button.grid(row=2, column=1)

        self.total_calories_label = tk.Label(self.master, text="Total Calories: 0")
        self.total_calories_label.grid(row=3, column=0, columnspan=2)

        self.total_calories = 0

    def add_food(self):
        food_item = self.food_entry.get()
        calorie_count = int(self.calorie_entry.get())

        self.total_calories += calorie_count
        self.total_calories_label.config(text="Total Calories: " + str(self.total_calories))

        self.food_entry.delete(0, tk.END)
        self.calorie_entry.delete(0, tk.END)

root = tk.Tk()
app = FoodCalorieCounter(root)
root.mainloop()
