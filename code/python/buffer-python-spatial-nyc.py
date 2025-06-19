# Task #1 
# Import necessary libraries
import folium

# Create a Map centered over Grand Central Station
map = folium.Map(location=[40.7488, -73.9857], tiles="openstreetmap")  
map

# Task #2 
# add a point 

# Create a marker for Grand Central Station and its Popup contents
marker = folium.Marker([40.7488, -73.9857], popup="Grand Central Station", tooltip="Grand Central Marker")  # Add an icon (optional)

# Add the marker to the Map
map.add_child(marker)
map

# Task #3, import a polygon shapefile and display it using folium / leaflet / open street map base map
# task 3 

import geopandas as gpd
import geodatasets
import matplotlib.pyplot as plt
from geodatasets import get_path
import folium

# Load NY boroughs dataset path and then read it with geopandas
path_to_nybb = get_path('nybb')
nybb = gpd.read_file(path_to_nybb)

# Folium uses lat/lng coordinates, ensure geometry is in WGS84 (EPSG:4326)
nybb = nybb.to_crs(epsg=4326)

# Create a folium map centered on New York City (rough center of boroughs)
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add the borough polygons to the map with a simple style
folium.GeoJson(
    nybb,
    name='NY Boroughs',
    style_function=lambda feature: {
        'fillColor': '#blue',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5,
    },
).add_to(m)

# Add layer control to toggle layers on/off (handy if you add more layers)
folium.LayerControl().add_to(m)

# Save to an HTML file and display (if running in Jupyter, just display m)
m.save('ny_boroughs_map.html')
m  # If using Jupyter Notebook, this will display the map inline

# task 4, add points of interest and polygons to map 

from geodatasets import get_path
from shapely.geometry import Point

# Load NY boroughs from geodatasets
path_to_nybb = get_path('nybb')
nybb = gpd.read_file(path_to_nybb)

# Project to EPSG:3857 (meters) for accurate spatial analysis
nybb = nybb.to_crs(epsg=3857)

# Dissolve all boroughs into a single polygon (NYC boundary)
nyc_boundary = nybb.dissolve()

# Create synthetic points of interest (lat, lon approx locations within NYC)
# Coordinates are WGS84 (EPSG:4326), need to project later
poi_data = {
    "name": [
        "Statue of Liberty",
        "Times Square",
        "Central Park",
        "Brooklyn Bridge",
        "Empire State Building",
        "Yankee Stadium"
    ],
    "latitude": [
        40.6892, 40.7580, 40.7829, 40.7061, 40.7484, 40.8296
    ],
    "longitude": [
        -74.0445, -73.9855, -73.9654, -73.9969, -73.9857, -73.9262
    ]
}

# Create GeoDataFrame of points
pois = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)

# Project points to match nybb CRS (EPSG:3857)
pois = pois.to_crs(epsg=3857)

# Create buffers around POIs (e.g., 1000 meters = 1 km)
pois['buffer'] = pois.geometry.buffer(1000)

# Plot everything
fig, ax = plt.subplots(figsize=(12, 12))

# Plot boroughs with light green
nybb.plot(ax=ax, color='lightgreen', edgecolor='black', label='Boroughs')

# Plot merged NYC boundary with red border
nyc_boundary.plot(ax=ax, color='none', edgecolor='red', linewidth=3, label='Merged Boundary')

# Plot POI buffers (light blue, transparent)
pois['buffer'].plot(ax=ax, color='lightblue', alpha=0.5, label='1km Buffers')

# Plot POIs (red points)
pois.plot(ax=ax, color='red', markersize=50, label='Points of Interest')

# Annotate POIs with their names
for x, y, label in zip(pois.geometry.x, pois.geometry.y, pois['name']):
    ax.text(x + 100, y + 100, label, fontsize=9)

plt.legend()
plt.title("NYC Boroughs, Merged Boundary, and Synthetic Points of Interest with Buffers")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis('equal')  # Equal scaling
plt.show()

#========


import folium
import geopandas as gpd
from geodatasets import get_path
from shapely.geometry import Point

# Load borough boundaries
nybb_fp = get_path('nybb')
nybb = gpd.read_file(nybb_fp).to_crs(epsg=4326)
nyc_boundary = nybb.dissolve()

# Original POIs plus 10 new points including airports, major train stations, and Yale Club
poi_data = {
    "name": [
        "Statue of Liberty",
        "Times Square",
        "Central Park",
        "Brooklyn Bridge",
        "Empire State Building",
        "Yankee Stadium",
        "John F. Kennedy International Airport (JFK)",
        "LaGuardia Airport (LGA)",
        "Newark Liberty International Airport (EWR)",
        "Penn Station",
        "Grand Central Terminal",
        "Port Authority Bus Terminal",
        "Atlantic Terminal",
        "Harlem–125th Street Station",
        "Yale Club of New York City"
    ],
    "latitude": [
        40.6892, 40.7580, 40.7829, 40.7061, 40.7484, 40.8296,
        40.6413, 40.7769, 40.6895,
        40.7506, 40.7527, 40.7570, 40.6839, 40.8116, 40.7509
    ],
    "longitude": [
        -74.0445, -73.9855, -73.9654, -73.9969, -73.9857, -73.9262,
        -73.7781, -73.8740, -74.1745,
        -73.9935, -73.9772, -73.9903, -73.9769, -73.9465, -73.9754
    ]
}

pois = gpd.GeoDataFrame(
    poi_data,
    geometry=gpd.points_from_xy(poi_data['longitude'], poi_data['latitude']),
    crs="EPSG:4326"
)

# Project for buffering
nybb_proj = nybb.to_crs(epsg=3857)
pois_proj = pois.to_crs(epsg=3857)
pois_proj['buffer'] = pois_proj.geometry.buffer(1000)
buffers_wgs84 = pois_proj.set_geometry('buffer').to_crs(epsg=4326)

# Center map around NYC
center_lat = 40.7128
center_lon = -74.0060
m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles='CartoDB positron')

# Add borough polygons with popups showing borough names
folium.GeoJson(
    nybb,
    name='Boroughs',
    style_function=lambda x: {
        'fillColor': 'lightgreen',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.4,
    },
    tooltip=folium.GeoJsonTooltip(fields=['BoroName'], aliases=['Borough:'])
).add_to(m)

# Add NYC boundary
folium.GeoJson(
    nyc_boundary.geometry.__geo_interface__,
    name='NYC Boundary',
    style_function=lambda x: {
        'fillColor': 'none',
        'color': 'red',
        'weight': 3,
    }
).add_to(m)

# Add buffers around POIs
for _, row in buffers_wgs84.iterrows():
    geojson = folium.GeoJson(row['buffer'].__geo_interface__,
                             style_function=lambda x: {
                                 'fillColor': 'lightblue',
                                 'color': 'blue',
                                 'weight': 1,
                                 'fillOpacity': 0.3,
                             })
    geojson.add_child(folium.Popup(row['name']))
    geojson.add_to(m)

# Add markers for POIs
for _, row in pois.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=row['name'],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

m
