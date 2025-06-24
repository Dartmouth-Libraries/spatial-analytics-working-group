import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from libpysal.weights import KNN
from esda import G_Local
import folium

# Set random seed
np.random.seed(123)

# Generate 50 random points near Boston
n_points = 50
boston_center = (-71.0589, 42.3601)  # lon, lat
radius = 0.1  # degrees, approx 11 km
longitudes = np.random.uniform(boston_center[0] - radius, boston_center[0] + radius, n_points)
latitudes = np.random.uniform(boston_center[1] - radius, boston_center[1] + radius, n_points)
values = np.random.normal(size=n_points)

# Create GeoDataFrame
df = pd.DataFrame({'longitude': longitudes, 'latitude': latitudes, 'value': values})
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Project to a metric CRS for accurate distance neighbor calculations (e.g., UTM zone 19N for Boston)
# EPSG 32619 corresponds to UTM zone 19N
gdf_utm = gdf.to_crs(epsg=32619)

# Calculate 4-nearest neighbors spatial weights using libpysal
coords = np.array([(point.x, point.y) for point in gdf_utm.geometry])
knn = KNN.from_array(coords, k=4)

# Compute Getis-Ord G* statistic (local G)
g_star = G_Local(gdf_utm['value'].values, knn, transform='r')

# Add results to GeoDataFrame
gdf_utm['G_star'] = g_star.Zs
gdf_utm['significant'] = (gdf_utm['G_star'] > 1.96) | (gdf_utm['G_star'] < -1.96)

# Reproject back to WGS84 for folium mapping
gdf = gdf_utm.to_crs(epsg=4326)

# Create folium map centered at Boston
m = folium.Map(location=[boston_center[1], boston_center[0]], zoom_start=12)

# Define colors for significant and non-significant points
def color_point(significant, g_star_val):
    if significant:
        # Hotspot (significant)
        return 'red' if g_star_val > 1.96 else 'blue'  # Red = high values hotspot, Blue = low values hotspot
    else:
        return 'gray'

# Add points to the folium map
for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=6,
        color=color_point(row['significant'], row['G_star']),
        fill=True,
        fill_opacity=0.7,
        popup=(f"Value: {row['value']:.2f}<br>"
               f"G*: {row['G_star']:.2f}<br>"
               f"Significant: {row['significant']}")
    ).add_to(m)

# Display the map (in notebook) or save
m.save('getis_ord_folium_map.html')
m  # If in Jupyter notebook this will display the map inline
