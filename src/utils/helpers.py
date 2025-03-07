import os
import osmnx as ox
from shapely.geometry import Point

def get_project_root():
    """Projenin kök dizinini dinamik olarak bulur."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    return os.path.abspath(os.path.join(current_dir, "..", ".."))  

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

def print_route_info(route, algorithm_name):
    """Rota bilgilerini terminalde yazdırır.
    
    Args:
        route (list): En kısa yolun düğüm listesi.
        algorithm_name (str): Algoritmanın adı (örneğin, "Dijkstra" veya "Two-Q").
    """
    print(f"{algorithm_name} Algoritması ile Bulunan Rota:")
    print(f"Rota Uzunluğu: {len(route)} düğüm")
    print(f"Rota: {route}")