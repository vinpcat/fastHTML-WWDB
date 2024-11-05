import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
from fasthtml import common as fh
from weather_api import WeatherAPI

def generate_weather_chart(city_name, forecast_days=5, use_tomorrow_api=True):
    api = WeatherAPI()
    
    if use_tomorrow_api:
        print(f"Fetching {forecast_days}-day forecast from Tomorrow.io for {city_name}...")  # Debug output
        forecast_data = api.get_7_day_forecast_tomorrow(city_name)
        if not forecast_data:
            print("Error: Forecast data could not be retrieved from Tomorrow.io.")
            return fh.Div(fh.P("Error: Unable to fetch forecast data. Please try again.", cls="error-message"))

        # Extract daily minimum and maximum temperatures from Tomorrow.io forecast, limited to forecast_days
        try:
            days = [interval["startTime"][:10] for interval in forecast_data[:forecast_days]]  # Extract date in YYYY-MM-DD format
            temperatures_min = [interval["values"]["temperatureMin"] for interval in forecast_data[:forecast_days]]
            temperatures_max = [interval["values"]["temperatureMax"] for interval in forecast_data[:forecast_days]]
            print("Extracted dates:", days)  # Debugging output
            print("Min temperatures:", temperatures_min)  # Debugging output
            print("Max temperatures:", temperatures_max)  # Debugging output
        except KeyError as e:
            print(f"Error: Missing key {e} in Tomorrow.io forecast data.")
            return fh.Div(fh.P("Error: Forecast data format is incorrect.", cls="error-message"))
    else:
        print("Using OpenWeatherMap as a fallback.")
        return fh.Div(fh.P("OpenWeatherMap fallback not implemented for forecast.", cls="error-message"))
    
    # Plot the min and max temperatures for the forecast
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(days, temperatures_min, marker='o', linestyle='-', color='blue', label='Min Temp')
        plt.plot(days, temperatures_max, marker='o', linestyle='-', color='red', label='Max Temp')
        plt.title(f'{forecast_days}-Day Temperature Forecast for {city_name}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True)
    except Exception as e:
        print("Error during plotting:", e)
        return fh.Div(fh.P("Error: Unable to generate the chart. Please try again.", cls="error-message"))
    
    # Save plot to buffer and encode as a base64 string
    try:
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()
        image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        print("Chart successfully encoded to base64.")  # Debugging output
    except Exception as e:
        print("Error during buffer encoding:", e)
        return fh.Div(fh.P("Error: Unable to encode chart image. Please try again.", cls="error-message"))
    
    # Return the encoded image as an HTML element for display
    return fh.Div(
        fh.Img(src=f"data:image/png;base64,{image_base64}", alt=f"{forecast_days}-Day Temperature Forecast for {city_name}")
    )
