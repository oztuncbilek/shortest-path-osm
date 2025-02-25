import osmnx as ox
from enum import Enum
from tqdm import tqdm

class State(Enum):
    UNREACHED = 1
    IN_QUEUE =  2
    SCANED = 3

def init_queues(nodes, source, labels, states):
    low_q = []
    high_q = []

    for i in range(len(nodes)):
        labels[nodes.iloc[i].name] = float("inf")
        states[nodes.iloc[i].name] = State.UNREACHED

    labels[source] = 0
    states[source] = State.IN_QUEUE
    low_q.append(source)

    return low_q, high_q

def extract(low_q, high_q):
    if high_q:
        return high_q.pop(0)
    else: 
        return low_q.pop(0)
    
def scan(low_q, high_q, labels, states, i, edges):
    arcs = {}
    if i in edges.length:
        arcs = {e[0]: edges.length[i][e[0]].values[0] for e in edges.length[i].keys()}

    for j in arcs:
        if labels[i] + arcs[j] < labels[j]:
            labels[j] = labels[i] + arcs[j]

            if states[j] == State.SCANED:
                high_q.append(j)
            elif states[j] == State.UNREACHED:
                low_q.append(j)
            states[j] = State.IN_QUEUE

    states[i] = State.SCANED



from tqdm import tqdm

def two_q(graph, source, target):
    nodes_proj, edges_proj = ox.graph_to_gdfs(graph, nodes=True, edges=True)
    labels = {}
    states = {}
    low_q, high_q = init_queues(nodes_proj, source, labels, states)

    # Toplam düğüm sayısını al (ilerleme çubuğu için)
    total_nodes = len(nodes_proj)

    # Adım sayacı
    step = 0

    # tqdm ile ilerleme çubuğu oluştur
    with tqdm(total=total_nodes, desc="Two-Q Algoritması Çalışıyor", unit="it", unit_scale=True) as pbar:
        # Döngüyü başlat
        while high_q or low_q:
            # Bir düğümü kuyruktan çıkar
            i = extract(low_q, high_q)

            # Hedef düğüme ulaşıldıysa dur
            if i == target:
                print(f"Hedef düğüme ulaşıldı: {i}")
                break

            # Düğümü tarama işlemi
            scan(low_q, high_q, labels, states, i, edges_proj)

            # İlerleme çubuğunu güncelle
            pbar.update(1)
            step += 1

            # Her 1000 adımda bir ara sonuçları yazdır
            if step % 1000 == 0:
                print(f"Step {step}: Current node {i}, Labels updated: {len(labels)}")

    # En kısa yolun düğümlerini bul
    shortest_path = []
    current = target
    while current != source:
        shortest_path.append(current)
        # En kısa yolu geri takip et
        current = min((node for node in graph.neighbors(current)), key=lambda x: labels[x])
    shortest_path.append(source)
    shortest_path.reverse()  # Yolu doğru sıraya getir

    return shortest_path  # Sadece en kısa yolun düğümlerini döndür