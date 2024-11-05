from fasthtml import common as fh
from weather_api import WeatherAPI

class WeatherDashboard:
    def __init__(self, city_name="London"):
        self.api = WeatherAPI()
        self.city_name = city_name
        self.weather_data = self.fetch_weather_data()

    def fetch_weather_data(self):
        # Fetch real data from the weather API
        data = self.api.get_weather_by_city(self.city_name)
        if data:
            return {
                "current_temp": data["main"]["temp"],
                "condition": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
        else:
            # Mock data or default values if the API call fails
            return {"current_temp": "--", "condition": "N/A", "humidity": "--", "wind_speed": "--"}

    def render(self):
        return fh.Div(
            fh.H1("Weather Dashboard"),
            fh.Div(fh.H2(f"Current Weather in {self.city_name}: {self.weather_data['current_temp']}°C, {self.weather_data['condition']}"), cls="current-weather"),
            fh.Div(fh.H3(f"Humidity: {self.weather_data['humidity']}%"), cls="humidity"),
            fh.Div(fh.H3(f"Wind Speed: {self.weather_data['wind_speed']} km/h"), cls="wind-speed"),
            fh.H3("Enter a city to update the weather:"),
            fh.Div(
                fh.Input(type="text", placeholder="Enter city name", name="city_name", id="city_name_input", cls="city-input"),
                fh.Button("Update Weather", hx_get="/update_weather", hx_target="#weather-info", hx_include="#city_name_input"),
                cls="city-input-container"
            ),
            fh.Div(id="weather-info")  # Placeholder for updated weather info
        )
