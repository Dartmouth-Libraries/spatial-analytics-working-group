# %%
#!pip install contextily
#!pip install geodatasets
#!pip install geopandas
# install successful
#!pip install pysal

# %% [markdown]
# # Introduction to Spatial and Geospatial Concepts & Analysis (part 1)
# # Spatial Analysis mini-project (part 2) 
# ## Python spatial analysis and mapping libraries  
# 
# ## Table of Contents
# 1. [Introduction](#intro)
# 2. [Setting Up Your Environment](#setup)
# 3. [Basic GIS Concepts](#gisconcepts)
# 4. [Python Libraries for Geospatial Analysis](#pylib)
# 5. [Three Basic Python Examples](#examples)
# 6. [Further Reading](#furtherreading)
# 
# <a name="intro"></a>
# 
# ## Introduction
# Welcome to this 1-hour introduction to geospatial analysis! In this tutorial, we'll cover some essential concepts and practice them using Python libraries in Google Colab.
# 
# <a name="setup"></a>
# 
# ## Setting Up Your Environment
# You'll need to have a Google account to access Google Colab.
# 
# 1. Open the link https://colab.research.google.com/ in your web browser.
# 2. To install required libraries, run this cell:
# 
# ```python
# !pip install geopandas==0.8.0 shapely fiona rasterio numpy pandas matplotlib seaborn folium
# ```
# 
# <a name="gisconcepts"></a>
# 
# ## Basic GIS Concepts
# In this section, we'll briefly discuss some key concepts that are fundamental to geospatial analysis:
# 
# 1. Projection Systems (CRS) - a mathematical function that transforms locations from one coordinate system to another.
# 2. Raster and Vector Data - represent geographic data on a continuous or composed of discrete elements respectively.
# 3. Geometry - the shapes used by GIS applications, like points, lines, polygons, and surfaces.
# 4. Coordinate Systems - systems that allow us to specify locations on the earth's surface using coordinates (e.g., latitude and longitude or UTM).
# 
# 
# 
# <a name="pylib"></a>
# 
# ## Python Libraries for Geospatial Analysis
# The main libraries we will use in this tutorial are:
# 1. geopandas - manipulation, analysis, and visualization of vector data.
# 2. shapely - a library for computational geometry used to create geometric objects like points, lines, and polygons that define the geographic features.
# 3. rasterio & numpy - managing raster data.
# 4. folium - interactive maps generation.
# 
# <a name="examples"></a>
# 
# ## Three Basic Python Examples
# 
# ### 1) Loading and Visualizing a Shapefile (Vector Data) with Geopandas
# 
# Create a new cell and paste this code:
# 
# ```python
# import geopandas as gpd
# 
# # Load shapefile using geopandas
# states = gpd.read_file('path/to/your/shapefile/countries.shp')
# 
# # Plot the map
# states.plot(column='NAME', categorize=True, figsize=(12, 6))
# ```
# 
# Replace `'path/to/your/shapefile/countries.shp'` with a valid shapefile path in your Google Drive.
# 
# ### 2) Performing Spatial Operations (Point-in-Polygon Operation)
# 
# Create another cell and paste this code:
# 
# ```python
# # Read a new shapefile (populated places)
# places = gpd.read_file('path/to/your/shapefile/places.shp')
# 
# # Determine the polygon containing each point based on spatial relationships
# points = gpd.GeoSeries([(10, -85)])  # Replace (10, -85) with a point in the map's coordinate system
# places['IN_places'] = places.within(points)  # Add boolean column indicating which polygon contains each point
# ```
# 
# ### 3) Reading and Plotting Raster Data with Rasterio & Folium
# 
# Create one last cell and paste this code:
# 
# ```python
# import rasterio as rio
# from folium.plugins import quicklook
# 
# # Open a raster and define its coordinates
# with rio.open('path/to/your/raster-files/image.tif') as src:
#     img = src.read(1)  # Load the first band of a multi-band image
#     img = np.flipud(img)  # Flip the image upside down because rasterio writes images bottom to top by default
#     xmin, ymin, xmax, ymax = src.bounds  # Get the bounding box
# 
# # Create a quicklook plugin and add it to a map
# map = folium.Map(location=[(ymin + xmin) / 2, (ymax + ymin) / 2], tiles='cartodbpositron')
# quicklook(src, map=map, plot=True, overlay=True)
# ```
# 
# Replace `'path/to/your/raster-files/image.tif'` with a valid raster file path in your Google Drive.
# 
# <a name="furtherreading"></a>
# 
# ## Further Reading
# If you're eager to learn more about geospatial data analysis using Python, try the following resources:
# 1. [The Geopandas Cookbook](https://geopandas.org/cookbook.html)
# 2. [Python for Spatial Data Science](https://gis.stackexchange.com/q/93098/59476) on GIS.SE
# 3. [Rasterio Manual](https://rasterio.readthedocs.io/en/latest/index.html)
# 

