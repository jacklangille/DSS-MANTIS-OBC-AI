'''
This file

Section 1 and Section 2 will be replaced by Aniket's Code
'''
import tensorflow as tf
import numpy as np
import matplotlib as img 
import rasterio
import os
import image_process as ip
from rasterio.plot import show
import json
import keras
import cv2


## Functions
def openImage(path):
    
    rasterImage = rasterio.open(path)

    return rasterImage

def convertImage(rasterImage):
    '''
    Converts a raster image to a tensor with 4 bands(RGB-NIR) of dimensions rasterImage.Height x rasterImage.width

    Parameters:
        rasterImage: 

    Returns:
        A tensor
    '''

    #set dimension of 3d-array to image height, width and number of bands
    imgArray = np.zeros((rasterImage.height, rasterImage.width, rasterImage.count))

    #fill the array with rgbnir values
    for i in range(4):
        imgArray[ :, :,i] = rasterImage.read(i+1)


    return imgArray



def prepareImage(image):
    '''
    This method does all preproccessing steps requires to prepare the image

    '''
    
    # Split the image into Red, Green, Blue, and NIR channels
    r, g, b, nir = cv2.split(image)

    # Normalize each channel
    r_normalized = (r - np.min(r)) / (np.max(r) - np.min(r))
    g_normalized = (g - np.min(g)) / (np.max(g) - np.min(g))
    b_normalized = (b - np.min(b)) / (np.max(b) - np.min(b))
    nir_normalized = (nir - np.min(nir)) / (np.max(nir) - np.min(nir))

    # Recombine the channels
    normalized_image = cv2.merge([r_normalized, g_normalized, b_normalized, nir_normalized])


    return normalized_image





def makePrediction(imgID):

    ## Setup


    # load model
    model = tf.keras.models.load_model('model2/my_model2_I1.keras')

    # open output file
    file1 = open("treeOutput.txt" , "a" )


    ## Section 1
    # recieve image + store metadata
    rasterImage = openImage(tiff_file)
    img = convertImage(rasterImage)



    ## Section 2
    # preprocess image

    img_prepared = prepareImage(img)

    print(img_prepared.shape)
    ## Section 3
    # make inference
    prediction = model.predict(img_prepared)

    
    index = prediction.argmax()
    conf = max(prediction) * 100
    

    # Section 4
    # print results to file


 
    # Writing to file
    file1.write("\nImg: ", imgID, "Class: ", index,  " With ", conf, "percent confidence.")
    
    # Closing file
    file1.close()

    return


image_height = 160
image_width = 175
bands = 4


tiff_file = 'model2/2020-02-21.tiff'

makePrediction("T01")