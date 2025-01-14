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
import os  # To handle file paths
import pandas as pd
import json
import csv

# Load the JSON file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)

# Define parsing functions for different resource types
def parse_patient(patient):
    return {
        "id": patient.get("id"),
        "name": " ".join(patient.get("name", [{}])[0].get("given", []) + [patient.get("name", [{}])[0].get("family", "")]),
        "gender": patient.get("gender"),
        "birthDate": patient.get("birthDate"),
        "address": patient.get("address", [{}])[0].get("text"),
    }

def parse_condition(condition):
    return {
        "id": condition.get("id"),
        "diagnosis": condition.get("code", {}).get("coding", [{}])[0].get("display"),
        "status": condition.get("clinicalStatus", {}).get("coding", [{}])[0].get("code"),
        "category": ", ".join([c.get("coding", [{}])[0].get("display", "") for c in condition.get("category", [])]),
    }

def parse_careplan(careplan):
    return {
        "id": careplan.get("id"),
        "description": careplan.get("description"),
        "activities": ", ".join([
            act["detail"]["code"]["coding"][0]["display"]
            for act in careplan.get("activity", [])
        ]),
    }

def parse_diagnosticreport(report):
    return {
        "id": report.get("id"),
        "tests": ", ".join([result.get("display", "") for result in report.get("result", [])]),
        "status": report.get("status"),
        "issued": report.get("issued"),
    }

# Process the data and organize by resource type
parsed_data = {
    "Patient": [],
    "Condition": [],
    "CarePlan": [],
    "DiagnosticReport": []
}

for entry in data:
    resource_type = entry.get("resourceType")
    if resource_type == "Patient":
        parsed_data["Patient"].append(parse_patient(entry))
    elif resource_type == "Condition":
        parsed_data["Condition"].append(parse_condition(entry))
    elif resource_type == "CarePlan":
        parsed_data["CarePlan"].append(parse_careplan(entry))
    elif resource_type == "DiagnosticReport":
        parsed_data["DiagnosticReport"].append(parse_diagnosticreport(entry))

# Save parsed data to CSV files
output_files = {}
for resource_type, entries in parsed_data.items():
    if entries:  # Only create a CSV file if there are entries for this type
        output_path = f'parsed_{resource_type.lower()}.csv'
        with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=entries[0].keys())
            writer.writeheader()
            writer.writerows(entries)
        output_files[resource_type] = output_path

output_files