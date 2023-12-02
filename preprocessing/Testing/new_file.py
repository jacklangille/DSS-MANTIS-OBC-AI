import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# sample image
img_path = 'images/Casa_Grande_Arizona.png'
img = image.load_img(img_path, target_size=(256, 256))  # target_size can be adjusted as needed
img_array = image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # batch dimension

# Displaying the original image
plt.imshow(img_array[0] / 255.0)  # Normalizing for display
plt.title('Original Image')
plt.show()

# Radiometric correction (pixel value normalization)
normalized_img = img_array / 255.0

# Corrected image display
plt.imshow(normalized_img[0])
plt.title('Radiometrically Corrected Image')
plt.show()

# Converting the TensorFlow tensor to a NumPy array with the appropriate data type - the value range can be adjusted
original_image_np = (img_array[0] / 255.0).numpy() * 255.0
corrected_image_np = (normalized_img[0]).numpy() * 255.0

# Saving generated correct image  into other folder
result_folder = 'result_images'
corrected_img_path = os.path.join(result_folder, 'radiometrically_corrected_image.png')
plt.imsave(corrected_img_path, corrected_image_np.astype(np.uint8))

print(f"Radiometrically corrected image saved at: {corrected_img_path}")
