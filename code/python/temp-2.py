# %%
# task  import dataset of points 

#!pip install geopandas
#!pip install shapely
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely

# import a CSV that contains latitude and longitude coordinate pairs 
points = pd.read_csv("https://rcweb.dartmouth.edu/homes/f002d69/workshops/data/bear-sightings.csv")
points.head(3)

# convert points from latitude longitude to a 'geopandas' spatial data frame 
points = gpd.GeoDataFrame(points, geometry=gpd.points_from_xy(points.longitude, points.latitude))
points.head(2)

# quick visualization to check the points 
points.plot()
plt.show()

# task load polygon shapefile into geopandas 

# NOTE: zip file containing a 'shapefile', which actually has several files within the zipfile
  # these include files .shp, .prj, .dbf, .shx, .cpg 
# function delete for backspace / del 
zipfile_url = "https://rcweb.dartmouth.edu/homes/f002d69/workshops/data/nationalparks_ak.zip"
polygons = gpd.read_file(zipfile_url)
print(polygons.head())

# quick viz of polygons 

polygons.plot()
plt.show()

# set crs 
points.crs='EPSG:4326'
points = points.to_crs(polygons.crs)
points.crs.to_epsg()

# intersect / spatial join (geopandas' "sjoin") / overlay 
points_in_polygons = gpd.sjoin(points, polygons, predicate='within')
points_in_polygons.head(2)

# basic visualization of points-in-polygons overlay (sjoin/spatial join/intersect) results using matplotlib  
polygons.plot(facecolor='none')
points.plot(ax=plt.gca())
points_in_polygons.plot(color='red',ax=plt.gca())
plt.axis("off")
plt.show()


# %%
# show the above layers on a folium map instead of matplotlib
import folium
map = folium.Map(location=[62.65822, -148.95602],
    zoom_start=5,
    control_scale=True)
# loop through points
for index, row in points.iterrows():
    folium.CircleMarker(location=[ row.latitude,row.longitude], radius =5).add_to(map)
# loop through points in polygons, color them gray
for index, row in points_in_polygons.iterrows():
    folium.CircleMarker(location=[ row.latitude,row.longitude], color = 'gray',fill=True, fill_opacity=1).add_to(map)

# add polygons to the map
for index, row in polygons.iterrows():
    folium.GeoJson(row.geometry.__geo_interface__, name='National Parks').add_to(map)

map

# %%
# task add points and buffer the points by 1000 meters 
# then polygons to map 

# Create points of interest (lat, lon approx locations within NYC)
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

# use shapely's "Point" 
from shapely.geometry import Point

# Create GeoDataFrame of points
pois_gpd = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)

# Project points  CRS (EPSG:3857)
pois_gpd = pois_gpd.to_crs(epsg=3857)

# Buffer using geopanda's "buffer" tool 
# Create buffers around POIs (e.g., 1000 meters = 1 km)
pois_gpd['buffer'] = pois_gpd.geometry.buffer(1000)

# Plot everything
fig, ax = plt.subplots(figsize=(12, 12))

# Plot POI buffers (light blue, transparent)
pois_gpd['buffer'].plot(ax=ax, color='lightblue', alpha=0.5, label='1km Buffers')

# Plot POIs (red points)
pois_gpd.plot(ax=ax, color='red', markersize=50, label='Points of Interest')

# Annotate POIs with their names
for x, y, label in zip(pois_gpd.geometry.x, pois_gpd.geometry.y, pois_gpd['name']):
    ax.text(x + 100, y + 100, label, fontsize=9)

plt.legend()
plt.title("Points of Interest with Buffers")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis('equal')  # Equal scaling
plt.show()

# %%
# task plot points, buffer the points by 1000 meters, add buffered points and polygons on matplotlib 

from geodatasets import get_path
from shapely.geometry import Point

# points 

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
pois_gpd = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)

# Project points to match nybb CRS (EPSG:3857)
pois_gpd = pois_gpd.to_crs(epsg=3857)

# Create buffers around POIs (e.g., 1000 meters = 1 km)
pois_gpd['buffer'] = pois_gpd.geometry.buffer(1000)

#################
# polygons 

