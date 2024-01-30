import rasterio
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

tiff_path = 'C:/DSS/DSS FOLDER 1 11TH NOV/DSS-MANTIS-OBC-AI/Images/tree-phen/trees_feb2020-Dec2021_10m/2020-02-21.tiff'


with rasterio.open(tiff_path) as src:
 
    data = src.read(1)  
    metadata = src.meta


print(f"Raster Shape: {data.shape}")
print(f"Raster Metadata: {metadata}")

# Min max scaling
min_max_scaler = MinMaxScaler()
data_minmax = min_max_scaler.fit_transform(data.reshape(-1, 1)).reshape(data.shape)

print(f"Raster Shape: {data.shape}")
print(f"Raster Metadata: {metadata}")


# z-score normalization
zscore_scaler = StandardScaler()
data_zscore = zscore_scaler.fit_transform(data.reshape(-1, 1)).reshape(data.shape)


print(f"Raster Shape: {data.shape}")
print(f"Raster Metadata: {metadata}")
