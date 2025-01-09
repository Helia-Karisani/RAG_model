import json

# Load the data file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)


# Function to debug the exact condition
def debug_exact_condition(data):
    results = []

    for idx, entry in enumerate(data):
        # Step 1: Check category.display
        category = entry.get("category", [])
        if isinstance(category, list) and len(category) > 0:
            first_category = category[0]
            if isinstance(first_category, dict):
                coding = first_category.get("coding", [])
                if isinstance(coding, list) and len(coding) > 0:
                    first_coding = coding[0]
                    if isinstance(first_coding, dict):
                        category_display = first_coding.get("display", "")
                    else:
                        category_display = ""
                else:
                    category_display = ""
            else:
                category_display = ""
        else:
            category_display = ""

        # Step 2: Check clinicalStatus for Health Concerns
        clinical_status = entry.get("clinicalStatus", {}).get("coding", [{}])[0].get("code", "")

        # Step 3: Check valueQuantity for Laboratory Results
        value = entry.get("valueQuantity", {}).get("value", None)
        reference_range = entry.get("referenceRange", [])
        out_of_range = False
        if value is not None and isinstance(reference_range, list) and len(reference_range) > 0:
            low = reference_range[0].get("low", {}).get("value", None)
            high = reference_range[0].get("high", {}).get("value", None)
            if (low is not None and value < low) or (high is not None and value > high):
                out_of_range = True

        # Debugging outputs
        print(f"\nProcessing item {idx}:")
        print(f"  Category Display: {category_display}")
        print(f"  Clinical Status: {clinical_status}")
        print(f"  Out of Range: {out_of_range}")

        # Match the conditions from the original code
        if category_display == "Health Concern" and clinical_status in ["active", "recurrence"]:
            results.append(idx)
        elif category_display == "Laboratory" and out_of_range:
            results.append(idx)

    # Print the results
    if results:
        print(f"\nItems meeting the exact condition: {results}")
    else:
        print("\nNo items met the exact condition.")

# Run the function
debug_exact_condition(data)
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