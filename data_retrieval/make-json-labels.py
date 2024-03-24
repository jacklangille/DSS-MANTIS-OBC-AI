"""
    This code creates a blank json file with the image file name included for each image. 
    The json data will then need to be populated with image labels. 
    

"""

import os
import json

# Directory containing your images
image_directory = r"C:\\Users\\jdapa\Documents\\MANTIS\DSS-MANTIS-OBC-AI\\Images\\tree-phen\\trees_feb2020-Dec2021_10m"

#File path to the output .json file
output_file = r"C:\\Users\\jdapa\Documents\\MANTIS\DSS-MANTIS-OBC-AI\\Images\\trees_feb2020-Dec2021_10m_labels.json"

# Function to generate JSON structure
def generate_json(image_dir):
    
    image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

    json_data = []

    for image in image_files:
        json_object = {
            "filename": image,
            "annotations": ""  # You can add annotations manually 
        }
        json_data.append(json_object)

    return json_data

# Generate JSON
json_output = generate_json(image_directory)

# Writing the JSON data to a file
with open(output_file, 'w') as json_file:
    json.dump(json_output, json_file, indent=4)

print("JSON data has been written to 'C:\\Users\\jdapa\Documents\\MANTIS\DSS-MANTIS-OBC-AI\\Images\\trees_feb2020-Dec2021_10m_labels.json'")
