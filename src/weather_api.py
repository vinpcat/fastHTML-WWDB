import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
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
        return response.json() if response.status_code == 200 else None

    def get_7_day_forecast_tomorrow(self, city_name):
        """Fetches 7-day forecast data using Tomorrow.io API for a specific city."""
        # Get city coordinates using OpenWeatherMap
        city_data = self.get_weather_by_city(city_name)
        if not city_data:
            print("Error: Unable to retrieve city coordinates.")
            return None

        lat = city_data["coord"]["lat"]
        lon = city_data["coord"]["lon"]

        # Define start and end times for 7-day forecast
        start_time = datetime.utcnow().isoformat() + "Z"
        end_time = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"

        params = {
            "apikey": self.tomorrow_api_key,
            "location": f"{lat},{lon}",
            "fields": ["temperatureMin", "temperatureMax"],
            "units": "metric",
            "timesteps": "1d",
            "startTime": start_time,
            "endTime": end_time
        }

        response = requests.get(self.tomorrow_base_url, params=params)
        
        if response.status_code == 200:
            forecast_data = response.json()
            print("Tomorrow.io 7-day forecast data:", forecast_data)  # Debugging output
            return forecast_data.get("data", {}).get("timelines", [])[0].get("intervals", [])
        else:
            print("Error fetching Tomorrow.io forecast data:", response.status_code, response.text)
            return None
