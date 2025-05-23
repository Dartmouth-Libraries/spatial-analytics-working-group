# -*- coding: utf-8 -*-
""" 
spatial-python-colab
"""
import folium

#!pip install folium

lat = 43.7031000
lon = -72.28854

map = folium.Map(location=[lat, lon], zoom_start=15)
map

map = folium.Map()
marker = folium.Marker(location=[lat, lon], popup='An interesting point')
marker.add_to(map)
map

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely

point_csv = pd.read_csv('https://rcweb.dartmouth.edu/homes/f002d69/workshops/data/bear-sightings.csv')
point_csv

point_csv.head(3)

point_csv.tail(3)

from google.colab import files
uploaded = files.upload()

file_name = list(uploaded.keys())[0]
polygons = gpd.read_file(file_name)
polygons.head(3)

points = gpd.GeoDataFrame(point_csv, geometry=gpd.points_from_xy(point_csv.longitude, point_csv.latitude))
points.head(3)

points.crs='EPSG:4326'

points = points.to_crs(polygons.crs)

points_in_polygons = gpd.sjoin(points, polygons, predicate='within')
points_in_polygons.head(50)

polygons.plot(facecolor='none')
points.plot(ax=plt.gca())
points_in_polygons.plot(color='red', ax=plt.gca())
plt.axis("off")
plt.show()
