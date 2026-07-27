"""
fish_predictor.py
---------------------
Estimates the probability of catching each species given the
conditions entered by the angler. This is a heuristic, rules-based
model in Version 1. Version 4 will refine it using the angler's own
catch history stored in SQLite (see project roadmap).
"""

from data.species_data import SPECIES


def predict_species(inputs):
    """
    inputs: dict from the input screen (must include month_num, species,
            weather, pressure_hpa, time_of_day, wind_speed_mph)
    returns: dict of {species_name: probability_percent}
    """
    month = inputs["month_num"]
    results = {}

    for name, profile in SPECIES.items():
        prob = profile["base_probability"]

        # Season / active months
        if month in profile["active_months"]:
            prob += 20
        else:
            prob -= 25

        # Bonus for being the angler's actual target species
        if name == inputs["species"]:
            prob += 15

        # Weather effects
        if inputs["weather"] in ("Overcast", "Light rain", "Cloudy"):
            prob += 4
        elif inputs["weather"] == "Bright sun":
            prob -= 8
        elif inputs["weather"] in ("Storm", "Snow"):
            prob -= 18

        # Pressure - falling/low pressure can switch off wary species
        if profile["wary_of_low_pressure"] and inputs["pressure_hpa"] < 1000:
            prob -= 14

        # Time of day - dawn/dusk favour most species
        if inputs["time_of_day"] in ("Dawn", "Dusk"):
            prob += 5
        elif inputs["time_of_day"] == "Night" and name in ("Bream", "Tench", "Pike"):
            prob += 4

        # A gentle breeze often improves feeding activity
        if 3 <= inputs["wind_speed_mph"] <= 12:
            prob += 3

        results[name] = max(5, min(95, round(prob)))

    return results
