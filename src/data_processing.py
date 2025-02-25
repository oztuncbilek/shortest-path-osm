import osmnx as ox
import os

def load_osm_data(osm_file):
    if not os.path.exists(osm_file):
        raise FileNotFoundError(f"OSM file not found: {osm_file}")
    print("OSM verileri yükleniyor...")
    return ox.graph_from_xml(osm_file, simplify=True, retain_all=False)

def project_graph(graph):
    print("Grafik projeksiyon yapılıyor...")
    return ox.project_graph(graph)

def get_convex_hull(edges_proj):
    return edges_proj.unary_union.convex_hull