# %%
#add: 
   # plot xy
   # xy to leaflet map
   # buffer 1 mile 
   # buffer merge clip 

# %%
import pandas as pd
import matplotlib.pyplot as plt


# %%
# Task #1 
# Import necessary libraries
import folium

# Create a Map centered over Grand Central Station
map = folium.Map(location=[40.7488, -73.9857], tiles="openstreetmap")  
map

# %%
# Task #2 
# add a point 

# Create a marker for Grand Central Station and its Popup contents
marker = folium.Marker([40.7488, -73.9857], popup="Grand Central Station", tooltip="Grand Central Marker")  # Add an icon (optional)

# Add the marker to the Map
map.add_child(marker)
map

# %%

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

# %%
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

# %%



# Some common tools include 
#  Buffer, Clip, Merge, Dissolve, Intersect, Union, Erase, Spatial Join, Extract by Mask, and Reclassify



# %%
# task 5 import dataset of points 

#!pip install geopandas
#!pip install shapely
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely

# %%

# import a CSV that contains latitude and longitude coordinate pairs 
points = pd.read_csv("https://rcweb.dartmouth.edu/homes/f002d69/workshops/data/bear-sightings.csv")
points.head(3)



# %%

# convert points from latitude longitude to a 'geopandas' spatial data frame 
points = gpd.GeoDataFrame(points, geometry=gpd.points_from_xy(points.longitude, points.latitude))
points.head(2)

# %%
# quick visualization to check the points 
points.plot()
plt.show()

# %%

# task # ___ load polygon shapefile into geopandas 

# NOTE: zip file containing a 'shapefile', which actually has several files within the zipfile
  # these include files .shp, .prj, .dbf, .shx, .cpg 
# function delete for backspace / del 
zipfile_url = "https://rcweb.dartmouth.edu/homes/f002d69/workshops/data/nationalparks_ak.zip"
polygons = gpd.read_file(zipfile_url)
print(gdf.head())




# %%
# quick viz of polygons 

polygons.plot()
plt.show()

# %%


# %%


# %%
# set crs 
points.crs='EPSG:4326'
points = points.to_crs(polygons.crs)
points.crs.to_epsg()

# %%
# intersect / spatial join / overlay 
points_in_polygons = gpd.sjoin(points, polygons, predicate='within')
points_in_polygons.head(2)

# %%
# basic visualization of results using matplotlib  
polygons.plot(facecolor='none')
points.plot(ax=plt.gca())
points_in_polygons.plot(color='red',ax=plt.gca())
plt.axis("off")
plt.show()

# %%
# advanced vis using folium / leaflet / open street map 
# https://geopandas.org/en/stable/gallery/plotting_with_folium.html
# create a folium map, complete with in-notebook zoom tools
map = folium.Map(location=[62.65822, -148.95602],
    zoom_start=5,
    control_scale=True)
# loop through points
for index, row in points.iterrows():
    folium.CircleMarker(location=[ row.latitude,row.longitude], radius =5).add_to(map)
# loop through points in polygons, color them gray
for index, row in points_in_polygons.iterrows():
    folium.CircleMarker(location=[ row.latitude,row.longitude], color = 'gray',fill=True, fill_opacity=1).add_to(map)
map


# %%
# task # ____

from shapely.geometry import Point

# NYC coordinates
latitude = 40.7128
longitude = -74.0060

# Buffer distance in meters
buffer_distance = 5656248 * 2        # 2 miles buffer for New York City

# Create the Point object
nyc_point = Point(latitude, longitude)

