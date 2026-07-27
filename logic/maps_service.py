"""
maps_service.py
---------------------
Google Maps integration for selecting fishing locations.
Provides URL generation for opening Google Maps in the browser
or initiating map picker on Android.
"""

import webbrowser
from urllib.parse import urlencode


def open_google_maps():
    """
    Opens Google Maps in the default browser so the user can
    search for and select their fishing location. Returns the
    coordinates if possible (requires manual entry or re-reading
    from browser in current version).
    """
    maps_url = "https://maps.google.com"
    webbrowser.open(maps_url)


def open_maps_search(query):
    """
    Opens Google Maps with a search query (e.g., "fishing venues near me").
    
    query: str, search term
    """
    params = {"q": query}
    maps_url = f"https://maps.google.com/maps?{urlencode(params)}"
    webbrowser.open(maps_url)


def open_maps_at_coordinates(lat, lon):
    """
    Opens Google Maps centered on the given coordinates.
    Useful for previewing the location the user typed in.
    
    lat, lon: float coordinates
    """
    maps_url = f"https://maps.google.com/maps?q={lat},{lon}&z=15"
    webbrowser.open(maps_url)


def generate_maps_url(lat, lon, zoom=13):
    """
    Generates a Google Maps URL for the given coordinates.
    Can be used to create a clickable link or share the location.
    
    lat, lon: float coordinates
    zoom: int, zoom level (1-21)
    returns: str, full Google Maps URL
    """
    return f"https://maps.google.com/maps?q={lat},{lon}&z={zoom}"
