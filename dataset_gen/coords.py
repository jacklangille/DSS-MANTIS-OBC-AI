import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

# Constants
EARTH_CIRCUMFERENCE = 40075000  # in meters
DEGREES_IN_CIRCLE = 360
METERS_PER_PIXEL = 20
PIXELS_PER_CELL_HEIGHT = 2000
PIXELS_PER_CELL_WIDTH = 2000
CELL_HEIGHT_METERS = PIXELS_PER_CELL_HEIGHT * METERS_PER_PIXEL
CELL_WIDTH_METERS = PIXELS_PER_CELL_WIDTH * METERS_PER_PIXEL
# Bounding box details from the image
delta_lon_meters = 533467.200  # the size of the bounding box in meters (longitude)
delta_lat_meters = 180135.781  # the size of the bounding box in meters (latitude)
lat_midpoint = 62.85  # latitude of the midpoint
sw_lon, sw_lat, ne_lon, ne_lat = 4.1, 62.04, 8.9, 63.66  # Coordinates as per the user image
# Functions to convert meters to degrees
def meters_to_latitude(meters):
    return meters / (EARTH_CIRCUMFERENCE / DEGREES_IN_CIRCLE)

def meters_to_longitude(meters, latitude):
    # Convert meters to degrees longitude, adjusting for latitude
    return meters / (EARTH_CIRCUMFERENCE / DEGREES_IN_CIRCLE * math.cos(math.radians(latitude)))

# Calculate the size of a cell in degrees
cell_width_degrees = meters_to_longitude(CELL_WIDTH_METERS, lat_midpoint)
cell_height_degrees = meters_to_latitude(CELL_HEIGHT_METERS)

# Calculate how many cells fit into the bounding box
num_cells_lon = math.ceil(delta_lon_meters / CELL_WIDTH_METERS)
num_cells_lat = math.ceil(delta_lat_meters / CELL_HEIGHT_METERS)

# Calculate the defining coordinates for each cell
cells = []
for i in range(num_cells_lat):
    for j in range(num_cells_lon):
        cell_sw_lon = sw_lon + (j * cell_width_degrees)
        cell_sw_lat = sw_lat + (i * cell_height_degrees)
        cell_ne_lon = cell_sw_lon + cell_width_degrees
        cell_ne_lat = cell_sw_lat + cell_height_degrees
        cells.append({
            'cell_id': (i * num_cells_lon) + j + 1,
            'sw_corner': (cell_sw_lon, cell_sw_lat),
            'ne_corner': (cell_ne_lon, cell_ne_lat)
        })

# Returning the total number of cells and the size of each cell in degrees
print(num_cells_lon, num_cells_lat, cell_width_degrees, cell_height_degrees, len(cells), cells[:1])  # Show the first 2 cells as an example

plt.figure(figsize=(12, 8))
m = Basemap(projection='merc', llcrnrlat=sw_lat, urcrnrlat=ne_lat, llcrnrlon=sw_lon, urcrnrlon=ne_lon, resolution='i')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='lightgray', lake_color='white')
m.drawmapboundary(fill_color='white')

for i in range(num_cells_lat):
    for j in range(num_cells_lon):
        cell_sw_lon = sw_lon + (j * cell_width_degrees)
        cell_sw_lat = sw_lat + (i * cell_height_degrees)
        cell_ne_lon = cell_sw_lon + cell_width_degrees
        cell_ne_lat = cell_sw_lat + cell_height_degrees
        m.plot([cell_sw_lon, cell_ne_lon], [cell_sw_lat, cell_sw_lat], color='blue', latlon=True)  # Bottom line of cell
        m.plot([cell_sw_lon, cell_sw_lon], [cell_sw_lat, cell_ne_lat], color='blue', latlon=True)  # Left line of cell
        m.plot([cell_ne_lon, cell_ne_lon], [cell_sw_lat, cell_ne_lat], color='blue', latlon=True)  # Right line of cell
        m.plot([cell_sw_lon, cell_ne_lon], [cell_ne_lat, cell_ne_lat], color='blue', latlon=True)  # Top line of cell

plt.title('Bounding Box with Grid Cells')
plt.show()
