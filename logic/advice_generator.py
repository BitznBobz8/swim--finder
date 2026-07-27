"""
advice_generator.py
-----------------------
Builds the short natural-language advice paragraph that ties together
the swim analysis, tackle recommendation and fish predictions into an
explanation for the angler: why the recommendation was made, where to
cast, how often to feed, and how to adjust if the weather changes.
"""


def generate_advice(inputs, swim, tackle, predictions):
    species = inputs["species"]
    top_species = max(predictions, key=predictions.get)

    zone_phrases = {
        "Margins": "the margin area",
        "Shelf": "the shelfline",
        "Open water": "open water",
    }
    zone = zone_phrases.get(swim["zone_recommendation"], swim["zone_recommendation"].lower())
    distance = swim["casting_distance_m"]
    depth = swim["depth_m"]

    parts = []

    parts.append(
        f"Based on the {inputs['water_type'].lower()} venue, {inputs['month']} conditions "
        f"and an estimated depth of around {depth}m, {zone} looks the most productive "
        f"area today, roughly {distance}m out."
    )

    if predictions[species] >= 60:
        parts.append(
            f"Conditions look favourable for {species}, with feeding activity likely to be "
            f"strongest around {inputs['time_of_day'].lower()}."
        )
    else:
        parts.append(
            f"{species} may be harder work in these conditions; {top_species} shows the "
            f"strongest probability today, so keep an open mind if bites are slow."
        )

    if tackle["loose_feed"] not in ("Not applicable",):
        parts.append(
            f"Introduce {tackle['loose_feed'].lower()} little and often rather than one large "
            f"application, feeding every 10-15 minutes to draw fish in without overfeeding."
        )
    else:
        parts.append(
            "Work the swim methodically, covering likely holding areas rather than "
            "sitting static in one spot for too long."
        )

    if inputs["weather"] == "Bright sun":
        parts.append(
            "If the sun stays bright, consider dropping to a lighter hooklength and easing "
            "back on feed, as fish can become more cautious in clear, bright conditions."
        )
    elif inputs["pressure_hpa"] < 1000:
        parts.append(
            "With low pressure in play, expect fishing to be more challenging; a more "
            "searching, mobile approach may out-fish sitting in one swim all day."
        )
    elif inputs["wind_speed_mph"] > 15:
        parts.append(
            "If the wind picks up further, favour a heavier feeder or lead to maintain "
            "presentation, and consider moving onto the sheltered or downwind bank."
        )
    else:
        parts.append(
            "Keep an eye on the weather; if conditions change, be ready to adjust feed "
            "frequency and hookbait size accordingly."
        )

    return " ".join(parts)
