"""
tackle_engine.py
--------------------
Builds a tackle recommendation for the chosen species, adjusted for
casting distance and water type.
"""

from data.tackle_data import TACKLE_BASE


def _format_range(value_range, unit=""):
    low, high = value_range
    if low == high:
        return f"{low}{unit}"
    return f"{low}-{high}{unit}"


def recommend_tackle(inputs, swim_analysis):
    """
    inputs: dict from the input screen (must include 'species', 'water_type')
    swim_analysis: dict returned by analyse_swim (must include 'casting_distance_m')
    returns: dict describing the recommended tackle setup
    """
    species = inputs["species"]
    base = TACKLE_BASE[species]
    distance = swim_analysis["casting_distance_m"]

    feeder_low, feeder_high = base["feeder_weight_g"]
    lead_low, lead_high = base["lead_size_oz"]

    # Scale feeder/lead weight up for longer range work
    if distance > 40 and species != "Pike":
        feeder_low = int(feeder_low * 1.3)
        feeder_high = int(feeder_high * 1.3)
        lead_low = round(lead_low * 1.3, 1)
        lead_high = round(lead_high * 1.3, 1)

    # Float vs feeder decision
    if species == "Pike":
        method = base["rig_choice"]
    elif distance <= 15 and inputs["water_type"] in ("Canal", "Lake"):
        style = "waggler" if distance > 8 else "pole/whip"
        method = f"Float ({style}) preferred at this range, feeder as backup"
    else:
        method = base["rig_choice"]

    if species == "Pike":
        hooklength = "Wire trace (in place of a standard hooklength)"
        feeder_weight = "N/A"
        lead_size = f"{lead_low}-{lead_high}oz"
    else:
        hooklength = _format_range(base["hooklength_lb"], "lb")
        feeder_weight = f"{feeder_low}-{feeder_high}g"
        lead_size = f"{lead_low}-{lead_high}oz"

    return {
        "rod_type": base["rod_type"],
        "rod_length_ft": base["rod_length_ft"],
        "reel_size": base["reel_size"],
        "mainline": _format_range(base["mainline_lb"], "lb"),
        "hooklength": hooklength,
        "hook_size": base["hook_size"],
        "method": method,
        "feeder_weight": feeder_weight,
        "lead_size": lead_size,
        "bait": base["bait"],
        "groundbait": base["groundbait"],
        "loose_feed": base["loose_feed"],
    }
