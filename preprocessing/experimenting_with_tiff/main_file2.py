import rasterio
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import numpy as np
from skimage import exposure, color, io, feature
from skimage.measure import shannon_entropy
from skimage import img_as_ubyte
from skimage.feature import greycomatrix
from sklearn.decomposition import PCA
from skimage import greycomatrix

tiff_path = 'C:/DSS/DSS FOLDER 1 11TH NOV/DSS-MANTIS-OBC-AI/Images/tree-phen/trees_feb2020-Dec2021_10m/2020-02-21.tiff'

with rasterio.open(tiff_path) as src:
    data = src.read(1)
    metadata = src.meta

# Min max scaling
min_max_scaler = MinMaxScaler()
data_minmax = min_max_scaler.fit_transform(data.reshape(-1, 1)).reshape(data.shape)

# Z-score normalization
zscore_scaler = StandardScaler()
data_zscore = zscore_scaler.fit_transform(data.reshape(-1, 1)).reshape(data.shape)

# Separating RGB and NIR bands - Doesn't apply to these TIFF files necessarily
rgb_bands = bands[:3]  # Assuming bands 1, 2, 3 are RGB
nir_band = bands[-1]  # Assuming the last band is NIR

hypercube = np.stack([rgb_bands[0], rgb_bands[1], rgb_bands[2], nir_band], axis=-1)

# Normalization and feature extraction can be done on this hypercube
hypercube_reshaped = hypercube.transpose(1, 2, 0)

#NDVI (Normalized Difference Vegetation Index)
ndvi = (hypercube_reshaped[:, :, 3] - hypercube_reshaped[:, :, 0]) / (hypercube_reshaped[:, :, 3] + hypercube_reshaped[:, :, 0])

# Texture analysis using GLCM
gray_img = img_as_ubyte(color.rgb2gray(hypercube_reshaped))
glcm = greycomatrix(gray_img, [1], [0], symmetric=True, normed=True)

# Computing entropy
entropy = shannon_entropy(gray_img)

# PCA related code
pca = PCA(n_components=3)
pca_result = pca.fit_transform(hypercube_reshaped.reshape(-1, 4))

print(f"NDVI Shape: {ndvi.shape}")
print(f"GLCM Shape: {glcm.shape}")
print(f"Entropy: {entropy}")
print(f"PCA Result Shape: {pca_result.shape}")
