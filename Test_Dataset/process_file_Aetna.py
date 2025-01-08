import json

# Load the data file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)

# Function to extract patient references and IDs
def extract_patient_references(data):
    references = {}
    for idx, item in enumerate(data):
        patient_id = None
        # Check if the item has a "subject" reference (e.g., Procedure, Condition)
        if "subject" in item and "reference" in item["subject"]:
            patient_id = item["subject"]["reference"]
        # Check if the item itself is a Patient resource
        elif item.get("resourceType") == "Patient" and "id" in item:
            patient_id = f"Patient/{item['id']}"

        if patient_id:
            if patient_id not in references:
                references[patient_id] = []
            references[patient_id].append(idx)

    return references


# Extract and group items by patient reference
grouped_items = extract_patient_references(data)

# Output the mapping of items to patient references
print(grouped_items)