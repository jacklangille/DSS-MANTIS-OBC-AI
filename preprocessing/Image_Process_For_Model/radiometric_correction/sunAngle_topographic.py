import numpy as np
import math

def sunAngleCorrection(image, solar_elevation_angle):
    # Sun angle correction using the formula DNcorr = DN / (sin(theta))
    sin_theta = math.sin(math.radians(solar_elevation_angle))
    corrected_image = image / sin_theta

    topographic_Corrected= minnaertCorrection(corrected_image,10, 1.5, 30)
    return topographic_Corrected

def minnaertCorrection(image, slope, minnaert_constant, solar_elevation_angle):
    # Minnaert correction for terrain illumination effects
    cos_theta = np.cos(np.radians(solar_elevation_angle))
    cos_slope = np.cos(np.radians(slope))

    # Apply Minnaert correction
    corrected_image = image * cos_theta * cos_slope ** (minnaert_constant - 1)

    return corrected_image