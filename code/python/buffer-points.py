# task add points and buffer the points by 1000 meters 
import pandas as pd
import geopandas as gpd 
import matplotlib.pyplot as plt 
from shapely.geometry import Point

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

# use shapely's "Point" tool with geopandas 
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
