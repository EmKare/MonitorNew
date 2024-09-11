import folium

# Create a map centered on a specific location
map_center = [18.0118757, -76.7968643]  # New York City
my_map = folium.Map(location=map_center, zoom_start=12)

# Define route coordinates
route_coordinates = [
[18.011877,-76.796858],
[18.011164,-76.79674],
[18.010999,-76.796697],
[18.011139,-76.796194],
[18.011197,-76.796033],
[18.011383,-76.7956],
[18.011621,-76.795018],
[18.011639,-76.794968],
[18.011825,-76.794418],
[18.011999,-76.79386],
[18.012404,-76.792816],
[18.012902,-76.791672],
[18.013198,-76.791069],
[18.012514,-76.790775],
[18.011941,-76.790359],
[18.011916,-76.790335],
[18.011779,-76.7902],
[18.011685,-76.790023],
[18.011547,-76.789819],
[18.011334,-76.789378],
[18.011285,-76.789274],
[18.011195,-76.789072],
[18.010801,-76.788153],
[18.010492,-76.787431],
[18.010272,-76.786879],
[18.010169,-76.78666],
[18.009479,-76.785368],
[18.00945,-76.785312],
[18.009008,-76.784394],
[18.008812,-76.783866],
[18.00879,-76.783789],
[18.008371,-76.78253],
[18.008078,-76.78168],
[18.007943,-76.781315],
[18.007935,-76.78129],
[18.007831,-76.781321],
[18.007662,-76.78138],
[18.007414,-76.78151],
]

# Add a polyline to the map representing the route
folium.PolyLine(route_coordinates, color="blue", weight=2.5, opacity=1).add_to(my_map)

# Add markers for the start and end points
folium.Marker(route_coordinates[0], popup="Start").add_to(my_map)
folium.Marker(route_coordinates[-1], popup="End").add_to(my_map)

# Save the map as an HTML file
my_map.save("route_map.html")