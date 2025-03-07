# main.py
import os
import osmnx as ox
from shapely.geometry import Point
from data_processing import load_osm_data, project_graph, get_convex_hull
from shortest_path_twoq import two_q  # Two-Q algoritması
from shortest_path_dijkstra import dijkstra  # Dijkstra algoritması
from visualization import visualize_dual_route
from utils.helpers import get_osm_file_path, find_nearest_node, print_route_info

def main():
    osm_file = get_osm_file_path()
    muc_graph = load_osm_data(osm_file)
    muc_graph_proj = project_graph(muc_graph)
    nodes_proj, edges_proj = ox.graph_to_gdfs(muc_graph_proj, nodes=True, edges=True)
    convex_hull = get_convex_hull(edges_proj)
    centroid = convex_hull.centroid

    source_point = Point(centroid.x, centroid.y)
    target_point = nodes_proj.loc[nodes_proj['x'] == nodes_proj['x'].min(), 'geometry'].values[0]

    source_node = find_nearest_node(muc_graph_proj, source_point)
    target_node = find_nearest_node(muc_graph_proj, target_point)

    shortest_path_dijkstra = dijkstra(muc_graph_proj, source_node, target_node)
    shortest_path_two_q = two_q(muc_graph_proj, source_node, target_node)

    if not shortest_path_dijkstra or not shortest_path_two_q:
        print("Hedef düğüme ulaşılamadı!")
    else:
        print_route_info(shortest_path_dijkstra, "Dijkstra")
        print_route_info(shortest_path_two_q, "Two-Q")

        route_nodes_dijkstra = nodes_proj.loc[shortest_path_dijkstra]
        route_edges_dijkstra = edges_proj.loc[shortest_path_dijkstra]

        route_nodes_two_q = nodes_proj.loc[shortest_path_two_q]
        route_edges_two_q = edges_proj.loc[shortest_path_two_q]

        visualize_dual_route(
        route_edges_two_q, route_nodes_two_q,
        route_edges_dijkstra, route_nodes_dijkstra,
        edges_proj, nodes_proj,
        source_node, target_node,
        output_html="outputs/dual_path_visualization.html"
        )
if __name__ == "__main__":
    main()