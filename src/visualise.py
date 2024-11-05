import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
from fasthtml import common as fh
from weather_api import WeatherAPI

def generate_weather_chart(city_name, days=5):
    api = WeatherAPI()
    
    print(f"Fetching forecast data for {city_name} for {days} days...")  # Debug output
    forecast_data = api.get_forecast_by_city(city_name, days)
    
    if not forecast_data:
        print("Error: Forecast data could not be retrieved.")
        return fh.Div(fh.P("Error: Unable to fetch forecast data. Please try again.", cls="error-message"))
    print("Forecast data retrieved:", forecast_data)

    try:
        temperatures = [day["temp"]["day"] for day in forecast_data]
        days_range = range(1, len(temperatures) + 1)
        print("Temperatures extracted for chart:", temperatures)
    except KeyError as e:
        print(f"Error: Missing key {e} in forecast data.")
        return fh.Div(fh.P("Error: Forecast data format is incorrect.", cls="error-message"))

    try:
        plt.figure(figsize=(10, 5))
        plt.plot(days_range, temperatures, marker='o', linestyle='-')
        plt.title(f'Temperature Forecast for {city_name}')
        plt.xlabel('Days')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
    except Exception as e:
        print("Error during plotting:", e)
        return fh.Div(fh.P("Error: Unable to generate the chart. Please try again.", cls="error-message"))
    
    try:
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        print("Chart successfully encoded to base64.")
    except Exception as e:
        print("Error during buffer encoding:", e)
        return fh.Div(fh.P("Error: Unable to encode chart image. Please try again.", cls="error-message"))
    
    return fh.Div(
        fh.Img(src=f"data:image/png;base64,{image_base64}", alt=f"Temperature Forecast for {city_name}")
    )
