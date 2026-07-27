"""
swim_analysis.py
--------------------
Core swim analysis engine. Produces an estimate of the physical
characteristics of the swim (depth, casting distance, feeding areas,
snag risk, confidence) based on location, water type, target species
and prevailing conditions.

Note: Version 1 has no access to real bathymetric or mapping data, so
estimates come from a rules-based model. The model is *seeded* on the
GPS coordinates + conditions, so the same inputs always return the
same analysis rather than a different random answer every time.
Version 5 will introduce real mapping/depth data to replace this.
"""

import hashlib
import random

from data.water_data import WATER_TYPES
from data.species_data import SPECIES


def _seeded_random(inputs):
    """Build a reproducible Random instance from the swim inputs, so a
    given location + conditions always produce the same analysis."""
    seed_string = (
        f"{inputs['lat']}-{inputs['lon']}-{inputs['water_type']}-"
        f"{inputs['species']}-{inputs['month']}"
    )
    seed = int(hashlib.md5(seed_string.encode()).hexdigest(), 16) % (10 ** 8)
    return random.Random(seed)


def analyse_swim(inputs):
    """
    inputs: dict with keys lat, lon, water_type, species, time_of_day,
            month, month_num, weather, wind_dir, wind_speed_mph,
            pressure_hpa
    returns: dict describing the physical swim analysis
    """
    rng = _seeded_random(inputs)
    water = WATER_TYPES[inputs["water_type"]]
    species_zones = SPECIES[inputs["species"]]["feeding_zone"]

    # --- Estimated water depth ---
    low, high = water["depth_range_m"]
    depth_m = round(rng.uniform(low, high), 1)

    # --- Suggested casting distance ---
    cast_low, cast_high = water["casting_distance_m"]
    if "margins" in species_zones and "open water" not in species_zones:
        # Margin-loving species (e.g. roach/tench) are fished shorter
        cast_high = cast_low + (cast_high - cast_low) * 0.4
    casting_distance_m = rng.randint(int(cast_low), max(int(cast_low) + 1, int(cast_high)))

    # --- Likely feeding areas ---
    feeding_areas = []
    if "margins" in species_zones:
        feeding_areas.append("tight to the near margins, especially close to cover")
    if "shelf" in species_zones:
        feeding_areas.append("along the marginal shelf where the bottom first drops away")
    if "open water" in species_zones:
        feeding_areas.append("open water over the deeper central area")
    if "features" in species_zones:
        feeding_areas.append("near visible features such as snags, reeds or overhanging cover")
    if inputs["wind_speed_mph"] and inputs["wind_speed_mph"] > 5:
        feeding_areas.append(
            f"the {inputs['wind_dir']} bank, where the breeze is pushing food and oxygen into the swim"
        )

    # --- Margin / shelf / open water recommendation ---
    if "margins" in species_zones and rng.random() > 0.4:
        zone_recommendation = "Margins"
    elif "shelf" in species_zones and rng.random() > 0.35:
        zone_recommendation = "Shelf"
    else:
        zone_recommendation = "Open water"

    # --- Snag risk ---
    snag_base = water["snag_risk_base"]
    if "features" in species_zones and rng.random() > 0.5:
        snag_risk = "High" if snag_base != "Low" else "Medium"
    else:
        snag_risk = snag_base

    # --- Confidence score ---
    # Rises with settled weather/pressure, falls with unstable conditions.
    confidence = 70
    calm_weather = {"Overcast", "Light rain", "Cloudy"}
    poor_weather = {"Bright sun", "Heavy rain", "Storm", "Snow"}
    if inputs["weather"] in calm_weather:
        confidence += 10
    elif inputs["weather"] in poor_weather:
        confidence -= 15

    pressure = inputs["pressure_hpa"]
    if 1008 <= pressure <= 1022:
        confidence += 8
    elif pressure < 995 or pressure > 1035:
        confidence -= 10

    confidence += rng.randint(-5, 5)
    confidence_pct = max(30, min(95, confidence))

    return {
        "depth_m": depth_m,
        "casting_distance_m": casting_distance_m,
        "feeding_areas": feeding_areas,
        "zone_recommendation": zone_recommendation,
        "snag_risk": snag_risk,
        "confidence_pct": confidence_pct,
    }
