# %% [markdown]
# ## Welcome to Geographic Data Science!
# - This morning's goal: introduce concepts, import libraries, what are Geographic Information Systems(GIS), what is geospatial analysis
# - This afternoon's goal: work with spatial datasets, mini-spatial project
# 
# 

# %% [markdown]
# - pandas data frames contain rows of observations or features, and columns of attributes that describe those features
# - geopandas data frames contain rows of observations or features, with columns of attributes, and one specialized column that stores the geographic attributes of the feature
# - this geometry column can contain:
#     - coordinate points
#     - coordinates that form a line or 'polyline' feature
#     - coordinates that form a shape (polygon)

# %% [markdown]
# # OVERVIEW
# ## Questions
# - How can I view spatial/geographic/geospatial data in Python?
# - What are Geographic Information Systems?  
# 
# ## Objectives
# - Basics of spatial and geospatial data science
# - Create a spatial/geospatial Python Jupyter notebook
# - Create a computational script to display geographic data

# %% [markdown]
# #Reminder
# ###   To run this code in the 'JupyterLab' environment:
# - navigate to https://jupyterlab.dartmouth.edu
# - log in with the credentials provided

# %%
import folium
import json
# define location in GeoJSON format(using geojson.io) and extract coordinates data

# copy in spatial data, from a single point created with
# https://geojson.io/

geojson_data =  ________

coordinates = geojson_data['features'][0]['geometry']['coordinates']
latitude = coordinates[1]
longitude = coordinates[0]
# visualize: create a map centered around the point, Add the point to the map and display
m = folium.Map(location=[latitude, longitude], zoom_start=15)
folium.Marker([latitude, longitude]).add_to(m)
m
# m.save("map.html")

# %%
import folium
import json
# define location in GeoJSON format(using geojson.io) and extract coordinates data

# copy in spatial data, from a single point created with
# https://geojson.io/
geojson_data = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": [
          -72.29047820804581,
          43.70310599038794
        ],
        "type": "Point"
      }
    }
  ]
}

coordinates = geojson_data['features'][0]['geometry']['coordinates']
latitude = coordinates[1]
longitude = coordinates[0]
# visualize: create a map centered around the point, Add the point to the map and display
m = folium.Map(location=[latitude, longitude], zoom_start=15)
folium.Marker([latitude, longitude]).add_to(m)
m
# m.save("map.html")

# %%
# install and import geospatial library 'geopandas'
# pip install geopandas
import geopandas as gdp
# geopandas basics, in jupyter notebook (no downloads/imports)

# %% [markdown]
# 

# %% [markdown]
# ## Exercise: extract and load a geospatial dataset using the 'GeoPandas' library
# 

# %%
pip install pandas

# %%
import pandas as pd

# %%
# first, let's read in a CSV file, using the 'pandas' library
points_csv = pd.read_csv("https://rcweb.dartmouth.edu/homes/f002d69/workshops/data/bear-sightings.csv")
points_csv.head(3)

# %%
# Step 1: Import the necessary libraries
import geopandas as gpd
import matplotlib.pyplot as plt

# Step 2: Load the built-in dataset
world = gpd.datasets.get_path('naturalearth_lowres')
# Steve - add to notes / slides, https://www.naturalearthdata.com/
gdf = gpd.read_file(world)

# Step 3: Explore the dataset
# Display the first few rows
print(gdf.head())

# Print the column names and their data types
print(gdf.dtypes)

# Step 4: Plot  world map
gdf.plot()
plt.title('World Map')
plt.show()
# !pip install geopandas==0.8.2
# pip show geopandas
# Name: geopandas
# Version: 0.13.2




# %% [markdown]
# **Exercise: **
# See if you can 'filter' the world dataset to show just one continent
# Hint: you can list the continent names first, and then build a filter by setting a variable like this:   a_continent = gdf[gdf['___________'] == '*______________*']
# 

# %%


# %% [markdown]
# **Exercise**
# 

# %% [markdown]
# See if you can 'filter' the world dataset to show just one continent

# %% [markdown]
# *hint: you can list the continent names first, then build a filter*

# %% [markdown]
# a_continent = gdf[gdf['continent']==' ____ ' ]

# %%


# %%
# Step 5: Filter and plot specific data (e.g., Africa)
_____ = gdf[gdf['continent'] == '_____']
_____.plot()
plt.title('_________')
plt.show()

# %% [markdown]
# Color the world map based on the values in the 'pop_est' field (color based on population)

# %%
# World map based on population
gdf.plot(column='pop_est', cmap='OrRd', legend=True)
plt.title('World Map shaded by Population in billions')
plt.show()


# %%
# Save the Africa GeoDataFrame to a new shapefile (a GIS data type for vector data )
#africa.to_file("africa.shp")


# notes: geocode one address, show open street map, write a loop to geocode five city names
# steve add https://geojson.io/

# add python import of geojson / json

# google maps as a geocoder

# geocode using pythong  & open street map

# https://www.openstreetmap.org/#map=5/37.996/-95.801

# natural earth data https://www.naturalearthdata.com/downloads/




# %%
# pip install folium
#pip install geopandas folium
import folium

# %%


# Read the shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Display the first few rows
print(world.head())


# %% [markdown]
# **Exercise:**

# %% [markdown]
# use a filter again, this time for South America

# %%
# Filter the dataset for South American countries
south_america = world[world['continent'] == 'South America']

# Display the first few rows of the South America dataset
print(south_america.head())


# %% [markdown]
# Use the 'folium' library to center a map near -15.7801 latitude, -47.9292 longitude.  Use Google Maps first to confirm where this point is.

# %%
import folium

# Create a base map centered around South America
m = folium.Map(location=[-15.7801, -47.9292], zoom_start=3, tiles='Stamen Toner')

# Add South America countries to the map
folium.GeoJson(south_america).add_to(m)

# Save the map to an HTML file
m.save('south_america_map.html')
m


# %%
# Calculate the area of each country (in square kilometers)
south_america['area_km2'] = south_america['geometry'].area / 10**6

# Create a base map centered around South America
m = folium.Map(location=[-15.7801, -47.9292], zoom_start=3, tiles='Stamen Toner')

# Add South America countries to the map with tooltips
for _, row in south_america.iterrows():
    folium.GeoJson(
        row['geometry'],
        tooltip=f"Country: {row['name']}<br>Area: {row['area_km2']:.2f} km²"
    ).add_to(m)

# Save the map to an HTML file
m.save('south_america_area_map.html')
m



