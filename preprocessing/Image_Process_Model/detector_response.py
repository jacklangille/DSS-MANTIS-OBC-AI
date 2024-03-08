import numpy as np
import matplotlib.pyplot as plt
from load_and_convert import image_tensors

def radiometricCorrection(images):
    corrected_images = []

    for image in images:
        destriped_image = destripeImage(image)

        # Normalization to each band
        normalized_image = (destriped_image - np.min(destriped_image)) / (np.max(destriped_image) - np.min(destriped_image))

        corrected_images.append(normalized_image)

    return corrected_images

def destripeImage(image):
    # Interpolate missing scan line and destripe 
    for y in range(1, image.shape[0] - 1):
        missing_scan_line_indices = np.isnan(image[y, :])
        if np.any(missing_scan_line_indices):
            for x in range(image.shape[1]):
                if missing_scan_line_indices[x]:
                  
                    image[y, x] = destripingFormula(image, y, x)

    return image

# De-striping formula
def destripingFormula(image, y, x):
    od = 255
    oi = 255
    md = np.mean(image)
    mi = np.mean(image)

    return (od / oi) * image[y - 1, x] + md - (od / oi) * mi

# Example Usage:
radiometrically_corrected_images = radiometricCorrection(image_tensors)

# Section 4: Displaying Radiometrically Corrected Images (Optional)
# plt.imshow(radiometrically_corrected_images[0])
# plt.title('First Radiometrically Corrected Image')
# plt.show()
