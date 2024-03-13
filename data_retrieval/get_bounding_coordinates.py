
import pyproj

"""
    Azimuth values: 
        North: 0   deg 
        East:  90  deg
        South: 180 deg
        West;  270 deg
"""

def get_bounding_coordinates(latitude, longitude, image_side_length):
    """
    This function calculates the coordiante points of teh NorthWest and SouthEast corners of an image,  
    based on the center point, and the desired side length of the square image (in metres).

    Args:
        latitude: the latitude of the central coordinate in WGS84 format
        long:     the longitude of the central coordinate in WGS84 format
        image_side_length: the desired side length of the square image which will be returned, in metres

    Returns:
        _type_: (long_min, lat_min, long_max, lat_max)
    """

    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")
    
    distanceToEdge = (image_side_length)/2

    WGS84_Geod = pyproj.Geod(ellps='WGS84')

    #Calculate the Northmost, Eastmost, Southmost and Wemost points, respectively
    _, lat_max, _ = WGS84_Geod.fwd(longitude, latitude, 0, distanceToEdge)
    long_max, _, _ = WGS84_Geod.fwd(longitude, latitude, 90, distanceToEdge)
    _, lat_min, _ = WGS84_Geod.fwd(longitude, latitude, 180, distanceToEdge)
    long_min, _, _ = WGS84_Geod.fwd(longitude, latitude, 270, distanceToEdge)

    bounding_coordinates = (long_min, lat_min, long_max, lat_max)

    return bounding_coordinates