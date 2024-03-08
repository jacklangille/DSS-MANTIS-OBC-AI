import numpy as np
import matplotlib.pyplot as plt
from load_and_convert import image_tensors
from sunAngle_topographic import sunAngleCorrection
import cv2

def radiometricCorrection(images):
    corrected_images = []

    for image in images:

        destriped_image = destripeImage(image)
        interpolated_image = interpolateMissingScanLine(destriped_image)
        after_vignetting_removal=correctVignetting(interpolated_image)
        denoised_image = removeRandomNoise(after_vignetting_removal)
        sun_angle_corrected_image = sunAngleCorrection(denoised_image, 30)  # Don't yet know how to get solar elevation angle
        
        # Normalization to each band
        normalized_image = (sun_angle_corrected_image - np.min(sun_angle_corrected_image)) / (np.max(sun_angle_corrected_image) - np.min(sun_angle_corrected_image))
        corrected_images.append(normalized_image)

    return corrected_images


def interpolateMissingScanLine(image):
    # Interpolate missing scan line (simple linear interpolation)
    for y in range(1, image.shape[0] - 1):
        missing_scan_line_indices = np.isnan(image[y, :])
        if np.any(missing_scan_line_indices):
            for x in range(image.shape[1]):
                if missing_scan_line_indices[x]:
                    # Linear interpolation for missing scan line
                    image[y, x] = (image[y - 1, x] + image[y + 1, x]) / 2

    return image

def destripeImage(image):
    #Destripe the image (using the provided formula)
    for y in range(1, image.shape[0] - 1):
        missing_scan_line_indices = np.isnan(image[y, :])
        if np.any(missing_scan_line_indices):
            for x in range(image.shape[1]):
                if missing_scan_line_indices[x]:
              
                    image[y, x] = destripingFormula(image, y, x)

    return image

#De-striping formula
def destripingFormula(image, y, x):
    od = 255
    oi = 255
    md = np.mean(image)
    mi = np.mean(image)

    return (od / oi) * image[y - 1, x] + md - (od / oi) * mi

def correctVignetting(image):
    clahe = cv2.createCLAHE()
    corrected_image = clahe.apply(image)
    return corrected_image

# Replacing each pixel value with the median value of its neighboring pixels within a specified kernel size
def removeRandomNoise(image):
    denoised_image = cv2.medianBlur(image.astype(np.uint8), 5)  # The kernel size here would need to be adjusted
    return denoised_image

radiometrically_corrected_images = radiometricCorrection(image_tensors)

# Section 4: Displaying Radiometrically Corrected Images (Optional)
# plt.imshow(radiometrically_corrected_images[0])
# plt.title('First Radiometrically Corrected Image')
# plt.show()

plt.close('all')