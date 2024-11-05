import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_weather_by_city(self, city_name):
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(f"{self.base_url}/weather", params=params)
        return response.json() if response.status_code == 200 else None

    def get_forecast_by_city(self, city_name, days=5):
        params = {
            "q": city_name,
            "cnt": days,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(f"{self.base_url}/forecast/daily", params=params)
        return response.json() if response.status_code == 200 else None
