import json

# Load the data file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)

# Extract health concerns and laboratory results
def get_top_health_or_lab_result(data):
    results = []
    for entry in data:
        resource_type = entry.get("resourceType")
        category = entry.get("category", [{}])[0].get("coding", [{}])[0].get("display", "")
        code_info = entry.get("code", {}).get("coding", [{}])[0]
        display_name = code_info.get("display", "Unknown Display")

        # Check for health concerns or lab results
        if resource_type in ["Condition", "DiagnosticReport"]:
            if category in ["Health Concern", "Laboratory"]:
                results.append({
                    "name": display_name,
                    "lastUpdated": entry.get("meta", {}).get("lastUpdated", ""),
                    "category": category
                })

    # Sort by last updated date and return the top result's name
    if results:
        results.sort(key=lambda x: x["lastUpdated"], reverse=True)
        return results[0]["name"] if results else None
    return None

# Get the top health concern or laboratory result
top_result = get_top_health_or_lab_result(data)
print(top_result)