# Load NY boroughs from geodatasets
path_to_nybb = get_path('nybb')
nybb = gpd.read_file(path_to_nybb)

# Project to EPSG:3857 (meters) for accurate spatial analysis
nybb = nybb.to_crs(epsg=3857)

# Dissolve all boroughs into a single polygon (NYC boundary)
nyc_boundary = nybb.dissolve()

# Plot everything
fig, ax = plt.subplots(figsize=(12, 12))

# Plot boroughs with light green
nybb.plot(ax=ax, color='lightgreen', edgecolor='black', label='Boroughs')

# Plot merged NYC boundary with red border
nyc_boundary.plot(ax=ax, color='none', edgecolor='red', linewidth=3, label='Merged Boundary')

# Plot POI buffers (light blue, transparent)
pois_gpd['buffer'].plot(ax=ax, color='lightblue', alpha=0.5, label='1km Buffers')

# Plot POIs (red points)
pois_gpd.plot(ax=ax, color='red', markersize=50, label='Points of Interest')

# Annotate POIs with their names
for x, y, label in zip(pois_gpd.geometry.x, pois_gpd.geometry.y, pois_gpd['name']):
    ax.text(x + 100, y + 100, label, fontsize=9)

plt.legend()
plt.title("NYC Boroughs, Merged Boundary, and Synthetic Points of Interest with Buffers")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis('equal')  # Equal scaling
plt.show()

# %%


# %%
# Import necessary libraries
import folium
import geopandas as gpd
from shapely.geometry import Point

# Create synthetic points of interest (lat, lon approx locations within NYC)
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
pois_gpd = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)

# Project points to match nybb CRS (EPSG:3857)
pois_gpd = pois_gpd.to_crs(epsg=3857)

pois_gpd.head(3)





# Display the map
#m


# %%


# %%


######## 2025-06-23 10:44 
# Import necessary libraries
import folium
import geopandas as gpd
from shapely.geometry import Point

# Create synthetic points of interest (lat, lon approx locations within NYC)
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
pois_gpd = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)

# Project points to match nybb CRS (EPSG:3857)
pois_gpd = pois_gpd.to_crs(epsg=3857)

# Create Folium map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add points to the map
for index, row in pois_gpd.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name']
    ).add_to(m)

####
# Load NY boroughs dataset path and then read it with geopandas
path_to_nybb = get_path('nybb')
nybb = gpd.read_file(path_to_nybb)

# Folium uses lat/lng coordinates, ensure geometry is in WGS84 (EPSG:4326)
nybb = nybb.to_crs(epsg=4326)

# Add the borough polygons to the map with a simple style
folium.GeoJson(
    nybb,
    name='NY Boroughs',
    style_function=lambda feature: {
        'fillColor': '#blue',
        'color': 'gray',
        'weight': 2,
        'fillOpacity': 0.5,
    },
)#.add_to(m)

# Add buffer polygons to the map

pois_buffer_gpd = pois_gpd.geometry.buffer(100000)

folium.GeoJson(
        data=pois_buffer_gpd.to_json(),
    name='NY Boroughs',
    style_function=lambda feature: {
        'fillColor': '#blue',
        'color': 'red',
        'weight': 2,
        'fillOpacity': 0.5,
    },
).add_to(m)


# Save the map as an HTML file
m

# %%
# Plot boroughs with light green
nybb.plot(ax=ax, color='lightgreen', edgecolor='black', label='Boroughs')

# Plot merged NYC boundary with red border
nyc_boundary.plot(ax=ax, color='none', edgecolor='red', linewidth=3, label='Merged Boundary')

# Plot POI buffers (light blue, transparent)
pois_gpd['buffer'].plot(ax=ax, color='lightblue', alpha=0.5, label='1km Buffers')

# Plot POIs (red points)
pois_gpd.plot(ax=ax, color='red', markersize=50, label='Points of Interest')


# %%


# %%
import folium
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

# Create synthetic points of interest (lat, lon approx locations within NYC)
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
pois_gpd = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)

# Create Folium map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add points to the map
for index, row in pois_gpd.iterrows():
    folium.Marker(
        location=[row['geometry'].y, row['geometry'].x],
        popup=row['name']
    ).add_to(m)

