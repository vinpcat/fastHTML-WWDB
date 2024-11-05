import matplotlib
matplotlib.use("Agg")  # Use Agg backend for non-GUI environments
import matplotlib.pyplot as plt
import io
import base64
from fasthtml import common as fh
from weather_api import WeatherAPI

def generate_weather_chart(city_name, days=5):
    api = WeatherAPI()
    
    # Step 1: Fetch forecast data from the API
    print(f"Attempting to fetch forecast data for {city_name} for {days} days...")  # Debugging output
    forecast_data = api.get_forecast_by_city(city_name, days)
    
    # Step 2: Check if forecast data was successfully retrieved
    if not forecast_data:
        print("Error: Forecast data could not be retrieved.")  # Debugging output
        return fh.Div(fh.P("Error: Unable to fetch forecast data. Please try again.", cls="error-message"))
    print("Forecast data retrieved:", forecast_data)  # Debugging output

    # Step 3: Extract daily temperature data for plotting
    try:
        temperatures = [day["temp"]["day"] for day in forecast_data]
        days_range = range(1, len(temperatures) + 1)
        print("Extracted temperatures:", temperatures)  # Debugging output
    except KeyError as e:
        print(f"Error: Missing key {e} in forecast data.")  # Debugging output
        return fh.Div(fh.P("Error: Forecast data format is incorrect.", cls="error-message"))
    except TypeError as e:
        print(f"Error: Data extraction issue - {e}")  # Debugging output
        return fh.Div(fh.P("Error: Unable to process forecast data.", cls="error-message"))

    # Step 4: Plot the temperature data
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(days_range, temperatures, marker='o', linestyle='-')
        plt.title(f'Temperature Forecast for {city_name}')
        plt.xlabel('Days')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        print("Temperature chart plotted successfully.")  # Debugging output
    except Exception as e:
        print("Error during plotting:", e)  # Debugging output
        return fh.Div(fh.P("Error: Unable to generate the chart. Please try again.", cls="error-message"))
    
    # Step 5: Save plot to buffer and check encoding process
    try:
        buf = io.BytesIO()
        plt.savefig(buf, format="png")  # Save the plot as PNG to buffer
        buf.seek(0)
        plt.close()
        image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        print("Chart successfully encoded to base64.")  # Debugging output
    except Exception as e:
        print("Error during buffer encoding:", e)  # Debugging output
        return fh.Div(fh.P("Error: Unable to encode chart image. Please try again.", cls="error-message"))
    
    # Step 6: Return the encoded image as an HTML element for display
    return fh.Div(
        fh.Img(src=f"data:image/png;base64,{image_base64}", alt=f"Temperature Forecast for {city_name}")
    )
