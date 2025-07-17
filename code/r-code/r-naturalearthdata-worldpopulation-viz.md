

# R spatial data science
 rev. 2025-07-16
 explanatory text, slides and examples 
 using publicly available datasets 
 from well-known R packages, 
 such as rnaturalearth and spData, 
 run the code directly without needing to download external shapefiles

 Part 1 / Slide 1 
 Overview
 Using R for Spatial Data Science and Spatial Analytics
 
 Introduction to Spatial Data Science in R
 Key R packages for spatial analysis
 Data import using built-in spatial datasets
 Spatial data visualization techniques
 Spatial data manipulation and transformation
 Spatial point pattern analysis
 Raster data handling and analysis
 Spatial interpolation and modeling
 Advanced spatial statistics
 Case study examples and practical applications

library(leaflet)
leaflet() %>% addTiles()

library(rnaturalearth)
library(sf)

world <- ne_countries(scale = "medium", returnclass = "sf")

head(world)
 check the coordinate reference system
st_crs(world)
 note: EPSG = 4326.  see https://epsg.io/4326 and https://en.wikipedia.org/wiki/Spatial_reference_system for more info
 note also, EPSG 4326 is an 'angular' coordinate system designed for 3D positioning
 other systems, such as EPSG 3437, New Hampshire State Plane, are designed for 2D or 'planar' mapping and analysis
   https://epsg.io/3437 

library(ggplot2)

ggplot(world) +
  geom_sf(aes(fill = pop_est)) +
  scale_fill_viridis_c() +
  theme_minimal() +
  labs(title = "World Population Estimates")

library(tmap)

tm_shape(world) +
  tm_polygons("pop_est", palette = "Blues", title = "Population") +
  tm_layout(title = "World Population")

# plot on leaflet 
leaflet() %>% addTiles() 

library(spatstat)
library(leaflet)

leaflet(world) %>%
  addTiles() %>%
  addPolygons(fillColor = ~colorNumeric("Blues", pop_est)(pop_est),
              fillOpacity = 0.5,
              color = "black",
              weight = 1)






