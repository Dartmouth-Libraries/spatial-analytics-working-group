# this file: point-in-polygon-qgis.py

# running this tool in the QGIS interface: 


# python code
from qgis.core import *
import processing

layer1 = processing.getObject('bearsightings')
layer2 = processing.getObject('nationalparks.zip') # 10m US parks layer 

processing.run("native:intersection", {'INPUT':'delimitedtext://file:///Downloads/bearsightings.csv?type=csv&maxFields=10000&detectTypes=yes&xField=longitude&yField=latitude&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no','OVERLAY':'/vsizip//Downloads/nationalparks.zip/10m_us_parks_area.shp|layername=10m_us_parks_area','INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OVERLAY_FIELDS_PREFIX':'','OUTPUT':'TEMPORARY_OUTPUT','GRID_SIZE':None})


