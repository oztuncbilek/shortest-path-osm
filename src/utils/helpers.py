import os
import osmnx as ox
from shapely.geometry import Point

def get_project_root():
    """Finds the root of the project dynamically"""
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    return os.path.abspath(os.path.join(current_dir, "..", ".."))  

def get_osm_file_path():
    """OSM  file path"""
    project_root = get_project_root()
    data_dir = os.path.join(project_root, "data")
    return os.path.join(data_dir, "munich_center.osm")

def calculate_distance(point1, point2):
    """Calculates the distance between 2 points."""
    return point1.distance(point2)

def find_nearest_node(graph, point):
    """Finds the closest node."""
    return ox.distance.nearest_nodes(graph, X=point.x, Y=point.y)

def print_route_info(route, algorithm_name):
    """Prints out the route information to the terminal.
    
    Args:
        route (list): List of nodes representing the shortest path.
        algorithm_name (str): Name of the algorithm (e.g., "Dijkstra" or "Two-Q").
    """
    print(f"Route found by {algorithm_name} Algorithm:")
    print(f"Route Length: {len(route)} nodes")
    print(f"Route: {route}")