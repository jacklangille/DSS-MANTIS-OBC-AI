import numpy as np
import matplotlib.pyplot as plt
from load_and_convert import image_tensors

def radiometricCorrection(images):
    corrected_images = []

    for image in images:
       
        # Interpolate missing scan line
        interpolated_image = interpolateMissingScanLine(image)

        # Normalization to each band
        normalized_image = (interpolated_image - np.min(interpolated_image)) / (np.max(interpolated_image) - np.min(interpolated_image))

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

# Example Usage:
radiometrically_corrected_images = radiometricCorrection(image_tensors)

# Section 4: Displaying Radiometrically Corrected Images (Optional)
# Plot the first radiometrically corrected image
plt.imshow(radiometrically_corrected_images[0])
plt.title('First Radiometrically Corrected Image')
plt.show()
