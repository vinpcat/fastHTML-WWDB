import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
from fasthtml import common as fh
from weather_api import WeatherAPI

def generate_weather_chart(city_name, forecast_days=5):
    api = WeatherAPI()
    forecast_data = api.get_5_day_forecast_tomorrow(city_name)
    
    if not forecast_data:
        print("Error: Forecast data could not be retrieved.")
        return fh.Div(fh.P("Error: Unable to fetch forecast data. Please try again.", cls="error-message"))

    days = [interval["startTime"][:10] for interval in forecast_data[:forecast_days]]
    
    # Temperature Chart
    temperatures_min = [interval["values"]["temperatureMin"] for interval in forecast_data[:forecast_days]]
    temperatures_max = [interval["values"]["temperatureMax"] for interval in forecast_data[:forecast_days]]
    temperature_chart = create_chart(days, temperatures_min, temperatures_max, city_name, "Temperature (°C)", "Temperature Forecast", "Min Temp", "Max Temp")
    
    # Humidity Chart
    humidity = [interval["values"]["humidityAvg"] for interval in forecast_data[:forecast_days]]
    humidity_chart = create_single_chart(days, humidity, city_name, "Humidity (%)", "Humidity Forecast")
    
    # Wind Gust Chart
    wind_gust = [interval["values"]["windGust"] for interval in forecast_data[:forecast_days]]
    wind_gust_chart = create_single_chart(days, wind_gust, city_name, "Wind Gust (km/h)", "Wind Gust Forecast")
    
    # Precipitation Chart
    precipitation = [interval["values"]["precipitationIntensityAvg"] for interval in forecast_data[:forecast_days]]
    precipitation_chart = create_single_chart(days, precipitation, city_name, "Precipitation (mm/h)", "Precipitation Forecast")
    
    # Arrange charts in a side-by-side 2x2 grid layout
    return fh.Div(
        fh.Div(
            fh.Div(temperature_chart, cls="chart-cell"),
            fh.Div(humidity_chart, cls="chart-cell"),
            style="display: flex; flex-direction: column; gap: 20px;"
        ),
        fh.Div(
            fh.Div(wind_gust_chart, cls="chart-cell"),
            fh.Div(precipitation_chart, cls="chart-cell"),
            style="display: flex; flex-direction: column; gap: 20px;"
        ),
        style="display: flex; justify-content: center; gap: 20px;"
    )

def create_chart(days, data_min, data_max, city_name, ylabel, title, label_min, label_max):
    """Helper function to generate a temperature chart with min and max values."""
    plt.figure(figsize=(8, 4))  # Adjusted figure size for grid layout
    plt.plot(days, data_min, marker='o', linestyle='-', color='blue', label=label_min)
    plt.plot(days, data_max, marker='o', linestyle='-', color='red', label=label_max)
    plt.title(f'{title} for {city_name}')
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    return encode_chart_to_base64()

def create_single_chart(days, data, city_name, ylabel, title):
    """Helper function to generate a single line chart."""
    plt.figure(figsize=(8, 4))  # Adjusted figure size for grid layout
    plt.plot(days, data, marker='o', linestyle='-', color='green')
    plt.title(f'{title} for {city_name}')
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.grid(True)
    return encode_chart_to_base64()

def encode_chart_to_base64():
    """Encodes the chart to a base64 string for HTML rendering."""
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return fh.Div(
        fh.Img(src=f"data:image/png;base64,{image_base64}", alt="Forecast Chart")
    )
