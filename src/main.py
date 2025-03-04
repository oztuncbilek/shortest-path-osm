import os
import osmnx as ox
from shapely.geometry import Point
from data_processing import load_osm_data, project_graph, get_convex_hull
from shortest_path import two_q
from visualization import visualize_route
from utils.helpers import get_osm_file_path, find_nearest_node, print_route_info

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

    # Two-Q algoritması ile en kısa yolu hesapla
    shortest_path = two_q(muc_graph_proj, source_node, target_node)

    # Eğer en kısa yol bulunamazsa
    if not shortest_path:
        print("Hedef düğüme ulaşılamadı!")
    else:
        print_route_info(shortest_path)

        route_nodes = nodes_proj.loc[shortest_path]
        route_edges = edges_proj.loc[shortest_path]

        '''
        # GeoJSON olarak export etme, opsyonel
        print("Sonuclar GeoJSON formatinda kaydediliyor.")
        route_edges.to_file("outputs/route_edges.geojson", driver="GeoJSON")
        route_nodes.to_file("outputs/route_nodes.geojson", driver="GeoJSON")
        edges_proj.to_file("outputs/edges_proj.geojson", driver="GeoJSON")
        nodes_proj.to_file("outputs/nodes_proj.geojson", driver="GeoJSON")
        '''

        # Görselleştirme yap ve HTML olarak kaydet
        visualize_route(route_edges, route_nodes, edges_proj, nodes_proj, source_node, target_node, output_html="outputs/shortest_path_visualization.html")

if __name__ == "__main__":
    main()