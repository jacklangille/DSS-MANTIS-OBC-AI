"""
    This is a sample script for how to download Sentinel-2 satellite imagery via 
    The Sentinel Hub API. 
    
    Before running this script: 
    
        1. Get an API key (for a free month trial) from  https://www.sentinel-hub.com/develop/api/. In the future, MANTIS may get a paid account.
        
        2. Based on your user account, add your id, and your secret to the variables below this comment section.
        
        3. Ensure the 'input' variable includes the file path to a .txt file with a list of dates for images you would like to retrieve.
        Date format = YYYY-MM-DD (if the day is a single digit, don't pad it with a zero), and list each date on a new line of a .txt file. 
        
        4. Specify the 
    
    For more details, here is a link to the documentation: 
    
    Notes: 
    1. this script downloads RGB and NIR imagery to a .TIFF format.
    Imagery that includes a NIR band must be stored in a TIFF file
"""


id = 'replace with SentinelHub id'
secret = 'replace with SentinelHub secret key'

import matplotlib.image as img

from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    MimeType,
    MosaickingOrder,
    SentinelHubRequest,
    SHConfig,
    bbox_to_dimensions
)

"""
    IMPORTANT: 
        before you can use this, you must make an account at 
        https://www.sentinel-hub.com/develop/api/, 
        and you will have a free month trial.
"""

config = SHConfig()
config.sh_client_id = id
config.sh_client_secret = secret

# List of dates, each on a new line of a .txt file. 
# date format: YYYY-MM-DD (if DD is a single digit, don't pad it with a zero)
input_file = "./trees_batch1_Feb2020-Dec2021.txt"
output_folder = "../Images/tree-phen/trees_Feb2020-Dec2021"

import evalscripts as eva

# specify the bands to download
evalscript = eva.rgbnir

# Bounding box of coordinates around Lake Torment, Nova Scotia
#coords = [-64.731232, 44.752646, -64.748555, 44.714253]

# bounding box of some forest, in the middle of Nova Scotia
coords = [-65.106524, 44.525456, -65.085068, 44.510646]

file_format ="tiff"
mimetype = MimeType.TIFF

bbox = BBox(bbox=coords, crs=CRS.WGS84)

imageSize = bbox_to_dimensions(bbox, resolution=30)

with open(input_file, "r") as file:
    data = file.readlines()
dates = []
for date in data:
    dates.append(date.strip())

for date in dates: 
    
    file_name = f"{date}.{file_format}"
    print(file_name, end='')
    date.strip()
    time_range = (date, date)

    request_image = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=time_range,
                mosaicking_order=MosaickingOrder.LEAST_CC,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", mimetype)],
        bbox     = bbox,
        size     = imageSize,
        config   = config,
    )
    
    images = request_image.get_data()
    
    img.imsave(f'{output_folder}/{file_name}', images[0])
    
    print(' -- downloaded')