'''
THIS FILE CONTAINS FUNCTIONS TO LOAD AND CONVERT RASTER FILES INTO NUMPY ARRAYS TO USE FOR MACHINE LEARNING
CODE WRITTEN FOR CUBESAT MANTIS PROGRAM (DSS)
AUTHOR: CHAZ DAVIES
DATE: 2024-01-20
''' 

import numpy as np
import matplotlib as img #to plot the image
import rasterio # module for raster data manipulation
from rasterio.plot import show #for plotting the images
import os



def loadDataSet(folder_path) -> []:
    '''
    Loads all the .tiff files into an array. From CHATGPT

    Parameters:
        path: a path to the .tiff file (Raster images)

    Returns:
        An array of raster images
    '''
    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter files with a .tiff or .tif extension
    tiff_files = [file for file in files if file.lower().endswith('.tiff') or file.lower().endswith('.tif')]

    # Construct the full paths to the TIFF files
    raster_images = [rasterio.open(os.path.join(folder_path, tiff_file) for tiff_file in tiff_files)]

    return raster_images



def convertImage(rasterImage) -> np.array:
    '''
    Converts a raster image to a tensor with 4 bands(RGB-NIR) of dimensions rasterImage.Height x rasterImage.width

    Parameters:
        rasterImage: 

    Returns:
        A tensor
    '''
    imgArray = np.zeros((rasterImage.height, rasterImage.width, rasterImage.count))

    #fill the array with rgbnir values
    for i in range(4):
        imgArray[ :, :,i] = rasterImage.read(i+1)

    return imgArray



def convertImages(rasterImages) -> np.array:
    '''
    Convert an array of raster images numpy array of tensors

    Parameters:
        rasterImages
        
    Returns:
        An array of tensors
    '''    
    images = np.array()

    for image in rasterImages:

        images.append(convertImage(image))

    return images
        




