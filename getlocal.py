import osmnx as ox
import networkx as nx 

location = "New York City, USA"

driving = ox.graph_from_place(location, network_type = 'drive')

source = (40.7128, -74.0060)
target = (40.748817, -73.985428)

source_node = ox.nearest_nodes(driving,source)
target_node = ox.nearest_nodes(driving,target)

shortestPath = nx.shortest_path(driving, source = source_node, target = target_node, weight = 'length')

print('Shortest path : ', shortestPath)

fig, ax = ox.plot_graph_route(driving, shortestPath, route_color = 'r')