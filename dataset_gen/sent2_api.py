import evalscripts as eva
import matplotlib.image as img
from sentinelhub import SentinelHubRequest, SHConfig, DataCollection, MimeType, CRS, BBox, bbox_to_dimensions, SentinelHubDownloadClient

config = SHConfig() # API keys are set as environment variables in ~/.zshrc

# coords = [min_lon, min_lat, max_lon, max_lat]
# coords define SW corner and NE corner of bounding box
# date = YYYY-MM-DD (dont pad day with 0!)

COORDS = [-65.106524, 44.525456, -65.085068, 44.510646]
DATE = "2021-06-17"
RES = 30 # Resolution in meters
OUTPUT_DIR = "../dataset_gen/results/"

def main():
    bbox = BBox(bbox=COORDS, crs=CRS.WGS84)
    evalscript = eva.rgbnir
    request = SentinelHubRequest(
        data_folder=OUTPUT_DIR,
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=(DATE)
            )
        ],
        responses=[
            SentinelHubRequest.output_response("default",MimeType.JPG)
        ],
        bbox=bbox,
        size=bbox_to_dimensions(bbox, resolution=RES),
        config=config
    )

    image_response = request.get_data()
    img_name = f"{DATE}_test.jpg"
    img.imsave(OUTPUT_DIR+img_name, image_response[0])
if __name__ == "__main__":
    main()