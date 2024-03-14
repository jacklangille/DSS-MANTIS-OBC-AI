from math import radians, cos, sin, sqrt, atan2
import folium

# Constants
SWATH_WIDTH = 290 # km, sentinel-2

# Coordinates (lon, lat) 
# TODO: Read these in from file for each AOI
# TODO: Send results to a file
center_pt = (-66.72838702399886, 41.1416760978243)
nw = (-68.58604112771494, 43.425172798679824) 
ne = (-64.74841888575303, 43.425172798679824)
sw = (-68.58604112771494, 38.63052616537985)
se = (-64.74841888575303,38.63052616537985)


def haversine(coord1, coord2):
    # !Expects (lon, lat)! # 
    R = 6378.14 # Radius of earth
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    # Convert latitude and longitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def folium_map():
    # !Expects (lat, lon)! # 
    m = folium.Map(location=center_pt[::-1], zoom_start=13)
    folium.Polygon(
    locations=[
        nw[::-1],
        ne[::-1],
        se[::-1],
        sw[::-1],
    ],
    color='blue',      
    fill=True,         
    fill_color='cyan'  
    ).add_to(m)
    m.save("aoi.html") 

def main():
    north_south_len = haversine(nw, sw)
    east_west_len = haversine(nw, ne)
    print(f"North-south length = {north_south_len:.2f} km, east-west length = {east_west_len:.2f} km ")
    num_images_horiz = east_west_len / SWATH_WIDTH
    print(f"Specified region requires {num_images_horiz:.2f} images/passes for full coverage") 
    folium_map()

if __name__ == "__main__":
    main()