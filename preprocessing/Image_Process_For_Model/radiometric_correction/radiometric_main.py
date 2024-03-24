import numpy as np
from load_and_convert import loadDataSet, convertImages
from detector_response import radiometricCorrection
import cv2
import matplotlib.pyplot as plt

def normalize_4channel_image(image):
    r, g, b, nir = cv2.split(image)
    r_normalized = (r - np.min(r)) / (np.max(r) - np.min(r))
    g_normalized = (g - np.min(g)) / (np.max(g) - np.min(g))
    b_normalized = (b - np.min(b)) / (np.max(b) - np.min(b))
    nir_normalized = (nir - np.min(nir)) / (np.max(nir) - np.min(nir))
    normalized_image = cv2.merge([r_normalized, g_normalized, b_normalized, nir_normalized])
    return normalized_image

def prepare_images_for_model(images):
    normalized_images = np.zeros_like(images)
    for i in range(len(images)):
        normalized_images[i] = normalize_4channel_image(images[i])
    return normalized_images

def run_radiometric_correction(folder_path):
    # Load TIFF paths
    tiff_paths = loadDataSet(folder_path)

    # Convert TIFFs to NumPy arrays
    image_tensors = convertImages(tiff_paths)

    # Radiometric correction
    radiometrically_corrected_images = radiometricCorrection(image_tensors)

    return radiometrically_corrected_images

if __name__ == "__main__":
    folder_path = 'C:/DSS/DSS FOLDER 1 11TH NOV/DSS-MANTIS-OBC-AI/Images/tree-phen/trees_feb2020-Dec2021_10m'

    corrected_images = run_radiometric_correction(folder_path)

    # Normalize and prepare images for the model
    normalized_images = prepare_images_for_model(corrected_images)

   
    model_predictions = model.predict(normalized_images)


