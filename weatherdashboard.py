from fasthtml import common as fh
from weather_api import WeatherAPI

class WeatherDashboard:
    def __init__(self, city_name=""):
        self.api = WeatherAPI()
        self.city_name = city_name
        self.weather_data = self.fetch_weather_data()

    def fetch_weather_data(self):
        """Fetch real data from the weather API. Return default values if API call fails or city is not provided."""
        if not self.city_name:
            return {"current_temp": "--", "condition": "N/A", "humidity": "--", "wind_speed": "--"}

        data = self.api.get_weather_by_city(self.city_name)
        if data:
            return {
                "current_temp": data["main"]["temp"],
                "condition": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
        else:
            return {"current_temp": "--", "condition": "N/A", "humidity": "--", "wind_speed": "--"}

    def render_weather_info(self):
        """Render the current weather information if a city is set, or a placeholder message otherwise."""
        if self.city_name and self.weather_data["current_temp"] != "--":
            weather_info = f"Current Weather in {self.city_name}: {self.weather_data['current_temp']}°C, {self.weather_data['condition']}"
            return fh.Div(
                fh.H2(weather_info, style="text-align: center;"),
                fh.Div(fh.H3(f"Humidity: {self.weather_data['humidity']}%"), style="text-align: center;"),
                fh.Div(fh.H3(f"Wind Speed: {self.weather_data['wind_speed']} km/h"), style="text-align: center;")
            )
        else:
            return fh.Div(
                fh.P("Please enter a city to view weather information.", style="text-align: center;")
            )

    def render(self):
        """Render the main dashboard layout."""
        return fh.Div(
            fh.H1("Weather Dashboard", style="text-align: center;"),
            
            # Display weather info or placeholder message
            self.render_weather_info(),
            
            # Input for updating weather
            fh.H3("Enter a city to update the weather:", style="text-align: center;"),
            fh.Div(
                fh.Input(
                    type="text", 
                    placeholder="Enter city name", 
                    name="city_name", 
                    id="city_name_input"
                ),
                fh.Button(
                    "Update Weather", 
                    hx_get="/update_weather", 
                    hx_target="#weather-info", 
                    hx_include="#city_name_input"
                ),
                style="display: flex; justify-content: center; gap: 10px;"
            ),
            
            # Placeholder for dynamically updated weather information
            fh.Div(id="weather-info", style="text-align: center;")
        )
