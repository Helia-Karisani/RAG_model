import json

# Load the data file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)

# Extract top health concerns or laboratory results
def get_top_10_items(data):
    results = []
    seen_items = set()  # To avoid repetitions

    for idx, entry in enumerate(data):
        category = entry.get("category", [])  # Get category or default to an empty list

        # Safely extract the display field from category
        if isinstance(category, list) and len(category) > 0:  # Ensure category is a non-empty list
            first_category = category[0]
            if isinstance(first_category, dict):  # Ensure the first element is a dictionary
                coding = first_category.get("coding", [])
                if isinstance(coding, list) and len(coding) > 0:  # Ensure "coding" is a non-empty list
                    first_coding = coding[0]
                    if isinstance(first_coding, dict):  # Ensure the first element of "coding" is a dictionary
                        category_display = first_coding.get("display", "")
                    else:
                        category_display = ""  # Default if "coding[0]" is not a dictionary
                else:
                    category_display = ""  # Default if "coding" is not a valid list
            else:
                category_display = ""  # Default if "category[0]" is not a dictionary
        else:
            category_display = ""  # Default if "category" is not a valid list

        # Extract display name of the condition or lab result
        code_info = entry.get("code", {}).get("coding", [{}])[0]
        display_name = code_info.get("display", "Unknown Display")

        # Check for health concerns or lab results and avoid duplicates
        if category_display in ["Health Concern", "Laboratory"] and display_name not in seen_items:
            results.append((idx, entry.get("meta", {}).get("lastUpdated", ""), display_name))
            seen_items.add(display_name)

    # Sort by last updated date and limit to top 10
    results.sort(key=lambda x: x[1], reverse=True)  # Sort by lastUpdated timestamp
    top_10_items = [item[0] for item in results[:10]]  # Extract only the item numbers

    return top_10_items

# Get the top 10 item numbers
top_10_item_numbers = get_top_10_items(data)

# Print only the item numbers
for item_number in top_10_item_numbers:
    print(item_number)







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