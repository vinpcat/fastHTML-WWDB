from fasthtml import common as fh

def validate_forecast_days(forecast_days):
    try:
        forecast_days = int(forecast_days)
        if forecast_days < 1 or forecast_days > 7:
            return fh.Div(
                fh.P("Error: Please enter a number between 1 and 7 for forecast days.", cls="error-message")
            )
        return None
    except ValueError:
        return fh.Div(
            fh.P("Error: Invalid input. Please enter a valid number for forecast days.", cls="error-message")
        )
