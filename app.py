from fasthtml import common as fh
from visualise import generate_weather_chart
from weatherdashboard import WeatherDashboard
from error_handler import validate_forecast_days  # Import the error handler

app, rt = fh.fast_app()

@rt("/", ["get"])
def homepage():
    return WeatherDashboard().render()

@rt("/update_forecast", ["get"])
def update_forecast(forecast_days: int):
    # Validate forecast_days input
    error_message = validate_forecast_days(forecast_days)
    
    # If there's an error message, return it immediately
    if error_message:
        return error_message

    # If input is valid, generate and display the chart
    return fh.Div(
        generate_weather_chart(int(forecast_days)),  # Cast to int to ensure correct type
        fh.P(f"Forecast for the next {forecast_days} days")
    )

fh.serve()
