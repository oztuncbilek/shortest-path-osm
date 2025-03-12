from keplergl import KeplerGl
from shapely.geometry import Point
import geopandas as gpd
import json
import os

def visualize_dual_route(route_edges_two_q, route_nodes_two_q, route_edges_dijkstra, route_nodes_dijkstra, edges_proj, nodes_proj, source_node, target_node, output_html="outputs/dual_path_visualization.html"):
    """
    Visualizes two different routes (Two-Q and Dijkstra) using KeplerGL and saves the result as an HTML file.
    
    Args:
        route_edges_two_q (GeoDataFrame): Edges of the route found by the Two-Q algorithm.
        route_nodes_two_q (GeoDataFrame): Nodes of the route found by the Two-Q algorithm.
        route_edges_dijkstra (GeoDataFrame): Edges of the route found by Dijkstra's algorithm.
        route_nodes_dijkstra (GeoDataFrame): Nodes of the route found by Dijkstra's algorithm.
        edges_proj (GeoDataFrame): All edges in the graph.
        nodes_proj (GeoDataFrame): All nodes in the graph.
        source_node (int): ID of the source node.
        target_node (int): ID of the target node.
        output_html (str): Name of the output HTML file.
    """
    # Check if the outputs directory exists, and create it if it doesn't
    output_dir = os.path.dirname(output_html)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the coordinates of the source and target nodes
    source_coords = (nodes_proj.loc[source_node].geometry.x, nodes_proj.loc[source_node].geometry.y)
    target_coords = (nodes_proj.loc[target_node].geometry.x, nodes_proj.loc[target_node].geometry.y)

    # Create Point geometries for the source and target
    source_point = Point(source_coords)
    target_point = Point(target_coords)

    # Create a GeoDataFrame for the start and end points
    start_end_points = gpd.GeoDataFrame({
        'geometry': [source_point, target_point],
        'name': ['Source', 'Target']
    }, crs=nodes_proj.crs)

    # Convert coordinates to WGS84 (EPSG:4326) format
    start_end_points_wgs84 = start_end_points.to_crs(epsg=4326)

    # Load the config file (new location: src/config/updated_kepler_config.json)
    config_path = os.path.join(os.getcwd(), "src", "config", "updated_kepler_config.json")
    with open(config_path, 'r', encoding="utf-8") as f:
        updated_config = json.load(f)

    # Apply the updated config to the map
    print("Applying config configuration...")
    route_map = KeplerGl(height=823, width=957, data={
        "two_q_edges": route_edges_two_q,
        "dijkstra_edges": route_edges_dijkstra,
        "start_end": start_end_points_wgs84,  # Points in WGS84 format
        "all_edges": edges_proj,  
        "all_nodes": nodes_proj  
    })
    route_map.config = updated_config["config"]

    # Save the map as an HTML file
    print(f"Saving HTML file: {output_html}")
    route_map.save_to_html(file_name=output_html)
    print(f"Visualization result saved as '{output_html}'.")

    # Open the HTML file and insert the template.html content
    with open(output_html, "r+", encoding="utf-8") as file:
        content = file.read()
        
        # Read the template file
        template_path = os.path.join(os.getcwd(), "src", "templates", "template.html")
        with open(template_path, 'r', encoding="utf-8") as template_file:
            template_content = template_file.read()
        
        # Replace the content of the HTML file with the template
        content = template_content.replace('<div id="map"></div>', content)

        file.seek(0)
        file.write(content)
        file.truncate()