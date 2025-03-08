# src/main.py
import os
import time
import osmnx as ox
from shapely.geometry import Point
from data_processing import load_osm_data, project_graph, get_convex_hull
from shortest_path_twoq import two_q
from shortest_path_dijkstra import dijkstra
from visualization import visualize_dual_route
from utils.helpers import get_osm_file_path, find_nearest_node, print_route_info
from comparison_text import save_algorithm_comparison  # Yeni eklenen import

def main():
    # OSM dosyasının yolunu al
    osm_file = get_osm_file_path()

    # OSM verilerini yükle ve grafik oluştur
    muc_graph = load_osm_data(osm_file)

    # Grafiği projeksiyon yap
    muc_graph_proj = project_graph(muc_graph)

    # Düğümleri ve kenarları al
    nodes_proj, edges_proj = ox.graph_to_gdfs(muc_graph_proj, nodes=True, edges=True)

    # Convex hull ve centroid hesapla
    convex_hull = get_convex_hull(edges_proj)
    centroid = convex_hull.centroid

    # Kaynak ve hedef düğümleri belirle
    source_point = Point(centroid.x, centroid.y)  # Centroid kaynak düğüm olacak
    target_point = nodes_proj.loc[nodes_proj['x'] == nodes_proj['x'].min(), 'geometry'].values[0]  # En batıdaki düğüm

    # Kaynak ve hedef düğümleri bul
    source_node = find_nearest_node(muc_graph_proj, source_point)
    target_node = find_nearest_node(muc_graph_proj, target_point)


    # Two-Q algoritması ile en kısa yolu hesapla ve süreyi ölç
    start_time = time.time()
    shortest_path_two_q = two_q(muc_graph_proj, source_node, target_node)
    two_q_time = time.time() - start_time

     # Dijkstra algoritması ile en kısa yolu hesapla ve süreyi ölç
    start_time = time.time()
    shortest_path_dijkstra = dijkstra(muc_graph_proj, source_node, target_node)
    dijkstra_time = time.time() - start_time


    # Eğer en kısa yol bulunamazsa
    if not shortest_path_two_q or not shortest_path_dijkstra:
        print("Hedef düğüme ulaşılamadı!")
    else:
        print_route_info(shortest_path_two_q, "Two-Q")
        print_route_info(shortest_path_dijkstra, "Dijkstra")

        # Algoritma karşılaştırma sonuçlarını kaydet
        save_algorithm_comparison(shortest_path_two_q, shortest_path_dijkstra, two_q_time, dijkstra_time, muc_graph_proj)

        route_nodes_two_q = nodes_proj.loc[shortest_path_two_q]
        route_edges_two_q = edges_proj.loc[shortest_path_two_q]

        route_nodes_dijkstra = nodes_proj.loc[shortest_path_dijkstra]
        route_edges_dijkstra = edges_proj.loc[shortest_path_dijkstra]

        # Görselleştirme yap ve HTML olarak kaydet
        visualize_dual_route(
        route_edges_two_q, route_nodes_two_q,
        route_edges_dijkstra, route_nodes_dijkstra,
        edges_proj, nodes_proj,
        source_node, target_node,
        output_html="outputs/dual_path_visualization.html"
        )
if __name__ == "__main__":
    main()