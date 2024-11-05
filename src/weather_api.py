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
        city_data = self.get_weather_by_city(city_name)
        if not city_data:
            return None
        
        lat = city_data["coord"]["lat"]
        lon = city_data["coord"]["lon"]

        params = {
            "lat": lat,
            "lon": lon,
            "exclude": "current,minutely,hourly,alerts",
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(f"{self.base_url}/onecall", params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data["daily"][:days]  # Return only the requested number of days
        else:
            print(f"Error fetching forecast data: {response.status_code}")
            return None
