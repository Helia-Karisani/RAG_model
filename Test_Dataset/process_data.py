import pandas as pd
import jsonschema
import fhirpy
import json

#print("Environment is set up and libraries are working!")
#------ above lines should work



# Load the provided JSON file
with open("Aetna_Test_Data_Fixed.json", "r") as file:
    data = json.load(file)

#hello

# Define a dictionary for normal ranges of common medical variables
# Updated to include variables mentioned in the JSON file
normal_ranges = {
    "Blood Pressure": {"systolic": (90, 120), "diastolic": (60, 80)},  # mmHg
    "BMI": (18.5, 24.9),  # kg/m^2
    "Heart Rate": (60, 100),  # bpm
    "Cholesterol": {"total": (125, 200), "LDL": (0, 100), "HDL": (40, 60)},  # mg/dL
    "Blood Sugar": (70, 100),  # fasting, mg/dL
    "Total score [AUDIT-C]": (0, 12),
    "Generalized anxiety disorder 7 item (GAD-7) total score": (0, 21),
    "MCHC [Mass/volume] by Automated count": (31, 37),  # g/dL
    "Leukocytes [#/volume] in Blood by Automated count": (4.0, 11.0),  # x10^9/L
    "Hematocrit [Volume Fraction] of Blood by Automated count": (37, 47),  # %
}

# Helper function to check if a value is in the normal range
def check_range(value, normal_range):
    if isinstance(normal_range, tuple):
        return normal_range[0] <= value <= normal_range[1]
    return False

# Analyze the JSON data to detect deviations and check for missing results
def analyze_data(data):
    deviations = []
    observed_tests = set()

    for entry in data:
        if entry.get("resourceType") == "Observation":
            # Extract the medical test name and value
            observation_name = entry.get("code", {}).get("text", "Unknown")
            value = entry.get("valueQuantity", {}).get("value")
            unit = entry.get("valueQuantity", {}).get("unit", "")

            # Track observed tests
            observed_tests.add(observation_name)

            # Check for specific medical tests and ranges
            if observation_name in normal_ranges:
                if isinstance(normal_ranges[observation_name], tuple):  # Single range (e.g., BMI)
                    if not check_range(value, normal_ranges[observation_name]):
                        deviations.append(
                            f"{observation_name} is out of range: {value} {unit} (Normal: {normal_ranges[observation_name]})"
                        )
                elif isinstance(normal_ranges[observation_name], dict):  # Multi-part range (e.g., Blood Pressure)
                    for sub_key, sub_range in normal_ranges[observation_name].items():
                        if sub_key in observation_name.lower() and not check_range(value, sub_range):
                            deviations.append(
                                f"{observation_name} ({sub_key}) is out of range: {value} {unit} (Normal: {sub_range})"
                            )

    # Check for tests in the dictionary but not in the observed tests
    for test in normal_ranges.keys():
        if test not in observed_tests:
            deviations.append(f"No Result for {test}")

    return deviations

# Analyze the data for deviations
deviations_detected = analyze_data(data)

# Display the detected deviations
for deviation in deviations_detected:
    print(deviation)
