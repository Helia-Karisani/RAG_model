import json
import pandas as pd


# Load the data file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)

# Evaluate importance for items without a range
def evaluate_importance(display_name):
    critical_terms = [
        "Acute", "Severe", "Critical", "Failure", "High", "Low", "Cancer", "Infarction",
        "Blood Pressure", "Heart Rate", "Glucose", "Oxygen Saturation", "Liver Enzymes",
        "Cholesterol", "Thyroid", "Creatinine"
    ]
    for term in critical_terms:
        if term.lower() in display_name.lower():
            return True
    return display_name != "Unknown Display"  # Fallback: mark as important if display_name is not empty

# Print all relevant health information
def print_health_information(data):
    for idx, entry in enumerate(data):
        # Safely access category
        category = entry.get("category", [])
        if isinstance(category, list) and len(category) > 0:
            first_category = category[0]
            if isinstance(first_category, dict):
                coding = first_category.get("coding", [])
                if isinstance(coding, list) and len(coding) > 0:
                    first_coding = coding[0]
                    category_display = first_coding.get("display", "")
                else:
                    category_display = ""
            else:
                category_display = ""
        else:
            category_display = ""

        # Safely access clinicalStatus
        clinical_status = entry.get("clinicalStatus", {}).get("coding", [{}])[0].get("code", "")

        # Extract display name
        code_info = entry.get("code", {}).get("coding", [{}])[0]
        display_name = code_info.get("display", "Unknown Display")

        # Check if value is out of range
        value = entry.get("valueQuantity", {}).get("value", None)
        reference_range = entry.get("referenceRange", [])
        out_of_range = False
        if value is not None and isinstance(reference_range, list) and len(reference_range) > 0:
            low = reference_range[0].get("low", {}).get("value", None)
            high = reference_range[0].get("high", {}).get("value", None)
            if (low is not None and value < low) or (high is not None and value > high):
                out_of_range = True

        # Evaluate items without a range
        evaluated_as_important = False
        if not out_of_range and len(reference_range) == 0:  # No range provided
            evaluated_as_important = evaluate_importance(display_name)

        # Print relevant information for Health Concern or Laboratory
        if category_display in ["Health Concern", "Laboratory"]:
            print(f"Item {idx}:")
            print(f"  Category: {category_display}")
            print(f"  Display Name: {display_name}")
            if category_display == "Laboratory":
                print(f"  Out of Range: {'Yes' if out_of_range else 'No'}")
            print(f"  Evaluated as Important: {'Yes' if evaluated_as_important else 'No'}")
            print()

# Run the function
print_health_information(data)
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