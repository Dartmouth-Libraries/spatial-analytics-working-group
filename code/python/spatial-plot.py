
import folium
# Task - plot a point on a web map 
# add a point 

latitude = 40.7488 # latitude is the 'y' coordinate
longitude = -73.9857 # longitude is the 'x' coordinate 

# Create a marker for Grand Central Station and its Popup contents
marker = folium.Marker([latitude, longitude], popup="Grand Central Station", tooltip="Grand Central Marker")  # Add an icon (optional)

# Add the marker to the Map
map.add_child(marker)
map
