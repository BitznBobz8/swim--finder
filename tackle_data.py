"""
species_data.py
-------------------
Behavioural and seasonal profile for each target species.
Used by the swim analysis engine (feeding zones) and the fish
predictor (season / activity based probability).
"""

SPECIES = {
    "Carp": {
        "active_months": [4, 5, 6, 7, 8, 9, 10],
        "feeding_zone": ["margins", "open water", "features"],
        "wary_of_low_pressure": True,
        "base_probability": 55,
    },
    "Bream": {
        "active_months": [4, 5, 6, 7, 8, 9, 10, 11],
        "feeding_zone": ["open water", "shelf"],
        "wary_of_low_pressure": False,
        "base_probability": 50,
    },
    "Roach": {
        "active_months": list(range(1, 13)),
        "feeding_zone": ["shelf", "margins"],
        "wary_of_low_pressure": False,
        "base_probability": 45,
    },
    "Tench": {
        "active_months": [4, 5, 6, 7, 8, 9],
        "feeding_zone": ["margins", "shelf"],
        "wary_of_low_pressure": True,
        "base_probability": 48,
    },
    "Chub": {
        "active_months": list(range(1, 13)),
        "feeding_zone": ["margins", "features", "open water"],
        "wary_of_low_pressure": False,
        "base_probability": 46,
    },
    "Barbel": {
        "active_months": [4, 5, 6, 7, 8, 9, 10],
        "feeding_zone": ["open water", "features"],
        "wary_of_low_pressure": True,
        "base_probability": 40,
    },
    "Pike": {
        "active_months": [9, 10, 11, 12, 1, 2, 3],
        "feeding_zone": ["margins", "features", "open water"],
        "wary_of_low_pressure": False,
        "base_probability": 42,
    },
    "Perch": {
        "active_months": list(range(1, 13)),
        "feeding_zone": ["margins", "features"],
        "wary_of_low_pressure": False,
        "base_probability": 44,
    },
}
