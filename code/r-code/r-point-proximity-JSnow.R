
##########################################
# Install and load necessary packages
if (!require("leaflet")) install.packages("leaflet")
library(leaflet)
library(sf)
library(tidyverse)
library(htmltools)

# Load John Snow's cholera outbreak data
# The HistData package contains this dataset
if (!require("HistData")) install.packages("HistData")
library(HistData)

# Load the datasets
data(Snow.deaths)
data(Snow.pumps)
data(Snow.streets)

# Convert the data to sf objects
# First, set the CRS to match Snow's original map
# These coordinates are approximate for Soho, London
deaths_sf <- st_as_sf(Snow.deaths, coords = c("x", "y"))
pumps_sf <- st_as_sf(Snow.pumps, coords = c("x", "y"))

# We need to convert Snow's original coordinates to geographic coordinates
# The original map is in a custom coordinate system
# We'll create a transformation function based on known points

# Define reference points (approximate Soho locations)
# Original coordinates from Snow's map
orig_coords <- data.frame(
  x = c(min(Snow.deaths$x), max(Snow.deaths$x)),
  y = c(min(Snow.deaths$y), max(Snow.deaths$y))
)

# Corresponding real-world coordinates (WGS84) for Soho, London
# These are approximate and would need refinement for a perfect match
real_coords <- data.frame(
  lon = c(-0.1367, -0.1329),  # West to East
  lat = c(51.5115, 51.5135)   # South to North
)

# Create a linear transformation function
transform_coords <- function(x, y) {
  # Linear interpolation
  x_ratio <- (x - orig_coords$x[1]) / (orig_coords$x[2] - orig_coords$x[1])
  y_ratio <- (y - orig_coords$y[1]) / (orig_coords$y[2] - orig_coords$y[1])
  
  lon <- real_coords$lon[1] + x_ratio * (real_coords$lon[2] - real_coords$lon[1])
  lat <- real_coords$lat[1] + y_ratio * (real_coords$lat[2] - real_coords$lat[1])
  
  return(data.frame(lon = lon, lat = lat))
}

# Transform death locations
deaths_coords <- transform_coords(Snow.deaths$x, Snow.deaths$y)
deaths_geo <- cbind(Snow.deaths, deaths_coords)
deaths_sf <- st_as_sf(deaths_geo, coords = c("lon", "lat"), crs = 4326)

# Transform pump locations
pumps_coords <- transform_coords(Snow.pumps$x, Snow.pumps$y)
pumps_geo <- cbind(Snow.pumps, pumps_coords)
pumps_sf <- st_as_sf(pumps_geo, coords = c("lon", "lat"), crs = 4326)

# Transform streets for context
streets_sf_list <- lapply(1:nrow(Snow.streets), function(i) {
  street <- Snow.streets[i, ]
  street_coords <- transform_coords(c(street$x1, street$x2), c(street$y1, street$y2))
  line <- st_linestring(matrix(c(street_coords$lon, street_coords$lat), ncol = 2))
  return(st_sfc(line, crs = 4326))
})
streets_sf <- st_sf(geometry = do.call(c, streets_sf_list))

# Create a custom icon for the Broad Street pump
broad_st_icon <- makeIcon(
  iconUrl = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
  iconWidth = 25, iconHeight = 41,
  iconAnchorX = 12, iconAnchorY = 41
)

# Create the interactive map
snow_map <- leaflet() %>%
  # Add a base map
  addProviderTiles(providers$CartoDB.Positron) %>%
  
  # Add historical map overlay (if available)
  # addTiles("https://mapwarper.net/maps/tile/29435/{z}/{x}/{y}.png", 
  #         options = tileOptions(opacity = 0.7)) %>%
  
  # Add the streets
  addPolylines(
    data = streets_sf,
    color = "#333333",
    weight = 2,
    opacity = 0.7
  ) %>%
  
  # Add the cholera deaths
  addCircles(
    data = deaths_sf,
    radius = 2,
    color = "black",
    fillColor = "blue",
    fillOpacity = 0.8,
    weight = 1,
    popup = "Cholera Death"
  ) %>%
  
  # Add the water pumps
  addCircleMarkers(
    data = pumps_sf,
    radius = 6,
    color = "black",
    fillColor = "green",
    fillOpacity = 0.8,
    weight = 2,
    popup = ~paste("<b>Water Pump</b><br>", as.character(label))
  ) %>%
  
  # Highlight the Broad Street pump
  addMarkers(
    data = pumps_sf %>% filter(label == "Broad Street"),
    icon = broad_st_icon,
    popup = "<b>Broad Street Pump</b><br>The source of the outbreak"
  ) %>%
  
  # Add a legend
  addLegend(
    position = "bottomright",
    colors = c("blue", "green", "red"),
    labels = c("Cholera Death", "Water Pump", "Broad Street Pump"),
    opacity = 0.7,
    title = "John Snow's Cholera Map (1854)"
  ) %>%
  
  # Set the view to focus on Soho
  setView(lng = mean(deaths_coords$lon), lat = mean(deaths_coords$lat), zoom = 17)

# Display the map
snow_map

# Optional: Add Voronoi polygons to show pump service areas
if (!require("deldir")) install.packages("deldir")
library(deldir)

# Create Voronoi polygons around pumps
pump_coords <- st_coordinates(pumps_sf)
voronoi <- deldir(pump_coords[,1], pump_coords[,2])
voronoi_polygons <- tile.list(voronoi)

# Convert to sf
voronoi_sf <- lapply(1:length(voronoi_polygons), function(i) {
  poly <- voronoi_polygons[[i]]
  coords <- cbind(poly$x, poly$y)
  # Close the polygon
  coords <- rbind(coords, coords[1,])
  # Create polygon
  st_polygon(list(coords))
})
voronoi_sf <- st_sfc(voronoi_sf, crs = 4326)
voronoi_sf <- st_sf(geometry = voronoi_sf, pump_id = 1:length(voronoi_polygons))

# Add Voronoi polygons to the map
snow_map_with_voronoi <- snow_map %>%
  addPolygons(
    data = voronoi_sf,
    fillColor = "yellow",
    fillOpacity = 0.2,
    color = "orange",
    weight = 1,
    dashArray = "3",
    popup = "Pump Service Area"
  )

# Display the enhanced map
snow_map_with_voronoi
