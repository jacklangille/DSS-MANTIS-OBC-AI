import rasterio

tiff_path = 'C:/DSS/DSS FOLDER 1 11TH NOV\DSS-MANTIS-OBC-AI/Images/tree-phen/trees_feb2020-Dec2021_10m/2020-02-21.tiff'


with rasterio.open(tiff_path) as src:
 
    data = src.read(1)  
    metadata = src.meta


print(f"Raster Shape: {data.shape}")
print(f"Raster Metadata: {metadata}")