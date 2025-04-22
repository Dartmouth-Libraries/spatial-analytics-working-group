# this file: point-in-polygon-qgis.py

# running this tool in the QGIS interface: 


# python code
from qgis.core import *
import processing

layer1 = processing.getObject('bear-sightings')
layer2 = processing.getObject('10m_us_parks')
