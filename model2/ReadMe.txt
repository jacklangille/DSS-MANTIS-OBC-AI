#this is directory for all files related to cnn model2

create a CNN model using tensor flow

input: 
4 channel rgb, nir image with attached metadeta such as location coordinates and timestamp.
    - paired metadata must not be lost while image goes through inferencing process


inference: 
-identify areas of interest: forests
-retrieve nir value and rgb value from forests

Two times of interest throughout the year
1. Budding season- spring
    - leaves growing on trees (nir increases over time)
2. Leaf loss season - Fall
    - leaves falling off of trees (nir decreases over time)
    
Also keeping record of leaf colour from budding season to end of leaf loss season

output:
- nir and rgb values of areas of interest of image are sent with images metadata to temporal change model 



