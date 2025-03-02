from keplergl import KeplerGl
from shapely.geometry import Point
import geopandas as gpd
import json

def visualize_route(route_edges, route_nodes, edges_proj, nodes_proj, source_node, target_node, output_html="route_visualization.html"):
    """
    Rota bilgilerini KeplerGL ile görselleştirir ve HTML olarak kaydeder.
    
    Args:
        route_edges (GeoDataFrame): Rota kenarları.
        route_nodes (GeoDataFrame): Rota düğümleri.
        edges_proj (GeoDataFrame): Tüm kenarlar.
        nodes_proj (GeoDataFrame): Tüm düğümler.
        source_node (int): Kaynak düğüm ID'si.
        target_node (int): Hedef düğüm ID'si.
        output_html (str): HTML çıktı dosyasının adı.
    """
    # Kaynak ve hedef noktalarının koordinatlarını al
    source_coords = (nodes_proj.loc[source_node].geometry.x, nodes_proj.loc[source_node].geometry.y)
    target_coords = (nodes_proj.loc[target_node].geometry.x, nodes_proj.loc[target_node].geometry.y)

    # Point geometrilerini oluştur
    source_point = Point(source_coords)
    target_point = Point(target_coords)

    # GeoDataFrame oluştur
    start_end_points = gpd.GeoDataFrame({
        'geometry': [source_point, target_point],
        'name': ['Kaynak', 'Hedef']  # Noktaları etiketlemek için
    }, crs=nodes_proj.crs)  # Mevcut projeksiyonu kullanın

    # Koordinatları WGS84 (EPSG:4326) formatına dönüştür
    start_end_points_wgs84 = start_end_points.to_crs(epsg=4326)

    # Kaynak noktasının WGS84 koordinatlarını al
    source_lat = start_end_points_wgs84.iloc[0].geometry.y  # Latitude (enlem)
    source_lon = start_end_points_wgs84.iloc[0].geometry.x  # Longitude (boylam)

    # Harita merkezini ve zoom seviyesini ayarla (source_node'a odaklan)
    map_center = {
        "latitude": source_lat,  # Kaynak düğümün enlemi (latitude)
        "longitude": source_lon,  # Kaynak düğümün boylamı (longitude)
        "zoom": 13.5
    }

    # KeplerGL haritası oluştur
    route_muc = KeplerGl(height=823, width=957, data={
        "muc": route_edges,
        "edges": route_nodes,
        "network": edges_proj,
        "nodes": nodes_proj,
        "start_end": start_end_points_wgs84  # WGS84 formatında noktalar
    })

    # Config dosyasını yükle
    config_path = "outputs/updated_kepler_config.json"  # Config dosyasının yolu
    with open(config_path, 'r') as f:
        updated_config = json.load(f)

    # Harita merkezini ve zoom seviyesini config'e ekle
    updated_config["config"]["mapState"] = {
        "bearing": 0,
        "dragRotate": False,
        "latitude": map_center["latitude"],
        "longitude": map_center["longitude"],
        "pitch": 0,
        "zoom": map_center["zoom"],
        "isSplit": False,
    }

    # Güncel config'i haritaya uygula
    print("Config yapılandırması uygulanıyor...")
    route_muc.config = updated_config["config"]

    # HTML olarak kaydet
    print(f"HTML dosyası kaydediliyor: {output_html}")
    route_muc.save_to_html(file_name=output_html)
    print(f"Görselleştirme sonucu '{output_html}' olarak kaydedildi.")


  # HTML dosyasını aç ve gereksiz CSS yazısını sil
    with open(output_html, "r+") as file:
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

        # Dosyayı başa sar ve güncellenmiş içeriği yaz
        file.seek(0)
        file.write(content)
        file.truncate()
