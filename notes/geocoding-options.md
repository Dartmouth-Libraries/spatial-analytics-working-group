**** geocoding options 

****  

ESRI Geocoding
Google Geocoding  

Open Street Map 'Nominitum' geocoding service (API, QGIS)


Geocoding(standard) & HIPAA-compliant geocoding
[Texas A&M geocode](https://www.geocod.io/enterprise/)

Offline, container-based geocoding (using a container tool like Docker) 
[Degauss](https://degauss.org/geocoder/)

ESRI Geocoding
Google Geocoding  
compliant geocoding, there are services that meet HIPAA and other standards, like Spatialitics (powered by ESRI),  , 


```
# code snippet / example of code-based geocoder through an API (Python, geopy and Nominatim)
# https://geopy.readthedocs.io/en/stable/ 
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("175 5th Avenue NYC")
print(location.address)
  #Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
print((location.latitude, location.longitude))
  #(40.7410861, -73.9896297241625)
print(location.raw)
  #{'place_id': '9167009604', 'type': 'attraction', ...}


```
**** 
