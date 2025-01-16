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

    def parse_diagnosticreport(report, patient_id):
        encoded_data = report.get("presentedForm", [{}])[0].get("data", "")
        try:
            decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            decoded_data = "No meaningful data available"

        return {
            "patient_id": patient_id,
            "tests": ", ".join([result.get("display", "") for result in report.get("result", []) if result.get("display")]),
            "data": decoded_data if len(decoded_data) > 0 and decoded_data != "0" else "No relevant information provided.",
            "Time": report.get("effectiveDateTime", "No time available")
        }

    # Find the single patient in the data
    patient_data = None
    diagnostic_reports = []
    for entry in data:
        resource_type = entry.get("resourceType")
        if resource_type == "Patient":
            patient_data = parse_patient(entry)
        elif resource_type == "DiagnosticReport" and patient_data:
            diagnostic_reports.append(parse_diagnosticreport(entry, patient_data["id"]))

    if not patient_data:
        print("No patient data found in the JSON.")
        exit()

    # Generate insights focusing only on the diagnosis from reports
    def extract_insights(patient, diagnostic_reports):
        insights = []
        insights.append(f"Patient {patient['id']} details: {patient['name']}, {patient['gender']}, {patient['birthDate']}, residing at {patient['address']}.")
        for report in diagnostic_reports:
            if "No relevant information provided." in report["data"]:
                continue
            # Focus only on the diagnosis in insights
         #   diagnosis_insight = f"Patient diagnosed with tests: {report['tests']} on {report['Time']}"
            insights.append(f"Patient diagnosed with tests: {report['tests']} on {report['Time']}")
        return insights

    insights = extract_insights(patient_data, diagnostic_reports)

    # Summarization
    summary_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def generate_summary(insights):
        summaries = []
        for insight in insights:
            input_length = len(insight.split())
            max_len = min(100, input_length + 20)  # Dynamically adjust max_length
            try:
                summary = summary_pipeline(insight, max_length=max_len, min_length=max(20, max_len // 2), do_sample=False)
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
