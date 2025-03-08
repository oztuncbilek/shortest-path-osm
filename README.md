# **Project: Map Visualization and Route Planning**  

This project uses OpenStreetMap (OSM) data to perform map visualization and route planning. It is developed using Python and the KeplerGL library.  

## **Features**  
- Load and process OSM data.  
- Plan routes using the shortest path algorithm (Two-Q and Dijkstra).  
- Visualize routes on a map and save as an HTML file.  
- Compare the results of multiple shortest path algorithms.  

## **About**  
This project is entirely developed in Python, with the output being an interactive HTML file. The HTML file is generated using the KeplerGL library, which allows for dynamic and interactive map visualizations. The project demonstrates how to:  
- Load and process geographic data.  
- Implement shortest path algorithms (Two-Q and Dijkstra).  
- Visualize the results on an interactive map (KeplerGL).  

The output HTML file is lightweight and can be easily shared or embedded in web applications. The project is designed to be modular and extensible, making it easy to adapt for different use cases.

## **Algorithm Result Comparison**  
The project now supports a structured comparison between multiple shortest path algorithms. The following algorithms are implemented:  
- **Two-Q Algorithm**: A custom shortest path algorithm optimized for large networks.  
- **Dijkstra's Algorithm**: A classic shortest path algorithm for weighted graphs.  

The comparison includes:  
- Route length (number of nodes).  
- Execution time.  
- Visualization of both routes on a dual-view map.  

## Running with Docker  

You can run this project in a Docker container to ensure consistency across environments. Follow these steps:  

### Build the Docker Image  

Before running the container, build the image using:  

```bash
docker build -t map-visualization.
```

### Run the Container  
Once the build is complete, run the container:  

```bash
docker run -p 8050:8050 --name map-container map-visualization
```

## Future Improvements  

- **Dual View Map Visualization**: Implement a dual-panel map to compare different routing results.  
 
- **User Interface:**: Develop a web-based interface for easier interaction.











