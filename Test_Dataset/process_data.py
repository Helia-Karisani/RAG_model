import pandas as pd
import jsonschema
import fhirpy
import json

#print("Environment is set up and libraries are working!")
#------ above lines should work

# Load the provided JSON file
# Load the data file

import json
import os

# Dynamically determine the base directory of the script
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "Epic_Test_Data.json")

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Error: File not found at {file_path}")

# Load the provided JSON file
with open(file_path, "r") as file:
    data = json.load(file)

#print(f"Looking for file at: {file_path}")



