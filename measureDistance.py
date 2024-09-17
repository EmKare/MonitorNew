from geopy.geocoders import Nominatim
from geopy import distance
import openrouteservice as ors
import folium as fl

client = ors.Client(key='5b3ce3597851110001cf62480f6929fa14f1415b865522ca5d94fb50')

m = fl.Map(location=list(reversed([-76.7968643, 18.0118757])),  zoom_start=16) #tiles="cartodbpositron",

coords = [[-76.7968643, 18.0118757], [-76.7812398, 18.0072864]]

route = client.directions(coordinates=coords,
                          profile='driving-car',
                          format='geojson',)

route_list = [tuple(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
route_list.insert(0, tuple(reversed(coords[0])))
route_list.insert(len(route_list), tuple(reversed(coords[1])))
fl.PolyLine(locations=route_list, color="blue").add_to(m)
print(len(route_list))

#m

route_distance, start, end = 0, 0, 1

while end < len(route_list):
    route_distance += distance.distance(route_list[start], route_list[end]).km
    print(f"{end}: {route_distance} kms - start:{end}, end:{end+1}")
    start += 1
    end += 1
    
s = (18.0118757, -76.7968643)
e = (18.0072864, -76.7812398)
print(f"dist = {distance.distance(s, e).km} kms")

m