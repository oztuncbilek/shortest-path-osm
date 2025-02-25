import os
import osmnx as ox
from shapely.geometry import Point

def get_project_root():
    """Projenin kök dizinini dinamik olarak bulur."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # helpers.py'nin bulunduğu dizin
    return os.path.abspath(os.path.join(current_dir, "..", ".."))  # Proje kök dizinine çık

def get_osm_file_path():
    """OSM dosyasının tam yolunu döner."""
    project_root = get_project_root()
    data_dir = os.path.join(project_root, "data")
    return os.path.join(data_dir, "munich_center.osm")

def calculate_distance(point1, point2):
    """İki nokta arasındaki mesafeyi hesaplar."""
    return point1.distance(point2)

def find_nearest_node(graph, point):
    """Bir noktaya en yakın düğümü bulur."""
    return ox.distance.nearest_nodes(graph, X=point.x, Y=point.y)

def print_route_info(route):
    """Rota bilgilerini terminalde yazdırır."""
    print(f"Shortest path: {route}")