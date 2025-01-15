import json
import csv
import base64
import os
from transformers import pipeline
import pandas as pd

# Disable symlink warning for Windows
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

if __name__ == "__main__":
    # Load the JSON file
    with open("Aetna_Test_Data_Fixed.json", "r") as file:
        data = json.load(file)

    # Parsing functions
    def parse_patient(patient):
        return {
            "id": patient.get("id"),
            "name": " ".join(patient.get("name", [{}])[0].get("given", []) + [patient.get("name", [{}])[0].get("family", "")]),
            "gender": patient.get("gender"),
            "birthDate": patient.get("birthDate"),
            "address": patient.get("address", [{}])[0].get("text"),
            "Time": patient.get("meta", {}).get("lastUpdated", "No time available")
        }

    def parse_condition(condition, patient_id):
        return {
            "patient_id": patient_id,
            "diagnosis": condition.get("code", {}).get("coding", [{}])[0].get("display"),
            "category": ", ".join([c.get("coding", [{}])[0].get("display", "") for c in condition.get("category", [])]),
            #"Time": condition.get("recordedDate", "No time available")
            "Time": condition.get("meta", {}).get("lastUpdated", "No time available")
        }

    # Find the single patient in the data
    patient_data = None
    conditions_data = []
    for entry in data:
        resource_type = entry.get("resourceType")
        if resource_type == "Patient":
            patient_data = parse_patient(entry)
        elif resource_type == "Condition" and patient_data:
            conditions_data.append(parse_condition(entry, patient_data["id"]))

    if not patient_data:
        print("No patient data found in the JSON.")
        exit()

    # Extract insights
    def extract_insights(patient, conditions):
        insights = []
        insights.append(f"Patient {patient['id']} details: {patient['name']}, {patient['gender']}, {patient['birthDate']}, residing at {patient['address']}.")
        for condition in conditions:
            insights.append(f"Patient diagnosed with {condition['diagnosis']} under category {condition['category']} on {condition['Time']}.")
        return insights

    insights = extract_insights(patient_data, conditions_data)

    # Summarization
    summary_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    def generate_summary(insights):
        summaries = []
        for insight in insights:
            input_length = len(insight.split())
            max_len = min(50, input_length + 10)  # Dynamically adjust max_length
            try:
                summary = summary_pipeline(insight, max_length=max_len, min_length=max(10, max_len // 2), do_sample=False)
                summaries.append(summary[0]['summary_text'])
            except Exception as e:
                summaries.append(f"Error in generating summary: {e}")
        return summaries

    summaries = generate_summary(insights)

    # Save to CSV
    output_df = pd.DataFrame({"Insight": insights, "Summary": summaries})
    output_csv_path = 'patient_insights_summaries.csv'
    output_df.to_csv(output_csv_path, index=False)

    print(f"Insights and summaries saved to {output_csv_path}")