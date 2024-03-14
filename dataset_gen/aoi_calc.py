"""---------------------------------------------- PREAMBLE ----------------------------------------------"""
from math import radians, cos, sin, sqrt, atan2, pi
import folium

""" Laundry List """
# TODO: Read in from file for each AOI
# TODO: Modify code to create the closest AOI based on acceptable pixel size and grid dimensions for API call
# TODO: Pipeline grid coordinates to perform API call. 
# TODO: Make copy of code that reflects MANTIS payload specifications (swath width, resolution)
# TODO: Add read me

"""---------------------------------------------- CONSTS ----------------------------------------------"""
# Hardcoded coordinates (lon, lat) 
center_pt = (-66.72838702399886, 41.1416760978243)
nw = (-68.58604112771494, 43.425172798679824) 
ne = (-64.74841888575303, 43.425172798679824)
sw = (-68.58604112771494, 38.63052616537985)
se = (-64.74841888575303,38.63052616537985)

SWATH_WIDTH = 290 # km, sentinel-2
MAX_WIDTH = 2500 # pixels
RESOLUTION = 10 # meters
EARTH_R = 6378.14 # km

"""---------------------------------------------- FUNCS ----------------------------------------------"""
def haversine(coord1, coord2):
    """ !Expects (lon, lat)!. Use the Haversine formula to compute point-to-point distance of two coordinate points. """
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = EARTH_R * c
    return distance

def get_pixel_count(distance_km, resolution_m):
    """ Calculate the number of pixels for a given side of the AOI."""
    distance_m = distance_km * 1000  
    pixels = distance_m / resolution_m
    return int(pixels)

def calculate_api_requests(pixels_width, pixels_height, max_width=MAX_WIDTH, max_height=MAX_WIDTH) -> tuple:
    """ Calculates the number of API requests needed to cover an area. """
    num_requests_horiz = -(-pixels_width // max_width)  # Ceiling division to ensure covering the whole area
    num_requests_vert = -(-pixels_height // max_height)  # Ceiling division
    
    return num_requests_horiz, num_requests_vert

def km_to_degrees(km, at_latitude):
    """ Converts a distance in kilometers to degrees, considering the latitude. """
    # Earth's radius in kilometers
    
    # 1 degree of latitude in kilometers
    lat_degree_km = 2 * pi * EARTH_R / 360
    
    # 1 degree of longitude in kilometers varies based on latitude
    lon_degree_km = cos(radians(at_latitude)) * lat_degree_km
    
    # Convert km to degrees
    delta_lat = km / lat_degree_km
    delta_lon = km / lon_degree_km
    
    return delta_lat, delta_lon

def generate_tile_coords(sw, ne, tile_size_km):
    """ Generates the coordinates for tiles within the specified area. """
    tile_coords = []
    
    # Convert the tile size from kilometers to degrees
    delta_lat, delta_lon = km_to_degrees(tile_size_km, sw[1])
    
    # Initialize starting points
    current_lat = sw[1]
    current_lon = sw[0]
    
    # Loop through rows and columns to generate tiles
    while current_lat < ne[1]:
        while current_lon < ne[0]:
            # Calculate the NE corner of the current tile
            tile_ne_lat = current_lat + delta_lat
            tile_ne_lon = current_lon + delta_lon
            
            # Store the SW and NE corners of the current tile
            tile_coords.append(((current_lon, current_lat), (tile_ne_lon, tile_ne_lat)))
            
            # Move to the next tile to the east
            current_lon += delta_lon
        
        # Move to the first tile of the next row to the north
        current_lat += delta_lat
        current_lon = sw[0]
    
    return tile_coords

def folium_map(tiles):
    """ !Expects (lat, lon)!. Produces map of AOI as a grid of API calls. """
    m = folium.Map(location=center_pt[::-1], zoom_start=13)
    folium.Polygon(
    locations=[
        nw[::-1],
        ne[::-1],
        se[::-1],
        sw[::-1],
    ],
    color="blue",      
    fill=True,         
    fill_color="cyan",
    fill_opacity = 0,  
    ).add_to(m)

    # Iterate through the tiles and draw each one
    for sw_tile, ne_tile in tiles:
        folium.Rectangle(
            bounds=[sw_tile[::-1], ne_tile[::-1]],  # Convert to (lat, lon) and specify SW and NE bounds
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.1  # Make the fill semi-transparent
        ).add_to(m)

    m.save(f"{RESOLUTION}m_aoi_grid.html") 

"""---------------------------------------------- MAIN ----------------------------------------------"""
def main():
    # Compute dimensions of region in kilometers
    north_south_len = haversine(nw, sw)
    east_west_len = haversine(nw, ne)
    print(f"North-south length = {north_south_len:.2f} km, east-west length = {east_west_len:.2f} km ")
    
    # Compute number of images required based on swath width
    num_images_horiz = east_west_len / SWATH_WIDTH
    print(f"Specified region requires {num_images_horiz:.2f} images/passes for full coverage") 

    # Calculate number of pixels of image (WxH) based on resolution
    pixels_north_south = get_pixel_count(north_south_len, RESOLUTION)
    pixels_east_west = get_pixel_count(east_west_len, RESOLUTION)
    print(f"Image dimensions in pixels: {pixels_east_west} (width) x {pixels_north_south} (height)")
    if pixels_north_south > MAX_WIDTH or pixels_east_west > MAX_WIDTH:
        print("!Requested dimensions exceed the maximum allowed pixel size!")
    
    # Calculate how many API requests are needed
    requests_horiz, requests_vert = calculate_api_requests(pixels_east_west, pixels_north_south)
    total_requests = requests_horiz * requests_vert
    print(f"Number of API requests needed: {total_requests} ({requests_horiz} horizontal x {requests_vert} vertical)")

    # Calculate size of each tile    
    tile_size_km = 2500 * RESOLUTION / 1000
    
    # Generate the tile coordinates
    tiles = generate_tile_coords(sw, ne, tile_size_km)
    
    # Print the number of tiles and their coordinates
    print(f"Generated {len(tiles)} tiles.")
    for tile in tiles: print(tile)
    
    # Produce map with folium 
    folium_map(tiles)

if __name__ == "__main__":
    main()