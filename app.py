from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime, timedelta
import requests

app = Flask(__name__, template_folder="Templates", static_folder='Static')
API_KEY = 'c965efd9d7e93fb45a4484bf4ccf5790'

@app.route('/')
def main():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET' ,'POST'])
def home():
    weather_data = None
    error_message = None

    date = None
    day = None
    iconURL = ''
    forecasts = None

    city = 'London'

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data, error_message = get_weather(city)
            date, day = get_city_date_and_day(city, API_KEY)
            iconURL = getIconURL(city, API_KEY)
            forecasts = getForecast(city, API_KEY)
    if request.method == 'GET':
        city = 'London'
        weather_data, error_message = get_weather(city)
        date, day = get_city_date_and_day(city, API_KEY)
        iconURL = getIconURL(city, API_KEY)
        forecasts = getForecast(city, API_KEY)
    return render_template('home.html', weather_data=weather_data, error_message=error_message, date=date, day=day, iconURL=iconURL, forecasts=forecasts)

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    print(f"Request URL: {url}")  # Debugging statement to check the URL
    try:
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")  # Debugging statement to check response status
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, "City not found."
        else:
            return None, "An error occurred while fetching the weather data."
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred: {e}"
    
def get_city_date_and_day(city_name, api_key):
    # Make the API request
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    # Extract the UNIX timestamp from the response
    timestamp = data['dt']
    
    # Convert the timestamp to a datetime object
    date_time = datetime.fromtimestamp(timestamp)
    
    # Get the date and day
    date = date_time.strftime('%Y-%m-%d')
    day = date_time.strftime('%A')
    
    return date, day

def getIconURL (city_name, api_key):
#   Make the API request
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

#   Extract the icon code
    icon_code = data['weather'][0]['icon']

#    Construct the URL for the icon
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

def kelvin_to_celsius(k):
    return k - 273.15

def getForecast(city_name, api_key):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        forecasts = data.get('list', [])

        current_time = datetime.utcnow()
        filtered_forecasts = []

        # Calculate the time intervals for the current hour, 2 hours before, and 2 hours after
        interval_hours = 3  # Forecasts are provided in 3-hour intervals

        # Calculate the specific hours we want to filter
        current_hour = current_time.hour
        target_hours = [
            (current_hour - 1) % 24,
            current_hour,
            (current_hour + 1) % 24
        ]

        for forecast in forecasts:
            try:
                forecast_time = datetime.fromtimestamp(forecast['dt'])
                forecast_hour = forecast_time.hour

                # Check if the forecast hour matches any of the target hours
                if forecast_hour in target_hours:
                    temperature_celsius = kelvin_to_celsius(forecast['main']['temp'])
                    description = forecast['weather'][0]['description']
                    filtered_forecasts.append({
                        'date': forecast_time.strftime('%d'),  # Format datetime as string
                        'temperature': round(temperature_celsius, 2),
                        'description': description
                    })
            except KeyError as e:
                print(f"KeyError: {e} - Skipping this forecast.")

        filter2 = [filtered_forecasts[0], filtered_forecasts[1], filtered_forecasts[2]]
        return filter2

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)