import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# API setup (Use your own OpenWeather API key)
API_KEY = '8b64c6f5bc6849b7d94956b4abd9d899'  # Replace with your OpenWeather API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Function to fetch weather data from OpenWeather API
def get_weather(city):
    try:
        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            raise ValueError("City not found")

        # Extract weather information
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']

        # Update the UI with weather data
        display_weather(temp, humidity, description, icon_img)
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to update the UI with weather data
def display_weather(temp, humidity, description, icon_img):
    # Update temperature, humidity, and description
    temp_label.config(text=f"Temperature: {temp}°C")
    humidity_label.config(text=f"Humidity: {humidity}%")
    description_label.config(text=f"Condition: {description.capitalize()}")

    # Update weather icon
    icon = ImageTk.PhotoImage(icon_img)
    icon_label.config(image=icon)
    icon_logo.png = icon  # Keep a reference

# Function to handle the city search
def on_search():
    city = city_entry.get().strip()
    if city:
        get_weather(city)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")

# Logo placeholder (you can replace this with an actual image)
logo = tk.Label(root, text="Weather App", font=("Arial", 24, "bold"), pady=20)
logo.pack()

# City input section
city_label = tk.Label(root, text="Enter City:", font=("Arial", 14))
city_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

search_button = tk.Button(root, text="Search", font=("Arial", 14), command=on_search)
search_button.pack(pady=10)

# Weather information display
temp_label = tk.Label(root, text="Temperature: N/A", font=("Arial", 14))
temp_label.pack(pady=5)

humidity_label = tk.Label(root, text="Humidity: N/A", font=("Arial", 14))
humidity_label.pack(pady=5)

description_label = tk.Label(root, text="Condition: N/A", font=("Arial", 14))
description_label.pack(pady=5)

# Weather icon display
icon_label = tk.Label(root)
icon_label.pack(pady=20)

# Run the application
root.mainloop()
