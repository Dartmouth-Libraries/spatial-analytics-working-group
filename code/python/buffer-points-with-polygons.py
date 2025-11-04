# tasks:
#   plot points, 
#   buffer points by a given distance, buffer the points by 1000 meters 
#   plot buffered points and polygons on matplotlib 

#pip install geodatasets

import matplotlib.pyplot as plt
import pandas as pd

import geopandas as gpd

from geodatasets import get_path
from shapely.geometry import Point

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

# Project the points to match nybb CRS (EPSG:3857)
pois_gpd = pois_gpd.to_crs(epsg=3857)

# Create buffers around POIs (e.g., 1000 meters = 1 km)
pois_gpd['buffer'] = pois_gpd.geometry.buffer(1000)

#################
# polygons 

# Load the geodatasets library with built in datasets,  NY boroughs (polygon)
path_to_nybb = get_path('nybb')
nybb = gpd.read_file(path_to_nybb)

# Project to EPSG:3857 (meters) for accurate spatial analysis
nybb = nybb.to_crs(epsg=3857)

# Dissolve all boroughs into a single polygon (NYC boundary)
nyc_boundary = nybb.dissolve()

# Plot 
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

# add map elements, legend, title, coordinate system axes
plt.legend()
plt.title("NYC Boroughs, Merged Boundary, and Synthetic Points of Interest with Buffers")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.axis('equal')  # Equal scaling
plt.show()





#### 
# For folium mapping 
# !pip install folium geopandas shapely pyproj

import folium
import geopandas as gpd
from shapely.geometry import mapping

# 1) Make sure everything is a GeoDataFrame and in WGS84 (EPSG:4326) for Folium
def to_gdf(g):
    if isinstance(g, gpd.GeoSeries):
        return gpd.GeoDataFrame(geometry=g, crs=g.crs)
    return g

nybb = to_gdf(nybb)
nyc_boundary = to_gdf(nyc_boundary)
pois_gpd = to_gdf(pois_gpd)

# Build a GDF for buffers from the 'buffer' column
buffer_gdf = gpd.GeoDataFrame(pois_gpd.drop(columns='geometry', errors='ignore'),
                              geometry=pois_gpd['buffer'],
                              crs=pois_gpd.crs)

# Reproject to EPSG:4326 for Folium (if not already)
def to_wgs84(gdf):
    if gdf.crs is None:
        # If CRS is missing, set it before converting (adjust if needed)
        # gdf = gdf.set_crs("EPSG:2263")  # Example for NY State Plane meters
        raise ValueError("CRS is not set on a GeoDataFrame. Set gdf.crs before converting.")
    return gdf.to_crs(epsg=4326)

nybb_wgs = to_wgs84(nybb)
nyc_boundary_wgs = to_wgs84(nyc_boundary)
buffer_wgs = to_wgs84(buffer_gdf)
pois_wgs = to_wgs84(pois_gpd)

# 2) Create the map centered on NYC bounds
# Use merged bounds of all layers for a good initial view
def bounds_union(gdfs):
    minxs, minys, maxxs, maxys = zip(*[g.total_bounds for g in gdfs])
    return [[min(minys), min(minxs)], [max(maxys), max(maxxs)]]

m = folium.Map(tiles="CartoDB positron", zoom_start=11)
m.fit_bounds(bounds_union([nybb_wgs, nyc_boundary_wgs, buffer_wgs, pois_wgs]))




# POIs (red points) with labels
for _, row in pois_wgs.iterrows():
    geom = row.geometry
    if geom is None or geom.is_empty:
        continue
    folium.CircleMarker(
        location=[geom.y, geom.x],
        radius=6,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=1.0,
        popup=str(row.get("name", "POI")),
        tooltip=str(row.get("name", "POI")),
    ).add_to(m)



folium.LayerControl(collapsed=False).add_to(m)

m



