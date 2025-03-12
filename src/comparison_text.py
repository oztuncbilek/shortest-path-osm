# src/comparison_text.py
import os

def calculate_route_length(graph, route):
    """
    Calculates the total length of the route in meters.
    
    Args:
        graph (networkx.Graph): OSMnx graph object.
        route (list): List of nodes representing the route.
    
    Returns:
        float: Total length of the route in meters.
    """
    total_length = 0.0
    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]
        edge_data = graph.get_edge_data(u, v)
        if edge_data:
            total_length += edge_data[0].get('length', 0.0)  
    return total_length

def calculate_travel_time_walking(route_length):
    """
    Calculates the total walking time for the route.
    
    Args:
        route_length (float): Total length of the route in meters.
    
    Returns:
        float: Total walking time in seconds.
    """
    walking_speed = 1.4  # Based on walking speed of average person (m/s)
    return route_length / walking_speed

def save_algorithm_comparison(two_q_result, dijkstra_result, two_q_time, dijkstra_time, graph, output_file="outputs/algorithm_comparison.txt"):
    """
    Saves the algorithm comparison results to a text file.
    
    Args:
        two_q_result (list): Route found by the Two-Q algorithm.
        dijkstra_result (list): Route found by the Dijkstra algorithm.
        two_q_time (float): Execution time of the Two-Q algorithm.
        dijkstra_time (float): Execution time of the Dijkstra algorithm.
        graph (networkx.Graph): OSMnx graph object.
        output_file (str): Path to the output file where results will be saved.
    """
    # Check outputs folder and create one if there is none
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Calculate distance and travel time
    two_q_length_meters = calculate_route_length(graph, two_q_result)
    dijkstra_length_meters = calculate_route_length(graph, dijkstra_result)
    two_q_travel_time_walking = calculate_travel_time_walking(two_q_length_meters)
    dijkstra_travel_time_walking = calculate_travel_time_walking(dijkstra_length_meters)

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

    with open(output_file, "w") as file:
        file.write(comparison_text)

    print(f"Algorithm comparison saved to {output_file}")