# Buffer the point by desired distance and create a Polygon object
buffered_nyc = nyc_point.buffer(buffer_distance)

print("Buffered NYC shape:", buffered_nyc)




# %%


# %%


# %%
# task # __  - clip 
# https://geopandas.org/en/stable/gallery/plot_clip.html

import matplotlib.pyplot as plt
import geopandas
from shapely.geometry import box
import geodatasets



# %%
chicago = geopandas.read_file(geodatasets.get_path("geoda.chicago_commpop"))
groceries = geopandas.read_file(geodatasets.get_path("geoda.groceries")).to_crs(chicago.crs)

# Create a subset of the Chicago data that is just the South American continent
near_west_side = chicago[chicago["community"] == "NEAR WEST SIDE"]

# Create a custom polygon
polygon = box(-87.8, 41.90, -87.5, 42)
poly_gdf = geopandas.GeoDataFrame([1], geometry=[polygon], crs=chicago.crs)

# %%
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
chicago.plot(ax=ax1)
poly_gdf.boundary.plot(ax=ax1, color="red")
near_west_side.boundary.plot(ax=ax2, color="green")
groceries.plot(ax=ax2, color="purple")
ax1.set_title("All Unclipped Chicago Communities", fontsize=20)
ax2.set_title("All Unclipped Groceries", fontsize=20)
ax1.set_axis_off()
ax2.set_axis_off()
plt.show()

# %%
chicago_clipped = chicago.clip(polygon)

# Plot the clipped data
# The plot below shows the results of the clip function applied to the chicago
# sphinx_gallery_thumbnail_number = 2
fig, ax = plt.subplots(figsize=(12, 8))
chicago_clipped.plot(ax=ax, color="purple")
chicago.boundary.plot(ax=ax)
poly_gdf.boundary.plot(ax=ax, color="red")
ax.set_title("Chicago Clipped", fontsize=20)
ax.set_axis_off()
plt.show()

# %%


# %%


# %%


# %%
import folium
from shapely.geometry import Point