# Add buffer polygons to the map
buffer_gpd = gpd.GeoDataFrame(
    geometry=[row.geometry.buffer(0.01) for index, row in pois_gpd.iterrows()],
    crs='EPSG:4326'
)

# Add buffer polygons to the map
for index, row in buffer_gpd.iterrows():
    # Convert polygon coordinates to list of lists for Folium
    polygon_coords = list(row.geometry.exterior.coords)
    
    folium.Polygon(
        locations=[(lat, lon) for lon, lat in polygon_coords],
        color='red',
        fill_color='red',
        fill_opacity=0.5,
        popup=pois_gpd.loc[index, 'name']
    ).add_to(m)

# Optional: Add borough data if you have the path
# Uncomment and modify as needed
# path_to_nybb = get_path('nybb')
# nybb = gpd.read_file(path_to_nybb)
# folium.GeoJson(
#     nybb,
#     name='NY Boroughs',
#     style_function=lambda feature: {
#         'fillColor': 'blue',
#         'color': 'gray',
#         'weight': 2,
#         'fillOpacity': 0.5,
#     },
# ).add_to(m)

# Save the map
m.save('nyc_map.html')

# Display the map (if in Jupyter notebook)
m

# %%


# %%


# %%


# %%
######## 2025-06-23 10:44 
# Import necessary libraries
import folium
import geopandas as gpd
from shapely.geometry import Point
# Create synthetic points of interest (lat, lon approx locations within NYC)
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
pois_gpd = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)
# Project points to match nybb CRS (EPSG:3857)
pois_gpd = pois_gpd.to_crs(epsg=3857)
# Create Folium map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
# Add points to the map
for index, row in pois_gpd.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name']
    ).add_to(m)
####
# Load NY boroughs dataset path and then read it with geopandas
path_to_nybb = get_path('nybb')
nybb = gpd.read_file(path_to_nybb)
# Folium uses lat/lng coordinates, ensure geometry is in WGS84 (EPSG:4326)
nybb = nybb.to_crs(epsg=4326)
# Add the borough polygons to the map with a simple style
folium.GeoJson(
    nybb,
    name='NY Boroughs',
    style_function=lambda feature: {
        'fillColor': '#blue',
        'color': 'gray',
        'weight': 2,
        'fillOpacity': 0.5,
    },
).add_to(m)



# Add buffer polygons to the map
buffer_gpd = gpd.GeoDataFrame(
    geometry=[row.geometry.buffer(10000) for index, row in pois_gpd.iterrows()],
    crs='EPSG:4326'
)
buffer_gpd = buffer_gpd.to_crs(epsg=3857)
for index, row in buffer_gpd.iterrows():
    folium.Polygon(
        row.geometry.exterior.coords[:-1],
        color='red',
        fill_color='red',
        fill_opacity=0.5
    ).add_to(m)

# Save the map as an HTML file
m

# %%


# %%


# %%


# %%


# %%


# %%
import folium
nycmap = folium.Map(location=[40.69, -74.14],
    zoom_start=12,
    control_scale=True)
# loop through points
for index, row in pois_gpd.iterrows():
    folium.CircleMarker(location=[ row.latitude,row.longitude], radius =5).add_to(nycmap)

# add polygons to the map
#for index, row in nybb.iterrows():
    #folium.GeoJson(row.geometry.__geo_interface__, name='NYC Burroughs').add_to(nycmap)


# add polygons to the map
for index, row in pois_gpd['buffer'].iterrows():
    folium.GeoJson(row.geometry.__geo_interface__, name='NYC Burroughs').add_to(nycmap)




nycmap

# %%
import folium
nycmap = folium.Map(location=[40.69, -74.14],
    zoom_start=11,
    control_scale=True)
# loop through points
for index, row in pois_gpd.iterrows():
    folium.CircleMarker(location=[ row.latitude,row.longitude], radius =5).add_to(nycmap)

#for index, row in pois_gpd['buffer'].iterrows():
#    folium.CircleMarker(location=[ row.latitude,row.longitude], color = 'gray',fill=True, fill_opacity=1).add_to(map)


# add polygons to the map
for index, row in nybb.iterrows():
    folium.GeoJson(row.geometry.__geo_interface__, name='NYC Burroughs').add_to(nycmap)


