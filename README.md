# **Project: Map Visualization and Route Planning**  

This project uses OpenStreetMap (OSM) data to perform map visualization and route planning. It is developed using Python and the KeplerGL library.  

## **Features**  
- Load and process OSM data.  
- Plan routes using the shortest path algorithm.  
- Visualize routes on a map and save as an HTML file.  

## About
This project is entirely developed in Python, with the output being an 
interactive HTML file. The HTML file is generated using the KeplerGL library 
which allows for dynamic and interactive map visualizations. The project 
demonstrates how to:
- Load and process geographic data.
- Implement a shortest path algorithm (Two-Q).
- Visualize the results on an interactive map(Kepler GL).

The output HTML file is lightweight and can be easily shared or embedded in web 
applications. The project is designed to be modular and extensible, making it 
easy to adapt for different use cases.

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

- **Dijkstra Algorithm Comparison**: Compare the Two-Q shortest path algorithm with Dijkstra’s algorithm.  
- **Dual View Map Visualization**: Implement a dual-panel map to compare different routing results.  
- **Algorithm Result Comparison**: Add a structured output comparison between multiple shortest path algorithms.  




