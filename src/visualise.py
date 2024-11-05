import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
from fasthtml import common as fh
from weather_api import WeatherAPI

def generate_weather_chart(city_name, days=5):
    api = WeatherAPI()
    forecast_data = api.get_forecast_by_city(city_name, days)
    
    # Check if forecast data was retrieved successfully
    if not forecast_data:
        print("Error: Forecast data could not be retrieved.")
        return fh.Div(fh.P("Error: Unable to fetch forecast data. Please try again.", cls="error-message"))

    # Extract temperature data for the specified forecast days
    try:
        temperatures = [day["temp"]["day"] for day in forecast_data]
        days_range = range(1, len(temperatures) + 1)
    except KeyError as e:
        print(f"Error: Unexpected data format - missing key {e}")
        return fh.Div(fh.P("Error: Forecast data format is incorrect.", cls="error-message"))
    
    # Plot the temperature forecast
    plt.figure(figsize=(10, 5))
    plt.plot(days_range, temperatures, marker='o', linestyle='-')
    plt.title(f'Temperature Forecast for {city_name}')
    plt.xlabel('Days')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    
    # Save plot to a buffer and encode as a base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    # Return the encoded image as an HTML element
    return fh.Div(
        fh.Img(src=f"data:image/png;base64,{image_base64}", alt=f"Temperature Forecast for {city_name}")
    )
