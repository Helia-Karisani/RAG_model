import json
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
import os  # To handle file paths
from transformers import pipeline
import pandas as pd

# Initialize the AI pipeline
try:
    classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
except Exception as e:
    print(f"Error loading pipeline: {e}")
    exit()

# Load the data file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)

# Function to process health information
def process_health_information(data):
    for idx, entry in enumerate(data):
        # Extract category
        category = entry.get("category", [])
        category_display = ""
        if isinstance(category, list) and len(category) > 0:
            first_category = category[0]
            if isinstance(first_category, dict):
                coding = first_category.get("coding", [])
                if isinstance(coding, list) and len(coding) > 0:
                    first_coding = coding[0]
                    if isinstance(first_coding, dict):
                        category_display = first_coding.get("display", "Unknown")

        # Extract display name
        display_name = entry.get("display", "Unknown")

        # Extract out-of-range information
        out_of_range = entry.get("outOfRange", False)

        # Skip items where both category and display name are missing
        if not category_display and display_name == "Unknown":
            continue

        # Analyze with AI model for importance
        is_important = "No"
        if display_name != "Unknown":
            try:
                prediction = classifier(display_name)
                if prediction and len(prediction) > 0:
                    label = prediction[0].get("label", "")
                    if label == "LABEL_1":  # Assuming LABEL_1 corresponds to importance
                        is_important = "Yes"
            except Exception as e:
                print(f"Error processing item {idx}: {e}")

        # Print results
        print(f"Item {idx}:")
        print(f"  Category: {category_display if category_display else 'Unknown'}")
        print(f"  Display Name: {display_name}")
        print(f"  Out of Range: {'Yes' if out_of_range else 'No'}")
        print(f"  Evaluated as Important: {is_important} (AI)")
        print()

# Run the function
process_health_information(data)
#------------------------------------------------------------------------------------
# Analyze the category field in each item
def analyze_category_field(data):
    results = []
    for idx, entry in enumerate(data):
        category = entry.get("category", None)  # Get category or None if not present

        # Determine the type/status of the category
        if isinstance(category, list) and len(category) > 0:
            status = "It is a non-empty list"
        elif isinstance(category, list) and len(category) == 0:
            status = "It is an empty list"
        elif isinstance(category, str) and category.strip() == "":
            status = "It is an empty string"
        elif isinstance(category, str):
            status = "It is a string"
        elif category is None:
            status = "It is None"
        else:
            status = "Unknown type"

        # Add the result for this entry
        results.append(f"{idx}. {status}")

    return results


# Get the category analysis
category_analysis = analyze_category_field(data)
'''
# Output the analysis
for line in category_analysis:
    print(line)
'''


# Analyze the first element of the category field in each item
def analyze_first_category_element(data):
    results = []
    for idx, entry in enumerate(data):
        category = entry.get("category", [])  # Get category or default to an empty list

        # Check if the first element of category is a dictionary
        if isinstance(category, list) and len(category) > 0:
            if isinstance(category[0], dict):
                status = "It is a dictionary"
            else:
                status = "It is not a dictionary"
        else:
            status = "Category is not a valid list or is empty"

        # Add the result for this entry
        results.append(f"{idx}. {status}")

    return results


# Get the analysis of the first category element
category_analysis = analyze_first_category_element(data)
'''
# Print the results
for line in category_analysis:
    print(line)
'''