# Plot boroughs with light green
#nybb.plot(ax=ax, color='lightgreen', edgecolor='black', label='Boroughs')

# Plot merged NYC boundary with red border
#nyc_boundary.plot(ax=ax, color='none', edgecolor='red', linewidth=3, label='Merged Boundary')

# Plot POI buffers (light blue, transparent)
#pois_gpd['buffer'].plot(ax=ax, color='lightblue', alpha=0.5, label='1km Buffers')

# Plot POIs (red points)
#pois_gpd.plot(ax=ax, color='red', markersize=50, label='Points of Interest')


nycmap

# %%
from geodatasets import get_path
from shapely.geometry import Point

# add polygons and plot everything 

# Project points to match nybb CRS (EPSG:3857)

# Load NY boroughs from geodatasets

from geodatasets import get_path
from shapely.geometry import Point

# task 4, add points of interest and polygons to map 

# subtask buffer the points by 1000 meters 

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
pois_gpd = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)

# Project points to match nybb CRS (EPSG:3857)
pois_gpd = pois_gpd.to_crs(epsg=3857)

# Create buffers around POIs (e.g., 1000 meters = 1 km)
pois_gpd['buffer'] = pois_gpd.geometry.buffer(1000)

# Plot everything
fig, ax = plt.subplots(figsize=(12, 12))

# Plot boroughs with light green
nybb.plot(ax=ax, color='lightgreen', edgecolor='black', label='Boroughs')

# Plot merged NYC boundary with red border
nyc_boundary.plot(ax=ax, color='none', edgecolor='red', linewidth=3, label='Merged Boundary')

# Plot POI buffers (light blue, transparent)
pois_gpd['buffer'].plot(ax=ax, color='lightblue', alpha=0.5, label='1km Buffers')

# Plot POIs (red points)
pois_gpd.plot(ax=ax, color='red', markersize=50, label='Points of Interest')

# Annotate POIs with their names
for x, y, label in zip(pois_gpd.geometry.x, pois_gpd.geometry.y, pois_gpd['name']):
    ax.text(x + 100, y + 100, label, fontsize=9)

plt.legend()
plt.title("NYC Boroughs, Merged Boundary, and Synthetic Points of Interest with Buffers")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis('equal')  # Equal scaling
plt.show()

# Load NY boroughs from geodatasets
path_to_nybb = get_path('nybb')
nybb = gpd.read_file(path_to_nybb)

# Project to EPSG:3857 (meters) for accurate spatial analysis
nybb = nybb.to_crs(epsg=3857)

# Dissolve all boroughs into a single polygon (NYC boundary)
nyc_boundary = nybb.dissolve()

# Create GeoDataFrame of points
pois_gpd = gpd.GeoDataFrame(
    poi_data,
    geometry=[Point(xy) for xy in zip(poi_data['longitude'], poi_data['latitude'])],
    crs='EPSG:4326'  # initial CRS
)

# Project points to match nybb CRS (EPSG:3857)
pois_gpd = pois_gpd.to_crs(epsg=3857)

# Create buffers around POIs (e.g., 1000 meters = 1 km)
pois_gpd['buffer'] = pois_gpd.geometry.buffer(1000)

# Plot everything
fig, ax = plt.subplots(figsize=(12, 12))

# Plot boroughs with light green
nybb.plot(ax=ax, color='lightgreen', edgecolor='black', label='Boroughs')

# Plot merged NYC boundary with red border
nyc_boundary.plot(ax=ax, color='none', edgecolor='red', linewidth=3, label='Merged Boundary')

# Plot POI buffers (light blue, transparent)
pois_gpd['buffer'].plot(ax=ax, color='lightblue', alpha=0.5, label='1km Buffers')

# Plot POIs (red points)
pois_gpd.plot(ax=ax, color='red', markersize=50, label='Points of Interest')

# Annotate POIs with their names
for x, y, label in zip(pois_gpd.geometry.x, pois_gpd.geometry.y, pois_gpd['name']):
    ax.text(x + 100, y + 100, label, fontsize=9)

plt.legend()
plt.title("NYC Boroughs, Merged Boundary, and Synthetic Points of Interest with Buffers")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis('equal')  # Equal scaling
plt.show()



