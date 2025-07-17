# Set working directory
setwd('~/Downloads')

# Load required libraries
library(sp)         # For spatial objects and functionalities
library(sf)         # For handling simple features
library(terra)      # For working with raster and vector data
library(maps)       # For plotting maps

library(tidyverse)

# Unzip the dataset containing parks
unzip(zipfile = "polygons-parks.zip", exdir = "data")

# Load sightings data using read.csv
points <- read.csv('points.csv')

# Convert the data frame to a simple features object
points_sf <- st_as_sf(points, coords = c('longitude', 'latitude'), crs = 4326)  # Let's set CRS to WGS84 directly

# Plot  locations
plot(st_geometry(points_sf), main = "point locations")

# Add a coarse map layer for context using maps package
map("world", region="usa", add=TRUE)

# Load the parks shapefile into R using the terra package
parks <- vect('polygons/polygons.shp')  # Load parks shapefile

# Convert parks from SpatVector to sf object
parks_sf <- st_as_sf(parks)  # Convert SpatVector to sf object

# Check and repair invalid geometries in parks_sf
parks_sf <- st_make_valid(parks_sf)

# Print the projection of the parks to check
parks_crs <- crs(parks_sf)  # Store the CRS of parks in a variable
print(parks_crs)

# Set the projection of points to the same as parks dataset
st_crs(points_sf) <- parks_crs  # Setting the same CRS  as parks

# Use st_within to check which are inside the parks
insidePark <- st_within(points_sf, parks_sf)

# Check if any points fall inside  parks (True if inside any park)
insidePark <- sapply(insidePark, function(x) length(x) > 0)

# Calculate the fraction of points inside parks
fractionInsidePark <- mean(insidePark)

# Print the percentage of points inside parks
cat("Percent inside parks: ", 100 * fractionInsidePark, ' percent ')

# Plot the point sightings with parks overlaid
plot(st_geometry(points_sf), main = "Point locations inside Parks")
map("world", region = "usa", add = TRUE)  # Add the USA map
plot(st_geometry(parks_sf), border = "green", col = NA, add = TRUE)  # Add parks to the plot

# Set the colors for the points: red for  inside parks, green for  outside parks
points(points_sf[insidePark, ], pch = 16, col = "red")
points(points_sf[!insidePark, ], pch = 1, col = "green")

# legend
legend("topright", cex=0.85,
       c("point in park", "point not in park", "Park boundary"),
       pch=c(16, 1, NA), lty=c(NA, NA, 1),
       col=c("red", "grey", "green"), bty="n")
title(expression(paste(italic("points"),
                       " sightings with respect to national parks")))

# Create a pie chart to visualize  inside and outside the parks
slices <- c(fractionInsidePark, 1 - fractionInsidePark)
lbls <- c("points in the parks", "points outside the parks")
pct <- round(slices/sum(slices)*100, 2)

# Add percentages to the labels
lbls <- paste(lbls, pct)
lbls <- paste(lbls, "%", sep="")

# Generate the pie chart
pie(slices, labels = lbls, col = rainbow(length(lbls)), main = " Sightings")

# Save the pie chart to results folder
dev.copy(jpeg, 'myplot2.jpg')
dev.off()  # Close the plotting device

# Store the name of the park as an attribute of the points dataset
#points_sf <- st_join(points_sf, st_zm(parks), join = st_intersects)

# ... [previous code remains unchanged]

# Store the name of the park as an attribute of the points dataset
points_sf <- st_join(points_sf, parks_sf, join = st_intersects)  # Use parks_sf directly

# output - csv file 

# Write a CSV file with point sightings and park names (if found)
write.csv(as.data.frame(points_sf), "points-by-park.csv", row.names = FALSE)

# Save this map to the results folder
dev.copy(jpeg, 'mymap.jpg')
dev.off()  # Close the plotting device

# Install and load necessary packages
if (!require("leaflet")) install.packages("leaflet")
library(htmltools)

