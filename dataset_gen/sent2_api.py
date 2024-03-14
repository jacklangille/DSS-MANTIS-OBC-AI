import evalscripts as eva
import matplotlib.image as img
from sentinelhub import SentinelHubRequest, SHConfig, DataCollection, MimeType, CRS, BBox, bbox_to_dimensions

config = SHConfig() # API keys are set as environment variables in ~/.zshrc

# coords = [min_lon, min_lat, max_lon, max_lat]
# coords define SW corner and NE corner of bounding box

nw = (-68.58604112771494, 43.425172798679824) 
ne = (-64.74841888575303, 43.425172798679824)
sw = (-68.58604112771494, 38.63052616537985)
se = (-64.74841888575303,38.63052616537985)

COORDS = [sw[0], sw[1], ne[0], ne[1]]
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
