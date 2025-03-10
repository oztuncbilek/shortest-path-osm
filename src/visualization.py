from keplergl import KeplerGl
from shapely.geometry import Point
import geopandas as gpd
import json
import os

def visualize_dual_route(route_edges_two_q, route_nodes_two_q, route_edges_dijkstra, route_nodes_dijkstra, edges_proj, nodes_proj, source_node, target_node, output_html="outputs/dual_path_visualization.html"):
    """
    İki farklı rotayı (Two-Q ve Dijkstra) KeplerGL ile görselleştirir ve HTML olarak kaydeder.
    
    Args:
        route_edges_two_q (GeoDataFrame): Two-Q algoritması ile bulunan rota kenarları.
        route_nodes_two_q (GeoDataFrame): Two-Q algoritması ile bulunan rota düğümleri.
        route_edges_dijkstra (GeoDataFrame): Dijkstra algoritması ile bulunan rota kenarları.
        route_nodes_dijkstra (GeoDataFrame): Dijkstra algoritması ile bulunan rota düğümleri.
        edges_proj (GeoDataFrame): Tüm kenarlar.
        nodes_proj (GeoDataFrame): Tüm düğümler.
        source_node (int): Kaynak düğüm ID'si.
        target_node (int): Hedef düğüm ID'si.
        output_html (str): HTML çıktı dosyasının adı.
    """
    # outputs klasörünü kontrol et ve yoksa oluştur
    output_dir = os.path.dirname(output_html)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Kaynak ve hedef noktalarının koordinatlarını al
    source_coords = (nodes_proj.loc[source_node].geometry.x, nodes_proj.loc[source_node].geometry.y)
    target_coords = (nodes_proj.loc[target_node].geometry.x, nodes_proj.loc[target_node].geometry.y)

    # Point geometrilerini oluştur
    source_point = Point(source_coords)
    target_point = Point(target_coords)

    # GeoDataFrame oluştur
    start_end_points = gpd.GeoDataFrame({
        'geometry': [source_point, target_point],
        'name': ['Kaynak', 'Hedef']
    }, crs=nodes_proj.crs)

    # Koordinatları WGS84 (EPSG:4326) formatına dönüştür
    start_end_points_wgs84 = start_end_points.to_crs(epsg=4326)

    # Config dosyasını yükle (yeni konum: src/config/updated_kepler_config.json)
    config_path = os.path.join(os.getcwd(), "src", "config", "updated_kepler_config.json")
    with open(config_path, 'r', encoding="utf-8") as f:
        updated_config = json.load(f)

    # Güncel config'i haritaya uygula
    print("Config yapılandırması uygulanıyor...")
    route_map = KeplerGl(height=823, width=957, data={
        "two_q_edges": route_edges_two_q,
        "dijkstra_edges": route_edges_dijkstra,
        "start_end": start_end_points_wgs84 , # WGS84 formatında noktalar
        "all_edges": edges_proj,  
        "all_nodes": nodes_proj  
    })
    route_map.config = updated_config["config"]

    # HTML olarak kaydet
    print(f"HTML dosyası kaydediliyor: {output_html}")
    route_map.save_to_html(file_name=output_html)
    print(f"Görselleştirme sonucu '{output_html}' olarak kaydedildi.")

    # HTML dosyasını aç ve template.html içeriğini ekle
    with open(output_html, "r+", encoding="utf-8") as file:
        content = file.read()
        
        # Template dosyasını oku
        template_path = os.path.join(os.getcwd(), "src", "templates", "template.html")
        with open(template_path, 'r', encoding="utf-8") as template_file:
            template_content = template_file.read()
        
        # HTML dosyasının içeriğini template ile değiştir
        content = template_content.replace('<div id="map"></div>', content)

        file.seek(0)
        file.write(content)
        file.truncate()