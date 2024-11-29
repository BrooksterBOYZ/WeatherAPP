from flask import Flask, render_template, request, jsonify
import requests
from PIL import Image
import io

# API setup (Use your own OpenWeather API key)
API_KEY = '8b64c6f5bc6849b7d94956b4abd9d899'  # Replace with your OpenWeather API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

app = Flask(__name__)

# Function to fetch weather data
def get_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        return None  # If city is not found or other error

    # Extract weather information
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']
    icon_code = data['weather'][0]['icon']

    # Fetch weather icon
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
    icon_response = requests.get(icon_url)
    icon_img = Image.open(io.BytesIO(icon_response.content))

    return temp, humidity, description, icon_img

@app.route('/')
def home():
    return render_template('index.html')  # Render an HTML page

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    if city:
        weather_data = get_weather(city)
        if weather_data:
            temp, humidity, description, icon_img = weather_data
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            return render_template('weather.html', city=city, temp=temp, humidity=humidity, description=description, icon_url=icon_url)
        else:
            return render_template('error.html', message="City not found or API error.")
    else:
        return render_template('error.html', message="Please enter a city name.")

if __name__ == '__main__':
    app.run(debug=True)