# Set up the initial map view, add a base layer and create markers
map_center = (40.7128, -74.0060)     # NYC coordinates
map_zoom = 12                        # Zoom level for the initial map
base_map_style = folium.TileLayer("CartoDB dark_all", attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>')
markers = [
   ('NYC location', map_center, 'info-sign', 'red'),
   ('2-mile Buffer', (0,0))         # Placeholder location for initializing buffered polygon later
]
map = folium.Map(location=map_center, zoom_start=map_zoom, tiles=base_map_style)
markers[1][1] = map.create_child_marker([], data={'icon_data': markers[1][2]}, text='Buffered area around NYC', maxWidth=200, popup = True).get_position()     # Initializing buffered polygon's position
markers[1]['text'] = "Buffered area around NYC"                                # Changing the marker label

# Create the Point object
nyc_point = Point(*map_center)

# Calculate and buffer the Point to a Polygon (2 miles buffer)
buffer_distance = 5656248 * 2    # 2 miles buffer for New York City
buffered_nyc = nyc_point.buffer(buffer_distance)
folium._geodesic_marker(buffered_nyc.representative_point, icon=markers[1]['icon_data'], text=markers[1]['text'])  # Adding the buffered polygon to the map
buffered_nyc.to_leaflet(zbuffer = -2).add_child(folium._geodesic_polygon()).show()        # Creating custom styles for the buffered polygon and changing its transparency

# Save and show the map
map.save("NYCBufferMap.html")      # Not including this part in the following examples if you prefer running code in a web-browser directly

# %%


# %%


# %%


# %%
polygons.plot()
points.plot()
plt.show()

# %%
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Assuming points is a DataFrame with columns 'longitude' and 'latitude', create two GeoDataFrames.
points = gpd.GeoDataFrame(points, geometry=[Point(xy) for xy in zip(points['longitude'], points['latitude'])])
points2 = gpd.GeoDataFrame(points, geometry=[Point(xy) for xy in zip(points['longitude'], points['latitude'])])

# Create subplots to visualize overlapping GeoDataFrames
fig, ax = plt.subplots()
points.plot(ax=ax, color='r', alpha=0.95) # Plot the first GeoDataFrame with 50% transparency
points2.plot(ax=ax, color='b', alpha=0.75) # Plot the second GeoDataFrame with 75% transparency
plt.show()

# %%
polygons.plot(ax=ax, fill=True, edgecolor='none', ) # alpha=polygons['outer_alpha'], zorder=-1)
points.plot(ax=ax, color='r', alpha=0.95, zorder=2) # Plot the first GeoDataFrame with 50% transparency
points2.plot(ax=ax, color='b', alpha=0.75, zorder=3) # Plot the second GeoDataFrame with 75% transparency
plt.show()

# %%


# %%


# %%

# more geospatial libraries to explore: 
import pysal as ps
from pysal.lib import examples

#GeoPandas: Extends Pandas DataFrames to handle geometric types, enabling spatial operations on vector data.
#Shapely: A library for planar geometric objects and operations.
#Fiona: Reads and writes various vector geospatial data formats, acting as a Python interface to OGR.
#Rasterio: Reads and writes raster geospatial data formats, acting as a Python interface to GDAL.
#GDAL/OGR (via osgeo): The fundamental library for geospatial data translation and processing, often accessed through Python bindings.
#Pyproj: Performs cartographic transformations and geodetic calculations.
#Xarray: A powerful library for working with labeled multi-dimensional arrays, particularly useful for raster data.
#Rioxarray: Extends Xarray with capabilities for geospatial raster data.

#Visualization & Interactive Mapping:
#Folium: Creates interactive Leaflet maps from Python.
#Matplotlib: A foundational plotting library, used for static geospatial visualizations.
Geoplotlib: A library specifically designed for visualizing geographical data.
#Datashader: For rendering large datasets quickly, including geospatial data.
#Cartopy: A library for cartographic projections and drawing maps, often used with Matplotlib.

#Specialized & Advanced Applications:
#ArcPy (for ArcGIS users): A Python package for performing geographic data analysis, conversion, management, and automation within ArcGIS.
#EarthPy: Simplifies working with spatial data in Python, especially for earth science data.
#Pysal: A library for spatial analysis, including spatial econometrics and spatial statistics.
#Geopy: Provides geocoding services, allowing conversion between addresses and geographic coordinates.


# %%
import geopandas as gpd
from shapely.geometry import Point, mapping, shape
import fiona
from folium import Map, Choropleth

#from shapely.ops import unary_union, buffer




# %%


# %%
# Alternative 1: Using PySAL for sample data
import pysal as ps
import geopandas as gpd

# Load the NYC census tracts dataset
nyc = gpd.read_file(ps.examples.get_path('nyc_census_tracts.shp'))
print(nyc.head())

# Alternative 2: Using scikit-learn's sample datasets
from sklearn.datasets import fetch_california_housing
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load California housing dataset
housing = fetch_california_housing()
df = pd.DataFrame(housing.data, columns=housing.feature_names)
df['target'] = housing.target  # median house values

# Create a GeoDataFrame (the dataset includes longitude and latitude)
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
print(gdf.head())

# %%
from libpysal.examples import get_path


# %%
get_path("mexicojoin.dbf")


# %%
import libpysal
from libpysal.examples import load_example
import geopandas
#
tampa1 = load_example('Tampa1')
tampa_counties_shp = tampa1.load('tampa_counties.shp')
tampa_df = geopandas.read_file(tampa1.get_path('tampa_counties.shp'))
%matplotlib inline
tampa_df.plot()
tampa_df.head()


# %%


# %%
pip install mapclassify

# %%
# Web Mapping with LibPysal and Folium
# ====================================

# Install required packages
!pip install libpysal folium geopandas mapclassify

# Import libraries
import numpy as np
import pandas as pd
import geopandas as gpd
import libpysal
import folium
import matplotlib.pyplot as plt
from libpysal.examples import load_example
#from mapclassify import Quantiles, Equal_Interval, Fisher_Jenks
from folium.plugins import MarkerCluster

# Introduction to the tutorial
print("="*80)
print("WEB MAPPING WITH LIBPYSAL AND FOLIUM")
print("="*80)
print("""
This tutorial will teach you how to:
1. Load geospatial data from LibPysal examples
2. Explore and understand the data structure
3. Create interactive web maps using Folium
4. Apply different choropleth mapping techniques
5. Add layers, markers, and popups to maps
6. Customize map styles and features
""")

# PART 1: LOADING DATA FROM LIBPYSAL
print("\n" + "="*80)
print("PART 1: LOADING DATA FROM LIBPYSAL")
print("="*80)

# Show available examples in libpysal
print("Available example datasets in LibPysal:")
available_examples = libpysal.examples.available()
for i, example in enumerate(available_examples[:10], 1):
    print(f"{i}. {example}")
print("... and more")

# Load a common example: US county data
print("\nLoading the 'us_counties' example dataset...")
us_counties = load_example('us_counties')

print("\nExample dataset information:")
print(f"- Description: {us_counties.description}")
print(f"- Data files: {us_counties.get_file_list()}")

# Load the shapefile using geopandas
counties_path = us_counties.get_path("us_counties.shp")
counties = gpd.read_file(counties_path)

print("\nDataset preview:")
display(counties.head())

print("\nData columns:")
for col in counties.columns:
    print(f"- {col}")

print("\nGeometry type:", counties.geometry.geom_type.iloc[0])
print("CRS:", counties.crs)

# %%


# PART 2: BASIC FOLIUM MAP
print("\n" + "="*80)
print("PART 2: BASIC FOLIUM MAP")
print("="*80)

print("""
Folium is a Python library that allows you to create interactive Leaflet maps.
It combines the data manipulation capabilities of Python with the mapping
strengths of Leaflet.js.
""")

# Create a basic map centered on the US
m1 = folium.Map(
    location=[39.8283, -98.5795],  # Center of the US
    zoom_start=4,
    tiles='CartoDB positron'
)

# Add a title
title_html = '''
<h3 align="center" style="font-size:16px"><b>Basic US Map</b></h3>
'''
m1.get_root().html.add_child(folium.Element(title_html))

# Display the map
display(m1)

print("""
The map above is a basic Folium map centered on the United States.
Key elements of a Folium map:
- location: Center coordinates [latitude, longitude]
- zoom_start: Initial zoom level
- tiles: Base map style (many options available)
""")

# PART 3: CHOROPLETH MAPPING
print("\n" + "="*80)
print("PART 3: CHOROPLETH MAPPING")
print("="*80)

print("""
Choropleth maps use color to represent data values in different geographic areas.
We'll create a choropleth map of population density by county.
""")

# Calculate population density
counties['pop_density'] = counties['POPULATION'] / counties['AREA']

# Create a choropleth map
m2 = folium.Map(
    location=[39.8283, -98.5795],
    zoom_start=4,
    tiles='CartoDB positron'
)

# Add choropleth layer
folium.Choropleth(
    geo_data=counties,
    name='Population Density',
    data=counties,
    columns=['FIPS', 'pop_density'],
    key_on='feature.properties.FIPS',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population Density (people per square unit)',
    highlight=True,
    bins=8
).add_to(m2)

# Add layer control
folium.LayerControl().add_to(m2)

# Add title
title_html = '''
<h3 align="center" style="font-size:16px"><b>US County Population Density</b></h3>
'''
m2.get_root().html.add_child(folium.Element(title_html))

# Display the map
display(m2)

print("""
Key elements of a choropleth map:
- geo_data: The GeoDataFrame with geometry
- data: The DataFrame with values
- columns: The columns for joining and values
- key_on: The field in the GeoJSON to match the column in the data
- fill_color: The colormap to use
- bins: Number of color categories
""")

# PART 4: DIFFERENT CLASSIFICATION METHODS
print("\n" + "="*80)
print("PART 4: DIFFERENT CLASSIFICATION METHODS")
print("="*80)

print("""
Classification methods determine how data is grouped into categories.
Different methods can highlight different patterns in your data.
""")

# Create a subset for better visualization
subset_states = ['NY', 'NJ', 'CT', 'MA', 'RI', 'NH', 'VT', 'ME', 'PA']
northeast = counties[counties['STATE_NAME'].isin(subset_states)].copy()

# Calculate the center of the northeast region
ne_center = [
    northeast.geometry.centroid.y.mean(),
    northeast.geometry.centroid.x.mean()
]

# Create three different classification schemes
q5 = Quantiles(northeast['pop_density'], k=5).bins
ei5 = Equal_Interval(northeast['pop_density'], k=5).bins
fj5 = Fisher_Jenks(northeast['pop_density'], k=5).bins

# Function to create a map with a specific classification
def create_classified_map(data, bins, title, scheme_name):
    m = folium.Map(
        location=ne_center,
        zoom_start=6,
        tiles='CartoDB positron'
    )

    folium.Choropleth(
        geo_data=data,
        name=f'Population Density ({scheme_name})',
        data=data,
        columns=['FIPS', 'pop_density'],
        key_on='feature.properties.FIPS',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Population Density ({scheme_name})',
        bins=bins
    ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Add title
    title_html = f'''
    <h3 align="center" style="font-size:16px"><b>{title}</b></h3>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    return m

# Create maps with different classification schemes
m_q5 = create_classified_map(northeast, q5, 'Northeast Population Density (Quantiles)', 'Quantiles')
m_ei5 = create_classified_map(northeast, ei5, 'Northeast Population Density (Equal Interval)', 'Equal Interval')
m_fj5 = create_classified_map(northeast, fj5, 'Northeast Population Density (Fisher-Jenks)', 'Fisher-Jenks')

# Display the maps
print("Map with Quantiles Classification (5 classes):")
display(m_q5)

print("\nMap with Equal Interval Classification (5 classes):")
display(m_ei5)

print("\nMap with Fisher-Jenks Classification (5 classes):")
display(m_fj5)

print("""
Classification Methods Comparison:
1. Quantiles: Each class has the same number of features
2. Equal Interval: Each class has the same range of values
3. Fisher-Jenks: Minimizes variance within classes, maximizes variance between classes

The choice of classification method can significantly impact how patterns appear in your map.
""")

# PART 5: INTERACTIVE FEATURES
print("\n" + "="*80)
print("PART 5: INTERACTIVE FEATURES")
print("="*80)

print("""
Folium allows you to add interactive features like popups, tooltips, and markers.
Let's create a map with these features to enhance user interaction.
""")

# Create a map with interactive features
m3 = folium.Map(
    location=ne_center,
    zoom_start=6,
    tiles='CartoDB positron'
)

# Add a choropleth layer
choropleth = folium.Choropleth(
    geo_data=northeast,
    name='Population Density',
    data=northeast,
    columns=['FIPS', 'pop_density'],
    key_on='feature.properties.FIPS',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population Density',
    highlight=True
)
choropleth.add_to(m3)

# Add tooltips to the choropleth
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(
        fields=['NAME', 'STATE_NAME', 'POPULATION', 'AREA', 'pop_density'],
        aliases=['County:', 'State:', 'Population:', 'Area:', 'Population Density:'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )
)

# Add markers for state capitals (example data)
capitals = {
    'NY': {'name': 'Albany', 'loc': [42.6526, -73.7562]},
    'MA': {'name': 'Boston', 'loc': [42.3601, -71.0589]},
    'CT': {'name': 'Hartford', 'loc': [41.7658, -72.6734]},
    'RI': {'name': 'Providence', 'loc': [41.8240, -71.4128]},
    'NH': {'name': 'Concord', 'loc': [43.2081, -71.5376]},
    'VT': {'name': 'Montpelier', 'loc': [44.2601, -72.5754]},
    'ME': {'name': 'Augusta', 'loc': [44.3106, -69.7795]},
    'NJ': {'name': 'Trenton', 'loc': [40.2206, -74.7597]},
    'PA': {'name': 'Harrisburg', 'loc': [40.2732, -76.8867]}
}

# Create a marker cluster group
marker_cluster = MarkerCluster(name='State Capitals').add_to(m3)

# Add markers to the cluster
for state, info in capitals.items():
    folium.Marker(
        location=info['loc'],
        popup=f"<strong>{info['name']}</strong><br>Capital of {state}",
        tooltip=info['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(marker_cluster)

# Add custom features - a circle marker for a major city
folium.CircleMarker(
    location=[40.7128, -74.0060],
    radius=20,
    popup='<strong>New York City</strong>',
    tooltip='New York City',
    color='#3186cc',
    fill=True,
    fill_color='#3186cc'
).add_to(m3)

# Add a measure tool
folium.plugins.MeasureControl(
    position='topright',
    primary_length_unit='miles',
    secondary_length_unit='kilometers',
    primary_area_unit='acres',
    secondary_area_unit='sqmeters'
).add_to(m3)

# Add fullscreen option
folium.plugins.Fullscreen(
    position='topright',
    title='Full Screen',
    title_cancel='Exit Full Screen',
    force_separate_button=True
).add_to(m3)

# Add layer control
folium.LayerControl().add_to(m3)

# Add title
title_html = '''
<h3 align="center" style="font-size:16px"><b>Interactive Northeast US Map</b></h3>
'''
m3.get_root().html.add_child(folium.Element(title_html))

# Display the map
display(m3)

print("""
Interactive Features Added:
1. Tooltips: Hover over counties to see information
2. Popups: Click on markers to see more details
3. Marker Clusters: Group markers that are close together
4. Measure Tool: Calculate distances and areas
5. Fullscreen Button: Expand the map to full screen
6. Layer Control: Toggle different map layers

These interactive features enhance user engagement and allow for exploration of the data.
""")

# PART 6: ADVANCED EXAMPLE - MULTIPLE DATA LAYERS
print("\n" + "="*80)
print("PART 6: ADVANCED EXAMPLE - MULTIPLE DATA LAYERS")
print("="*80)

print("""
Let's create a more complex map that combines multiple data layers from different LibPysal examples.
This demonstrates how to overlay different types of spatial data.
""")

# Load another example dataset - Rio de Janeiro
rio = load_example('Rio')
rio_path = rio.get_path('Rio_Grande_Do_Sul.shp')
rio_gdf = gpd.read_file(rio_path)

# Create a base map
m4 = folium.Map(
    location=[-30.0, -53.0],
    zoom_start=6,
    tiles='CartoDB positron'
)

# Add the first layer - Rio Grande do Sul municipalities
folium.GeoJson(
    rio_gdf,
    name='Rio Grande do Sul',
    style_function=lambda x: {
        'fillColor': '#ffff00',
        'color': '#000000',
        'weight': 1,
        'fillOpacity': 0.1
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['CODMUNRS', 'MUNICIPIO'],
        aliases=['Code:', 'Municipality:'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )
).add_to(m4)

# Create a choropleth layer based on population
folium.Choropleth(
    geo_data=rio_gdf,
    name='Population',
    data=rio_gdf,
    columns=['CODMUNRS', 'POP2000'],
    key_on='feature.properties.CODMUNRS',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population (2000)',
    highlight=True
).add_to(m4)

# Add some major cities as markers
cities = [
    {'name': 'Porto Alegre', 'loc': [-30.0346, -51.2177]},
    {'name': 'Caxias do Sul', 'loc': [-29.1685, -51.1796]},
    {'

# %%
#!pip install geodatasets
# pip install geopandas geodatasets matplotlib shapely


# %%
from geodatasets import get_path
import geopandas as gpd
import matplotlib.pyplot as plt
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

# %%
import folium
import geopandas as gpd
from geodatasets import get_path
from shapely.geometry import Point
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import time

# Step A: Create the folium map and save as HTML (same as before)

nybb_fp = get_path('nybb')
nybb = gpd.read_file(nybb_fp).to_crs(epsg=4326)
nyc_boundary = nybb.dissolve()

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

pois = gpd.GeoDataFrame(
    poi_data,
    geometry=gpd.points_from_xy(poi_data['longitude'], poi_data['latitude']),
    crs="EPSG:4326"
)

nybb_proj = nybb.to_crs(epsg=3857)
pois_proj = pois.to_crs(epsg=3857)
pois_proj['buffer'] = pois_proj.geometry.buffer(1000)
buffers_wgs84 = pois_proj.set_geometry('buffer').to_crs(epsg=4326)

center_lat = 40.7128
center_lon = -74.0060

m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles='CartoDB positron')

folium.GeoJson(
    nybb.geometry.__geo_interface__,
    name='Boroughs',
    style_function=lambda x: {
        'fillColor': 'lightgreen',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.4,
    }
).add_to(m)

folium.GeoJson(
    nyc_boundary.geometry.__geo_interface__,
    name='NYC Boundary',
    style_function=lambda x: {
        'fillColor': 'none',
        'color': 'red',
        'weight': 3,
    }
).add_to(m)

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

for _, row in pois.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=row['name'],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

folium.LayerControl().add_to(m)

m



# %%
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


