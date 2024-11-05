from fasthtml import common as fh

def validate_forecast_days(forecast_days):
    """
    Validates the forecast_days input. Returns an error message if invalid, or None if valid.
    """
    try:
        # Convert forecast_days to an integer and check the range
        forecast_days = int(forecast_days)
        if forecast_days < 1 or forecast_days > 7:
            return fh.Div(
                fh.P("Error: Please enter a number between 1 and 7 for forecast days.", cls="error-message")
            )
        # If valid, return None (no error)
        return None
    except ValueError:
        # Return error message if conversion to integer fails
        return fh.Div(
            fh.P("Error: Invalid input. Please enter a valid number for forecast days.", cls="error-message")
        )
