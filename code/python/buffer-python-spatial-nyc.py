# Task #1 
# Import necessary libraries
import folium

# Create a Map centered over Grand Central Station
map = folium.Map(location=[40.7488, -73.9857], tiles="openstreetmap")  
map

# Task #2 
# add a point 

# Create a marker for Grand Central Station and its Popup contents
marker = folium.Marker([40.7488, -73.9857], popup="Grand Central Station", tooltip="Grand Central Marker")  # Add an icon (optional)

# Add the marker to the Map
map.add_child(marker)
map



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
