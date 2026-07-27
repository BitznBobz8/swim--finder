"""
water_data.py
-----------------
Baseline physical characteristics for each water type.

These values are the starting point for the Swim Analysis engine,
before conditions (species, weather, wind) adjust them. In Version 1
there is no real bathymetric/mapping data available, so these are
realistic coarse-fishing rules of thumb. Version 5 will replace/augment
this with real depth and mapping data where available.
"""

WATER_TYPES = {
    "Lake": {
        "depth_range_m": (1.5, 4.5),
        "casting_distance_m": (15, 60),
        "snag_risk_base": "Medium",
        "description": "Lakes typically feature a marginal shelf, open "
                        "water in the middle, and features such as "
                        "islands or overhanging trees.",
    },
    "Canal": {
        "depth_range_m": (1.0, 2.2),
        "casting_distance_m": (5, 25),
        "snag_risk_base": "Medium",
        "description": "Canals are narrow, with near and far shelves "
                        "either side of a deeper central channel kept "
                        "clear for boat traffic.",
    },
    "River": {
        "depth_range_m": (0.8, 3.5),
        "casting_distance_m": (10, 40),
        "snag_risk_base": "High",
        "description": "Rivers have flow-dependent depth, crease lines "
                        "and eddies that concentrate feeding fish.",
    },
    "Reservoir": {
        "depth_range_m": (2.5, 9.0),
        "casting_distance_m": (30, 90),
        "snag_risk_base": "Low",
        "description": "Reservoirs are typically deep, open venues with "
                        "fewer snags, favouring longer-range tactics.",
    },
}
