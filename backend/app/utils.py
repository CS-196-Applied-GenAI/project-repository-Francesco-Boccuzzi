"""
Utility functions for distance calculations and geospatial operations.
"""

import math
from typing import Tuple


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth using the Haversine formula.
    
    Args:
        lat1: Latitude of point 1 in degrees
        lon1: Longitude of point 1 in degrees
        lat2: Latitude of point 2 in degrees
        lon2: Longitude of point 2 in degrees
    
    Returns:
        Distance in kilometers
    
    Reference: https://en.wikipedia.org/wiki/Haversine_formula
    """
    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = EARTH_RADIUS_KM * c
    return distance


def filter_stations_by_radius(
    stations: list,
    center_lat: float,
    center_lon: float,
    radius_km: float
) -> list:
    """
    Filter stations that fall within a given radius from a center point.
    
    Args:
        stations: List of station ORM objects
        center_lat: Center latitude
        center_lon: Center longitude
        radius_km: Radius in kilometers
    
    Returns:
        List of station objects with distance calculated (as 'distance_km' attribute)
    """
    filtered_stations = []
    
    for station in stations:
        distance = haversine_distance(center_lat, center_lon, station.latitude, station.longitude)
        
        if distance <= radius_km:
            # Attach distance to station object for response building
            station.distance_km = round(distance, 2)
            filtered_stations.append(station)
    
    # Sort by distance (closest first)
    filtered_stations.sort(key=lambda s: s.distance_km)
    
    return filtered_stations
