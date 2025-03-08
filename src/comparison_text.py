# src/comparison_text.py
import os

def calculate_route_length(graph, route):
    """
    Rotanın toplam uzunluğunu metre cinsinden hesaplar.
    
    Args:
        graph (networkx.Graph): OSMnx grafik nesnesi.
        route (list): Rota düğümlerinin listesi.
    
    Returns:
        float: Rotanın toplam uzunluğu (metre cinsinden).
    """
    total_length = 0.0
    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]
        edge_data = graph.get_edge_data(u, v)
        if edge_data:
            total_length += edge_data[0].get('length', 0.0)  # Kenar uzunluğunu ekle
    return total_length

def calculate_travel_time_walking(route_length):
    """
    Rotanın toplam yürüme süresini hesaplar.
    
    Args:
        route_length (float): Rotanın toplam uzunluğu (metre cinsinden).
    
    Returns:
        float: Rotanın toplam yürüme süresi (saniye cinsinden).
    """
    walking_speed = 1.4  # Yürüme hızı (m/s)
    return route_length / walking_speed

def save_algorithm_comparison(two_q_result, dijkstra_result, two_q_time, dijkstra_time, graph, output_file="outputs/algorithm_comparison.txt"):
    """
    Algoritma karşılaştırma sonuçlarını bir text dosyasına kaydeder.
    
    Args:
        two_q_result (list): Two-Q algoritmasının bulduğu rota.
        dijkstra_result (list): Dijkstra algoritmasının bulduğu rota.
        two_q_time (float): Two-Q algoritmasının çalışma süresi.
        dijkstra_time (float): Dijkstra algoritmasının çalışma süresi.
        graph (networkx.Graph): OSMnx grafik nesnesi.
        output_file (str): Sonuçların kaydedileceği dosya yolu.
    """
    # outputs klasörünü kontrol et ve yoksa oluştur
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Rota uzunluklarını ve yürüme sürelerini hesapla
    two_q_length_meters = calculate_route_length(graph, two_q_result)
    dijkstra_length_meters = calculate_route_length(graph, dijkstra_result)
    two_q_travel_time_walking = calculate_travel_time_walking(two_q_length_meters)
    dijkstra_travel_time_walking = calculate_travel_time_walking(dijkstra_length_meters)

    # Karşılaştırma sonuçlarını hazırla
    comparison_text = f"""
    Algorithm Comparison Report 

    Two-Q Algorithm:
        - Route Length: {len(two_q_result)} nodes
        - Route Distance: {two_q_length_meters:.2f} meters
        - Walking Time: {two_q_travel_time_walking:.2f} seconds ({two_q_travel_time_walking / 60:.2f} minutes)
        - Execution Time: {two_q_time:.2f} seconds
        - Efficiency: {"Excellent" if two_q_time < dijkstra_time else "Needs Improvement"}

    Dijkstra Algorithm:
        - Route Length: {len(dijkstra_result)} nodes
        - Route Distance: {dijkstra_length_meters:.2f} meters
        - Walking Time: {dijkstra_travel_time_walking:.2f} seconds ({dijkstra_travel_time_walking / 60:.2f} minutes)
        - Execution Time: {dijkstra_time:.2f} seconds
        - Efficiency: {"Excellent" if dijkstra_time < two_q_time else "Needs Improvement"}

    Winner: {"Two-Q" if two_q_time < dijkstra_time else "Dijkstra"}

    Summary:
        - Two-Q is {"faster" if two_q_time < dijkstra_time else "slower"} than Dijkstra.
        - Two-Q found a {"shorter" if two_q_length_meters < dijkstra_length_meters else "longer"} route.
        - Two-Q has a {"shorter" if two_q_travel_time_walking < dijkstra_travel_time_walking else "longer"} walking time.
    """

    # Sonuçları dosyaya yaz
    with open(output_file, "w") as file:
        file.write(comparison_text)

    print(f"Algorithm comparison saved to {output_file}")