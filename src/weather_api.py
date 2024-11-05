import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.tomorrow_api_key = os.getenv("TOMORROW_API_KEY")
        self.openweathermap_base_url = "http://api.openweathermap.org/data/2.5"
        self.tomorrow_base_url = "https://api.tomorrow.io/v4/timelines"
        
    def get_weather_by_city(self, city_name):
        params = {
            "q": city_name,
            "appid": self.openweathermap_api_key,
            "units": "metric"
        }
        response = requests.get(f"{self.openweathermap_base_url}/weather", params=params)
        if response.status_code == 200:
            data = response.json()
            precipitation = data.get("rain", {}).get("1h", 0)
            return {
                "current_temp": data["main"]["temp"],
                "condition": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "precipitation": precipitation,
                "coord": data.get("coord", {})
            }
        else:
            print("Error: Unable to retrieve weather data from OpenWeatherMap.")
            return None

    def get_5_day_forecast_tomorrow(self, city_name):
        """Fetches 5-day forecast data using Tomorrow.io API for a specific city."""
        city_data = self.get_weather_by_city(city_name)
        if not city_data or "coord" not in city_data:
            print("Error: Unable to retrieve city coordinates.")
            return None

        lat = city_data["coord"].get("lat")
        lon = city_data["coord"].get("lon")

        # Validate coordinates before making the API request
        if lat is None or lon is None:
            print("Error: Missing latitude or longitude for Tomorrow.io forecast.")
            return None

        start_time = datetime.utcnow().isoformat() + "Z"
        end_time = (datetime.utcnow() + timedelta(days=5)).isoformat() + "Z"

        params = {
            "apikey": self.tomorrow_api_key,
            "location": f"{lat},{lon}",
            "fields": ["temperatureMin", "temperatureMax", "humidityAvg", "windGust", "precipitationIntensityAvg"],
            "units": "metric",
            "timesteps": "1d",
            "startTime": start_time,
            "endTime": end_time
        }

        response = requests.get(self.tomorrow_base_url, params=params)
        if response.status_code == 200:
            forecast_data = response.json()
            return forecast_data.get("data", {}).get("timelines", [])[0].get("intervals", [])
        else:
            print("Error fetching Tomorrow.io forecast data:", response.status_code, response.text)
            return None
