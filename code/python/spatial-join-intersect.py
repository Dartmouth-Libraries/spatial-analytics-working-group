# task  import dataset of points 

#!pip install geopandas
#!pip install shapely
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








