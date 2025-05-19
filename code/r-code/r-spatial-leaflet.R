# Install and load necessary packages
if (!require("leaflet")) install.packages("leaflet")
if (!require("sf")) install.packages("sf")
if (!require("RColorBrewer")) install.packages("RColorBrewer")
library(leaflet)
library(sf)
library(RColorBrewer)

# Load the meuse dataset
data(meuse, package = "sp")

# Convert to sf object and transform to WGS84
meuse_sf <- st_as_sf(meuse, coords = c("x", "y"), crs = 28992)
meuse_sf <- st_transform(meuse_sf, 4326)  # Transform to WGS84

# Create a color palette for zinc concentration
pal <- colorNumeric(
  palette = "YlOrRd",
  domain = meuse_sf$zinc
)

# Create an interactive leaflet map
leaflet(meuse_sf) %>%
  addTiles() %>%  # Add default OpenStreetMap tiles
  addCircleMarkers(
    radius = ~zinc/200,  # Size based on zinc concentration
    color = ~pal(zinc),
    stroke = FALSE,
    fillOpacity = 0.8,
    popup = ~paste(
      "<strong>Location ID:</strong>", meuse_sf$dist,
      "<br><strong>Zinc (ppm):</strong>", zinc,
      "<br><strong>Copper (ppm):</strong>", copper,
      "<br><strong>Lead (ppm):</strong>", lead
    )
  ) %>%
  addLegend(
    position = "bottomright",
    pal = pal,
    values = ~zinc,
    title = "Zinc Concentration (ppm)",
    opacity = 1
  ) %>%
  setView(lng = mean(st_coordinates(meuse_sf)[,1]), 
          lat = mean(st_coordinates(meuse_sf)[,2]), 
          zoom = 13)
