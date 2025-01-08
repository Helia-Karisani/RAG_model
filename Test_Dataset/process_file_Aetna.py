import json

# Load the data file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)


# Extract health concerns and laboratory results
def get_top_health_or_lab_result(data):
    results = []
    for entry in data:
        resource_type = entry.get("resourceType", "")
        category = entry.get("category", None)  # Default to None if not present

        # Handle `category` safely, accounting for various formats
        if isinstance(category, list) and len(category) > 0:  # Case 1: category is a list
            category_display = category[0].get("coding", [{}])[0].get("display", "")
        elif isinstance(category, dict):  # Case 2: category is a dictionary
            category_display = category.get("coding", [{}])[0].get("display", "")
        elif isinstance(category, str):  # Case 3: category is a string
            category_display = category
        else:  # Case 4: category is missing or invalid
            category_display = ""

        # Extract display name of the condition or lab result
        code_info = entry.get("code", {}).get("coding", [{}])[0]
        display_name = code_info.get("display", "Unknown Display")

        # Check for health concerns or lab results
        if resource_type in ["Condition", "DiagnosticReport"] and category_display in ["Health Concern", "Laboratory"]:
            results.append({
                "name": display_name,
                "lastUpdated": entry.get("meta", {}).get("lastUpdated", ""),
                "category": category_display
            })

    # Sort by last updated date and return the top result's name
    if results:
        results.sort(key=lambda x: x["lastUpdated"], reverse=True)
        return results[0]["name"]
    return "No valid health concern or laboratory result found"


# Get the top health concern or laboratory result
top_result = get_top_health_or_lab_result(data)
print("Top Result:", top_result)