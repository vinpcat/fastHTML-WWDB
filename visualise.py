import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def generate_weather_chart(days):
    temperatures = [np.random.randint(15, 30) for _ in range(days)]
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, days + 1), temperatures, marker='o')
    plt.title('Temperature Forecast')
    plt.xlabel('Days')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)

    # Save plot to a buffer and encode it as a base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f'<img src="data:image/png;base64,{image_base64}" alt="Temperature Forecast">'
