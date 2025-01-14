# For FHIR data handling
from fhir.resources.patient import Patient  # Example: Work with Patient resources
from fhir.resources.observation import Observation  # Example: Work with Observation resources
from fhir.resources.bundle import Bundle  # Example: Work with Bundles
from fhir.resources.condition import Condition  # Example: Work with Conditions

# For US Core FHIR data
# If additional US Core-specific handling is needed
# Uncomment if you use US Core extensions
# from fhir.core.core import USCorePatient

# For FHIR utilities and validators
from fhirpath import FHIRPath  # For querying FHIR data
from fhirpy import SyncFHIRClient  # For interacting with FHIR servers

# For NLP and RAG pipeline
from transformers import pipeline  # Text-generation and classification

# Standard Python imports (if applicable)
import json  # For loading and saving JSON
import csv
import os  # To handle file paths
import pandas as pd

# Load the JSON file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)

# Prepare the CSV output
csv_output_path = 'resources.csv'

# Extract the required information and write to CSV
with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['id', 'resourceType'])  # Write header

    for entry in data:
        id_value = entry.get('id', '')
        resource_type = entry.get('resourceType', '')
        writer.writerow([id_value, resource_type])  # Write rows

csv_output_path