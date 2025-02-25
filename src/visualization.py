from keplergl import KeplerGl
from tqdm import tqdm

def visualize_route(route_edges, route_nodes, edges_proj, nodes_proj, output_html="route_visualization.html"):
    """
    Rota bilgilerini KeplerGL ile görselleştirir ve HTML olarak kaydeder.
    
    Args:
        route_edges (GeoDataFrame): Rota kenarları.
        route_nodes (GeoDataFrame): Rota düğümleri.
        edges_proj (GeoDataFrame): Tüm kenarlar.
        nodes_proj (GeoDataFrame): Tüm düğümler.
        output_html (str): HTML çıktı dosyasının adı.
    """

    print("Harita oluşturuluyor...")
    # KeplerGL haritası oluştur
    route_muc = KeplerGl(height=700, data={"muc": route_edges, "edges": route_nodes, "network": edges_proj, "nodes": nodes_proj})

    # Config yapılandırmasını ekle
    config = {
        'version': 'v1',
        'config': {
            'visState': {
                'filters': [],
                'layers': [
                    {
                        'id': '8qdqs2m',
                        'type': 'geojson',
                        'config': {
                            'dataId': 'muc',
                            'label': 'muc',
                            'color': [77, 193, 156],
                            'highlightColor': [252, 242, 26, 255],
                            'columns': {'geojson': 'geometry'},
                            'isVisible': True,
                            'visConfig': {
                                'opacity': 0.8,
                                'strokeOpacity': 0.8,
                                'thickness': 0.5,
                                'strokeColor': None,
                                'colorRange': {
                                    'name': 'Global Warming',
                                    'type': 'sequential',
                                    'category': 'Uber',
                                    'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                                },
                                'strokeColorRange': {
                                    'name': 'Global Warming',
                                    'type': 'sequential',
                                    'category': 'Uber',
                                    'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                                },
                                'radius': 10,
                                'sizeRange': [0, 10],
                                'radiusRange': [0, 50],
                                'heightRange': [0, 500],
                                'elevationScale': 5,
                                'enableElevationZoomFactor': True,
                                'stroked': True,
                                'filled': False,
                                'enable3d': False,
                                'wireframe': False
                            },
                            'hidden': False,
                            'textLabel': [{
                                'field': None,
                                'color': [255, 255, 255],
                                'size': 18,
                                'offset': [0, 0],
                                'anchor': 'start',
                                'alignment': 'center'
                            }]
                        },
                        'visualChannels': {
                            'colorField': None,
                            'colorScale': 'quantile',
                            'strokeColorField': None,
                            'strokeColorScale': 'quantile',
                            'sizeField': None,
                            'sizeScale': 'linear',
                            'heightField': None,
                            'heightScale': 'linear',
                            'radiusField': None,
                            'radiusScale': 'linear'
                        }
                    },
                    {
                        'id': 'p557il8',
                        'type': 'geojson',
                        'config': {
                            'dataId': 'edges',
                            'label': 'edges',
                            'color': [23, 184, 190],
                            'highlightColor': [252, 242, 26, 255],
                            'columns': {'geojson': 'geometry'},
                            'isVisible': True,
                            'visConfig': {
                                'opacity': 0.8,
                                'strokeOpacity': 0.8,
                                'thickness': 0.5,
                                'strokeColor': None,
                                'colorRange': {
                                    'name': 'Global Warming',
                                    'type': 'sequential',
                                    'category': 'Uber',
                                    'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                                },
                                'strokeColorRange': {
                                    'name': 'Global Warming',
                                    'type': 'sequential',
                                    'category': 'Uber',
                                    'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                                },
                                'radius': 10,
                                'sizeRange': [0, 10],
                                'radiusRange': [0, 50],
                                'heightRange': [0, 500],
                                'elevationScale': 5,
                                'enableElevationZoomFactor': True,
                                'stroked': False,
                                'filled': True,
                                'enable3d': False,
                                'wireframe': False
                            },
                            'hidden': False,
                            'textLabel': [{
                                'field': None,
                                'color': [255, 255, 255],
                                'size': 18,
                                'offset': [0, 0],
                                'anchor': 'start',
                                'alignment': 'center'
                            }]
                        },
                        'visualChannels': {
                            'colorField': None,
                            'colorScale': 'quantile',
                            'strokeColorField': None,
                            'strokeColorScale': 'quantile',
                            'sizeField': None,
                            'sizeScale': 'linear',
                            'heightField': None,
                            'heightScale': 'linear',
                            'radiusField': None,
                            'radiusScale': 'linear'
                        }
                    },
                    {
                        'id': 'qwigsz',
                        'type': 'geojson',
                        'config': {
                            'dataId': 'network',
                            'label': 'network',
                            'color': [246, 209, 138],
                            'highlightColor': [252, 242, 26, 255],
                            'columns': {'geojson': 'geometry'},
                            'isVisible': True,
                            'visConfig': {
                                'opacity': 0.8,
                                'strokeOpacity': 0.8,
                                'thickness': 0.1,
                                'strokeColor': None,
                                'colorRange': {
                                    'name': 'Global Warming',
                                    'type': 'sequential',
                                    'category': 'Uber',
                                    'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                                },
                                'strokeColorRange': {
                                    'name': 'Global Warming',
                                    'type': 'sequential',
                                    'category': 'Uber',
                                    'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                                },
                                'radius': 10,
                                'sizeRange': [0, 10],
                                'radiusRange': [0, 50],
                                'heightRange': [0, 500],
                                'elevationScale': 5,
                                'enableElevationZoomFactor': True,
                                'stroked': True,
                                'filled': False,
                                'enable3d': False,
                                'wireframe': False
                            },
                            'hidden': False,
                            'textLabel': [{
                                'field': None,
                                'color': [255, 255, 255],
                                'size': 18,
                                'offset': [0, 0],
                                'anchor': 'start',
                                'alignment': 'center'
                            }]
                        },
                        'visualChannels': {
                            'colorField': None,
                            'colorScale': 'quantile',
                            'strokeColorField': None,
                            'strokeColorScale': 'quantile',
                            'sizeField': None,
                            'sizeScale': 'linear',
                            'heightField': None,
                            'heightScale': 'linear',
                            'radiusField': None,
                            'radiusScale': 'linear'
                        }
                    }
                ],
                'interactionConfig': {
                    'tooltip': {
                        'fieldsToShow': {
                            'muc': [
                                {'name': 'osmid', 'format': None},
                                {'name': 'oneway', 'format': None},
                                {'name': 'lanes', 'format': None},
                                {'name': 'name', 'format': None},
                                {'name': 'highway', 'format': None}
                            ],
                            'edges': [
                                {'name': 'y', 'format': None},
                                {'name': 'x', 'format': None},
                                {'name': 'highway', 'format': None},
                                {'name': 'ref', 'format': None}
                            ],
                            'network': [
                                {'name': 'osmid', 'format': None},
                                {'name': 'oneway', 'format': None},
                                {'name': 'lanes', 'format': None},
                                {'name': 'name', 'format': None},
                                {'name': 'highway', 'format': None}
                            ]
                        },
                        'compareMode': False,
                        'compareType': 'absolute',
                        'enabled': True
                    },
                    'brush': {'size': 0.5, 'enabled': False},
                    'geocoder': {'enabled': False},
                    'coordinate': {'enabled': False}
                },
                'layerBlending': 'normal',
                'splitMaps': [],
                'animationConfig': {'currentTime': None, 'speed': 1}
            },
            'mapState': {
                'bearing': 0,
                'dragRotate': False,
                'latitude': 48.13095857731462,
                'longitude': 11.586642695981286,
                'pitch': 0,
                'zoom': 12.993509727831723,
                'isSplit': False
            },
            'mapStyle': {
                'styleType': 'dark',
                'topLayerGroups': {},
                'visibleLayerGroups': {
                    'label': True,
                    'road': True,
                    'border': False,
                    'building': True,
                    'water': True,
                    'land': True,
                    '3d building': False
                },
                'threeDBuildingColor': [9.665468314072013, 17.18305478057247, 31.1442867897876],
                'mapStyles': {}
            }
        }
    }

    print("Config yapılandırması uygulanıyor...")
    # Config'i haritaya uygula
    route_muc.config = config

    # HTML olarak kaydet
    print(f"HTML dosyası kaydediliyor: {output_html}")
    route_muc.save_to_html(file_name=output_html)
    print(f"Görselleştirme sonucu '{output_html}' olarak kaydedildi.")