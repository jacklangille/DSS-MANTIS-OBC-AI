import rasterio
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import numpy as np

tiff_path = 'C:/DSS/DSS FOLDER 1 11TH NOV/DSS-MANTIS-OBC-AI/Images/tree-phen/trees_feb2020-Dec2021_10m/2020-02-21.tiff'


with rasterio.open(tiff_path) as src:
 
    data = src.read(1)  
    metadata = src.meta

    bands = src.read()


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

# Separating RGB and NIR bands- Doesn't apply to these tiff files necessarily
rgb_bands = bands[:3]  # Assuming bands 1, 2, 3 are RGB
nir_band = bands[-1]    # Assuming the last band is NIR

hypercube = np.stack([rgb_bands[0], rgb_bands[1], rgb_bands[2], nir_band], axis=-1)


#Normalization and feature extraction can be done on this hypercube
hypercube_reshaped = hypercube.transpose(1, 2, 0)

# Assuming 'hypercube_reshaped' is the 3D hypercube obtained previously

# Alternatively, looping through all pixels in a specific band (like band 1)
band_0_values = hypercube_reshaped[:, :, 1]

print("Pixel values for all pixels in band 0:", band_0_values)

if 0 <= 100 < hypercube_reshaped.shape[0] and 0 <= 150 < hypercube_reshaped.shape[1]:
    pixel_values = hypercube_reshaped[100, 150, :]  # Getting pixel value at row=100, column=150 for all bands - example
    print("Pixel values at row=100, column=150 for all bands:", pixel_values)
else:
    print("Invalid row or column index.")
