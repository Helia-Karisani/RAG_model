import json
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
def process_health_information_with_ai(data):
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
                        category_display = first_coding.get("display", "")

        # Extract display name
        display_name = entry.get("display", "Unknown")

        # Skip if display_name is empty
        if not display_name:
            continue

        # Analyze with AI model
        try:
            prediction = classifier(display_name)
            is_important = "No"
            if prediction and len(prediction) > 0:
                label = prediction[0].get("label", "")
                if label == "LABEL_1":  # Assuming LABEL_1 corresponds to importance
                    is_important = "Yes"

            # Print results
            print(f"Item {idx}:")
            print(f"  Category: {category_display}")
            print(f"  Display Name: {display_name}")
            print(f"  Evaluated as Important: {is_important} (AI)")
            print()

        except Exception as e:
            print(f"Error processing item {idx}: {e}")

# Run the function
process_health_information_with_ai(data)

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