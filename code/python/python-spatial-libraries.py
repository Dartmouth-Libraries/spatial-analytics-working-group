
import numpy as np
# dataframe
import pandas as pd
# geodataframe
import geopandas as gpd

# web maps
import folium 

# spatial analysis library https://pysal.org/ 
import pysal as ps
import shapely
from shapely.geometry import Point

from matplotlib.mlab import griddata
from mpl_toolkits.basemap import Basemap, interp
from matplotlib.tri import Triangulation, TriAnalyzer, UniformTriRefiner
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.interpolate import griddata
from shapely.geometry import Polygon, MultiPolygon, box
from descartes import PolygonPatch
%matplotlib inline
import math
from itertools import chain

from descartes import PolygonPatch
import fiona
from itertools import chain, permutations, combinations
import json
