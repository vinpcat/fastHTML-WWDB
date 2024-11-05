from fasthtml import common as fh
from weatherdashboard import WeatherDashboard
from visualise import generate_weather_chart

app, rt = fh.fast_app()

@rt("/", ["get"])
def homepage():
    return WeatherDashboard().render()

@rt("/update_weather", ["get"])
def update_weather(city_name: str):
    from weather_api import WeatherAPI
    api = WeatherAPI()
    data = api.get_weather_by_city(city_name)
    
    if data:
        weather_info = {
            "current_temp": data["main"]["temp"],
            "condition": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        
        return fh.Div(
            fh.H2(f"Current Weather in {city_name}: {weather_info['current_temp']}°C, {weather_info['condition']}"),
            fh.H3(f"Humidity: {weather_info['humidity']}%"),
            fh.H3(f"Wind Speed: {weather_info['wind_speed']} km/h"),
            cls="updated-weather"
        )
    else:
        return fh.Div(
            fh.P("Error: Unable to fetch weather data. Please try again.", cls="error-message")
        )

@rt("/get_forecast_chart", ["get"])
def get_forecast_chart(city_name: str):
    return generate_weather_chart(city_name, use_tomorrow_api=True)

fh.serve()
