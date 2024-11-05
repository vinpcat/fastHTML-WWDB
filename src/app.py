from fasthtml import common as fh
from weatherdashboard import WeatherDashboard
from visualise import generate_weather_chart
from error_handler import validate_forecast_days

app, rt = fh.fast_app()

@rt("/", ["get"])
def homepage():
    return WeatherDashboard().render()

@rt("/update_weather", ["get"])
def update_weather(city_name: str):
    from weather_api import WeatherAPI
    api = WeatherAPI()
    data = api.get_weather_by_city(city_name)
    
    if data and all(key in data for key in ["current_temp", "condition", "humidity", "wind_speed", "precipitation"]):
        weather_info = {
            "current_temp": data["current_temp"],
            "condition": data["condition"],
            "humidity": data["humidity"],
            "wind_speed": data["wind_speed"],
            "precipitation": data["precipitation"]
        }
        
        return fh.Div(
            fh.H2(f"Current Weather in {city_name}: {weather_info['current_temp']}°C, {weather_info['condition']}"),
            fh.Div(
                fh.Div(fh.H3(f"Temperature: {weather_info['current_temp']}°C"), cls="box"),
                fh.Div(fh.H3(f"Humidity: {weather_info['humidity']}%"), cls="box"),
                fh.Div(fh.H3(f"Wind Speed: {weather_info['wind_speed']} km/h"), cls="box"),
                fh.Div(fh.H3(f"Precipitation: {weather_info['precipitation']} mm"), cls="box"),
                style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; padding: 10px;"
            ),
            cls="updated-weather"
        )
    else:
        return fh.Div(
            fh.P("Error: Unable to fetch weather data. Please check the city name or try again later.", cls="error-message")
        )

@rt("/get_forecast_chart", ["get"])
def get_forecast_chart(city_name: str, forecast_days: str = "5"):
    validation_error = validate_forecast_days(forecast_days)
    if validation_error:
        return validation_error
    
    forecast_days = int(forecast_days)
    return generate_weather_chart(city_name, forecast_days)

fh.serve()
