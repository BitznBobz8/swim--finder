"""
weather_codes.py
---------------------
Converts raw values from the Open-Meteo weather API into the same
plain-English options already used in the app's Weather and Wind
Direction spinners, so auto-fetched data lines up with manual entry.
"""

# WMO weather interpretation codes (see https://open-meteo.com/en/docs)
# grouped into the app's existing Weather spinner categories.
_WEATHER_CODE_MAP = {
    0: "Bright sun",   # Clear sky
    1: "Cloudy",       # Mainly clear
    2: "Cloudy",       # Partly cloudy
    3: "Overcast",     # Overcast
    45: "Fog",
    48: "Fog",         # Depositing rime fog
    51: "Light rain",  # Drizzle: light
    53: "Light rain",  # Drizzle: moderate
    55: "Heavy rain",  # Drizzle: dense
    56: "Light rain",  # Freezing drizzle: light
    57: "Heavy rain",  # Freezing drizzle: dense
    61: "Light rain",  # Rain: slight
    63: "Heavy rain",  # Rain: moderate
    65: "Heavy rain",  # Rain: heavy
    66: "Light rain",  # Freezing rain: light
    67: "Heavy rain",  # Freezing rain: heavy
    71: "Snow",
    73: "Snow",
    75: "Snow",
    77: "Snow",
    80: "Light rain",  # Rain showers: slight
    81: "Heavy rain",  # Rain showers: moderate
    82: "Storm",       # Rain showers: violent
    85: "Snow",
    86: "Snow",
    95: "Storm",       # Thunderstorm
    96: "Storm",
    99: "Storm",
}

_COMPASS_POINTS = [
    "North", "North-East", "East", "South-East",
    "South", "South-West", "West", "North-West",
]


def weather_code_to_label(code):
    """Map an Open-Meteo WMO weather code to the app's Weather spinner text.
    Falls back to 'Overcast' for unrecognised/missing codes."""
    try:
        return _WEATHER_CODE_MAP.get(int(code), "Overcast")
    except (TypeError, ValueError):
        return "Overcast"


def degrees_to_compass(degrees):
    """Convert a wind bearing in degrees (0-360) to the app's Wind
    Direction spinner text (8-point compass). Falls back to 'West'
    for missing/malformed input."""
    try:
        degrees = float(degrees) % 360
    except (TypeError, ValueError):
        return "West"
    index = int((degrees + 22.5) // 45) % 8
    return _COMPASS_POINTS[index]
