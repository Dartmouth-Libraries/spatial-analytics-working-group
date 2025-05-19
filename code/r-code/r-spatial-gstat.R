# Install and load necessary packages
if (!require("sf")) install.packages("sf")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("sp")) install.packages("sp")
if (!require("gstat")) install.packages("gstat")
library(sf)
library(ggplot2)
library(sp)
library(gstat)

# Load the meuse dataset
data(meuse, package = "sp")
head(meuse)

# Convert to sf object
meuse_sf <- st_as_sf(meuse, coords = c("x", "y"), crs = 28992)  # Dutch coordinate system

# Transform to WGS84 for mapping
meuse_sf_wgs84 <- st_transform(meuse_sf, 4326)

# Create a spatial visualization of zinc concentration
ggplot(meuse_sf) +
  geom_sf(aes(color = zinc, size = zinc), alpha = 0.7) +
  scale_color_viridis_c() +
  theme_minimal() +
  labs(title = "Zinc Concentration in the Meuse Dataset",
       color = "Zinc (ppm)",
       size = "Zinc (ppm)")

# Let's create a spatial interpolation map
# First convert meuse to SpatialPointsDataFrame (sp object)
coordinates <- meuse[, c("x", "y")]
meuse_sp <- SpatialPointsDataFrame(coords = coordinates, data = meuse,
                                   proj4string = CRS("+init=epsg:28992"))

# Create a grid for prediction
bb <- st_bbox(meuse_sf)
x_range <- seq(bb["xmin"], bb["xmax"], length.out = 50)
y_range <- seq(bb["ymin"], bb["ymax"], length.out = 50)
grid_points <- expand.grid(x = x_range, y = y_range)
grid_sp <- SpatialPixelsDataFrame(points = grid_points, data = data.frame(id = 1:nrow(grid_points)),
                                  proj4string = CRS("+init=epsg:28992"))

# Fit a variogram and create a kriging model
v <- variogram(log(zinc) ~ 1, meuse_sp)
m <- fit.variogram(v, vgm(1, "Sph", 800, 1))
k <- krige(log(zinc) ~ 1, meuse_sp, grid_sp, model = m)

# Convert kriging results to sf
k_sf <- st_as_sf(k)

# Plot the interpolated surface
ggplot() +
  geom_sf(data = k_sf, aes(color = var1.pred), size = 1.5) +
  scale_color_viridis_c(option = "plasma", name = "log(zinc)") +
  geom_sf(data = meuse_sf, size = 2, shape = 21, fill = "white") +
  theme_minimal() +
  labs(title = "Kriging Interpolation of Zinc Concentration")

