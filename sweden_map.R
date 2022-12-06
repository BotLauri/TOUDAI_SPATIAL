# Set up. 
setwd("~/GitHub/TOUDAI_SPATIAL")
universities <- read.csv(file = "Data/institution_data.csv", header=TRUE, stringsAsFactors=FALSE, fileEncoding="latin1") # nolint

# Set up and simple Sweden map. 
# https://github.com/junkka/histmaps
devtools::install_github('junkka/histmaps')
library(histmaps)
library(sf)
## Linking to GEOS 3.10.1, GDAL 3.4.0, PROJ 8.2.0; sf_use_s2() is TRUE
library(tidyverse)
map <- get_boundaries(1990, "county")
#plot(st_geometry(map))

# Get the counties with at least one higher instiution to a separate data set. 
university_county <- unique(universities[3])
nr_uni_county <- universities %>%
  group_by(county) %>%
  summarise(n = n()) %>%
  ungroup()

# Get the data for each county. 
st_map <- map %>% left_join(geom_meta, by = c("geom_id"))
st_map <- st_map %>% right_join(university_county, by = c("county"))
st_map <- st_map %>% right_join(nr_uni_county, by = c("county"))

# Plot with different colors based on how many instituions within the county. 
ggplot() +
  geom_sf(data = map, color = "black", fill = "lightgray") +
  geom_sf(data = st_map %>% filter(n == 1), color = "black", fill = "blue") +
  geom_sf(data = st_map %>% filter(n == 2), color = "black", fill = "red") +
  geom_sf(data = st_map %>% filter(n == 4), color = "black", fill = "green") +
  geom_sf(data = st_map %>% filter(n == 13), color = "black", fill = "yellow") +
  theme_minimal()
