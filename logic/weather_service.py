"""
weather_service.py
---------------------
Fetches current weather, wind, pressure, and sunrise/sunset from the
free Open-Meteo API (no API key required). Converts raw WMO codes
and wind degrees into the app's field format.
"""

import requests
from datetime import datetime

from data.weather_codes import weather_code_to_label, degrees_to_compass


def fetch_weather(lat, lon):
    """
    Fetches current weather data for the given GPS coordinates from Open-Meteo.
    
    lat, lon: float coordinates
    returns: dict with keys weather, wind_dir, wind_speed_mph, pressure_hpa,
             sunrise, sunset (all already converted to app field format)
    raises: Exception if the API call fails or returns invalid data
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "weather_code,wind_speed_10m,wind_direction_10m,pressure_msl",
        "timezone": "auto",
    }
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    current = data.get("current", {})
    
    # Extract and convert weather code
    weather_code = current.get("weather_code", 3)
    weather_label = weather_code_to_label(weather_code)
    
    # Extract and convert wind direction
    wind_degrees = current.get("wind_direction_10m", 270)
    wind_dir = degrees_to_compass(wind_degrees)
    
    # Extract wind speed (convert km/h to mph)
    wind_speed_kmh = current.get("wind_speed_10m", 0)
    wind_speed_mph = round(wind_speed_kmh / 1.60934, 1) if wind_speed_kmh else 0
    
    # Extract pressure
    pressure_hpa = current.get("pressure_msl", 1013)
    if pressure_hpa:
        pressure_hpa = round(pressure_hpa)
    
    # Fetch sunrise/sunset (requires a separate call)
    sunrise, sunset = _fetch_sun_times(lat, lon)
    
    return {
        "weather": weather_label,
        "wind_dir": wind_dir,
        "wind_speed_mph": wind_speed_mph,
        "pressure_hpa": pressure_hpa,
        "sunrise": sunrise,
        "sunset": sunset,
    }


def _fetch_sun_times(lat, lon):
    """Fetch sunrise and sunset times from Open-Meteo."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "sunrise,sunset",
            "timezone": "auto",
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        daily = data.get("daily", {})
        sunrise_list = daily.get("sunrise", [])
        sunset_list = daily.get("sunset", [])
        
        if sunrise_list and sunset_list:
            # Parse ISO format and extract time
            sunrise_str = sunrise_list[0]  # e.g. "2025-07-27T05:30"
            sunset_str = sunset_list[0]
            
            sunrise_time = sunrise_str.split("T")[1] if "T" in sunrise_str else "05:30"
            sunset_time = sunset_str.split("T")[1] if "T" in sunset_str else "20:30"
            
            return sunrise_time, sunset_time
    except Exception:
        pass
    
    return "06:00", "20:00"  # Fallback
