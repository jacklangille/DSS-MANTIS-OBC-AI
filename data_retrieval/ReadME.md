# Data Retrivel: 

    For imagery retrieval,  download_imagery.py sends requests to the Sentinel-2 API to download imagery at certain coordinates at a certain data. 

    I Specified dates to retrieve data in the .txt files, and manually entered coordinates in the python script (This could be improved by writing the coordinates at the top of each .txt file, and altering the python script to automatically extract this)

    Before running the script, please follow the instructions in the first 20 lines of the script.

    Going forward, it may be beneficial to transition to using Google Earth Engine's API instead of Sentinel-2's for accessing iamgery. 
    
# Coordinates of batch files: 
trees_batch1_Feb2020-Dec2021.txt is used for images with this coordinates: 
{"type":"Polygon","coordinates":[[[-65.106524,44.525456],[-65.085068,44.525456],[-65.085068,44.510646],[-65.106524,44.510646],[-65.106524,44.525456]]]}

(-65.106524, 44.525456, -65.085068, 44.510646)

