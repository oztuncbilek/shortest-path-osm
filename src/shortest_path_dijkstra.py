import osmnx as ox
import heapq
from tqdm import tqdm

def dijkstra(graph, source, target):
    nodes_proj, edges_proj = ox.graph_to_gdfs(graph, nodes=True, edges=True)
    labels = {node: float('inf') for node in nodes_proj.index}
    labels[source] = 0
    queue = [(0, source)]
    visited = set()

    # Toplam düğüm sayısını al (ilerleme çubuğu için)
    total_nodes = len(nodes_proj)

    # tqdm ile ilerleme çubuğu oluştur
    with tqdm(total=total_nodes, desc="Dijkstra Algoritması Çalışıyor", unit="it", unit_scale=True) as pbar:
        while queue:
            current_dist, current_node = heapq.heappop(queue)

            if current_node == target:
                print(f"\nHedef düğüme ulaşıldı: {current_node}")
                pbar.update(total_nodes - pbar.n)  # Progress bar'ı tamamla
                break

            if current_node in visited:
                continue

            visited.add(current_node)

            # İlerleme çubuğunu güncelle
            pbar.update(1)

            for neighbor in graph.neighbors(current_node):
                edge_data = graph.get_edge_data(current_node, neighbor)
                if edge_data:
                    weight = edge_data[0].get('length', 1)
                    distance = current_dist + weight

                    if distance < labels[neighbor]:
                        labels[neighbor] = distance
                        heapq.heappush(queue, (distance, neighbor))

    shortest_path = []
    current = target
    while current != source:
        shortest_path.append(current)
        current = min((node for node in graph.neighbors(current)), key=lambda x: labels[x])
    shortest_path.append(source)
    shortest_path.reverse()

    return shortest_path