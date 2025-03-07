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

    # Kaynak noktasının WGS84 koordinatlarını al
    source_lat = start_end_points_wgs84.iloc[0].geometry.y
    source_lon = start_end_points_wgs84.iloc[0].geometry.x

    # Harita merkezini ve zoom seviyesini ayarla (source_node'a odaklan)
    map_center = {
        "latitude": source_lat,
        "longitude": source_lon,
        "zoom": 13.2
    }

    # KeplerGL haritası oluştur
    route_map = KeplerGl(height=823, width=957, data={
        "two_q_edges": route_edges_two_q,
        "two_q_nodes": route_nodes_two_q,
        "dijkstra_edges": route_edges_dijkstra,
        "dijkstra_nodes": route_nodes_dijkstra,
        "network": edges_proj,
        "nodes": nodes_proj,
        "start_end": start_end_points_wgs84  # WGS84 formatında noktalar
    })

    # Config dosyasını yükle 
    config_path = os.path.join(os.getcwd(), "outputs", "updated_kepler_config.json")

    # Config dosyasının varlığını kontrol et
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with open(config_path, 'r', encoding="utf-8") as f:
        updated_config = json.load(f)

    # Harita merkezini ve zoom seviyesini config'e ekle
    updated_config["config"]["mapState"] = {
        "bearing": 0,
        "dragRotate": False,
        "latitude": map_center["latitude"],
        "longitude": map_center["longitude"],
        "pitch": 0,
        "zoom": map_center["zoom"],
        "isSplit": True,  # Dual view için split modunu aktif et
    }

    # Layer ayarları (Two-Q ve Dijkstra için farklı renkler)
    updated_config["config"]["visState"]["layers"] = [
        {
            "id": "two_q_edges",
            "type": "line",
            "config": {
                "dataId": "two_q_edges",
                "label": "Two-Q Rota",
                "color": [0, 0, 255],  # Mavi renk
                "columns": {
                    "lat": "geometry",
                    "lng": "geometry"
                },
                "isVisible": True,
                "visConfig": {
                    "opacity": 0.8,
                    "thickness": 2
                }
            }
        },
        {
            "id": "dijkstra_edges",
            "type": "line",
            "config": {
                "dataId": "dijkstra_edges",
                "label": "Dijkstra Rota",
                "color": [255, 0, 0],  # Kırmızı renk
                "columns": {
                    "lat": "geometry",
                    "lng": "geometry"
                },
                "isVisible": True,
                "visConfig": {
                    "opacity": 0.8,
                    "thickness": 2
                }
            }
        }
    ]

    # Güncel config'i haritaya uygula
    print("Config yapılandırması uygulanıyor...")
    route_map.config = updated_config["config"]

    # HTML olarak kaydet
    print(f"HTML dosyası kaydediliyor: {output_html}")
    route_map.save_to_html(file_name=output_html)
    print(f"Görselleştirme sonucu '{output_html}' olarak kaydedildi.")

    # HTML dosyasını aç ve gereksiz CSS yazısını sil
    with open(output_html, "r+", encoding="utf-8") as file:
        content = file.read()
        
        # Gereksiz CSS yazısını sil
        unwanted_css = '''font-family: ff-clan-web-pro, 'Helvetica Neue', Helvetica, sans-serif; 
        font-weight: 400; 
        font-size: 0.875em; 
        line-height: 1.71429; 
        *, *:before, *:after { 
            -webkit-box-sizing: border-box; 
            -moz-box-sizing: border-box; 
            box-sizing: border-box; 
        } 
        body { 
            margin: 0; 
            padding: 0; 
        }'''
        
        # Tam ekran yapmak için CSS ekle
        fullscreen_css = '''<style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
        }
        .kepler-gl {
            height: 100vh !important;
            width: 100vw !important;
        }
        </style>'''

        # CSS'i HTML dosyasına ekle
        content = content.replace('<style>', fullscreen_css + '<style>')

        # Gereksiz CSS yazısını içeren kısmı sil
        content = content.replace(unwanted_css, "")

        file.seek(0)
        file.write(content)
        file.truncate()