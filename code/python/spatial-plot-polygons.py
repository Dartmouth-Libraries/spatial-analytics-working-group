# task - using the 'geodatasets' library, plot spatial polgyons on a web map 

import geopandas as gpd
import geodatasets
import matplotlib.pyplot as plt
from geodatasets import get_path
import folium

# Load NY boroughs dataset (polygons) path and then read it with geopandas
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
        'color': 'gray',
        'weight': 2,
        'fillOpacity': 0.5,
    },
).add_to(m)

# Add layer control to toggle layers on/off (handy if you add more layers)
folium.LayerControl().add_to(m)

# Save to an HTML file and display (if running in Jupyter, just display m)
m.save('ny_boroughs_map.html')
m  # If using Jupyter Notebook, this will display the map inline
