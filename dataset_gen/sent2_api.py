import pandas as pd
import matplotlib.image as img
from sentinelhub import SentinelHubRequest, SHConfig, DataCollection, MimeType, CRS, BBox, bbox_to_dimensions, Geometry
import evalscripts as eva

CONFIG = SHConfig() 
OUTPUT_DIR = "../dataset_gen/results/"
RES = 20 # Resolution in meters
TIME_INTERVAL = ("2023-10-30", "2023-11-6")

# Original coordinates
coordinates =[4.1, 62.04, 4.887440854041823, 62.39932626325639]
# Create a bbox from the original coordinates
bbox = BBox(bbox=coordinates, crs=CRS.WGS84)

# Calculate dimensions to see if it exceeds the 2500 pixel limit
dimensions = bbox_to_dimensions(bbox, resolution=RES)

print(f"Original dimensions: {dimensions}")

# Adjusted request with new_bbox
request = SentinelHubRequest(
    evalscript=eva.algae,  
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=TIME_INTERVAL,
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.JPG)
    ],
    bbox=bbox,  # Use the adjusted BBox object
    size=dimensions,  # Use the new dimensions
    config=CONFIG
)

img_response = request.get_data()
for idx, img_data in enumerate(img_response):
    img_name = f"{TIME_INTERVAL[0]}_to_{TIME_INTERVAL[1]}_{idx}.jpg"
    img.imsave(OUTPUT_DIR + img_name, img_data)