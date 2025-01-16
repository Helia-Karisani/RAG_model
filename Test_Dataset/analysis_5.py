import json
import base64
import os
import csv
import pandas as pd
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key="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"
)

if __name__ == "__main__":
    # Load the JSON file
    with open("Aetna_Test_Data_Fixed.json", "r") as file:
        data = json.load(file)

    # Parsing functions (using your original logic)
    def parse_patient(patient):
        return {
            "id": patient.get("id"),
            "name": " ".join(patient.get("name", [{}])[0].get("given", []) + [patient.get("name", [{}])[0].get("family", "")]),
            "gender": patient.get("gender"),
            "birthDate": patient.get("birthDate"),
            "address": patient.get("address", [{}])[0].get("text"),
            #"Time": patient.get("meta", {}).get("lastUpdated", "No time available")
        }

    def parse_diagnosticreport(report):
        encoded_data = report.get("presentedForm", [{}])[0].get("data", "")
        try:
            decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            decoded_data = "No meaningful data available"

        return {
            "tests": ", ".join([result.get("display", "") for result in report.get("result", []) if result.get("display")]),
            "data": decoded_data if len(decoded_data) > 0 and decoded_data != "0" else "No relevant information provided.",
            "Time": report.get("effectiveDateTime", "No time available")
        }

    def parse_care_plan(care_plan):
        return {
            "category": ", ".join([c.get("coding", [{}])[0].get("display", "") for c in care_plan.get("category", [])]),
            #"description": care_plan.get("description", "No description available"),
            "status": care_plan.get("status", "No status available"),
            "created": care_plan.get("created", "No creation date available"),
            "activities": ", ".join([a.get("detail", {}).get("code", {}).get("coding", [{}])[0].get("display", "") for a in care_plan.get("activity", [])])
        }
    def parse_condition(condition):
        return {
            "diagnosis": condition.get("code", {}).get("coding", [{}])[0].get("display"),
            "category": ", ".join([c.get("coding", [{}])[0].get("display", "") for c in condition.get("category", [])]),
            #"Time": condition.get("recordedDate", "No time available")
            "Time": condition.get("meta", {}).get("lastUpdated", "No time available")
        }
    # Parse data
    patient_data = None
    diagnostic_reports = []
    care_plans = []
    conditions = []
    for entry in data:
        resource_type = entry.get("resourceType")
        if resource_type == "Patient":
            patient_data = parse_patient(entry)
        elif resource_type == "DiagnosticReport":
            diagnostic_reports.append(parse_diagnosticreport(entry))
        elif resource_type == "CarePlan":
            care_plans.append(parse_care_plan(entry))
        elif resource_type == "Condition":
            conditions.append(parse_condition(entry))

    if not patient_data:
        print("No patient data found in the JSON.")
        exit()

    # Generate insights with OpenAI
    # Generate insights with OpenAI
    def generate_insights_with_openai(patient, care_plans, diagnostic_reports, conditions):
        prompt = f"""
        Patient Information:
        Name: {patient['name']}
        Gender: {patient['gender']}
        Birth Date: {patient['birthDate']}
        Address: {patient['address']}

        Conditions:
        {', '.join([f"Diagnosis: {cp['diagnosis']}, Category: {cp['category']}, Time: {cp['Time']}" for cp in conditions])}

        Care Plans:
        {', '.join([f"Category: {cp['category']}, Activities: {cp['activities']}, Created: {cp['created']}" for cp in care_plans])}

        Diagnostic Reports:
        {', '.join([f"Tests: {dr['tests']}, Data: {dr['data']}, Time: {dr['Time']}" for dr in diagnostic_reports])}

        Generate detailed health insights and observations for this patient.
        Ps:Don't say we don't know or there is lack of information or results is unknown. give result based on what we know.
        """
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="gpt-4o"
            )
            return [response.choices[0].message.content.strip()]
        except Exception as e:
            return [f"Error in generating insights: {e}"]


    # Generate summaries with OpenAI
    def generate_summaries_with_openai(insights):
        summaries = []
        for insight in insights:
            try:
                response = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"Summarize this medical insight for a layperson: {insight}"
                        }
                    ],
                    model="gpt-4o"
                )
                summaries.append(response.choices[0].message.content.strip())
            except Exception as e:
                summaries.append(f"Error in generating summary: {e}")
        return summaries


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
            parsed_data["CarePlan"].append(parse_care_plan(entry))
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




    # Generate insights and summaries
    insights = generate_insights_with_openai(patient_data, care_plans, diagnostic_reports, conditions)
    summaries = generate_summaries_with_openai(insights)


    # Save to CSV
    output_df = pd.DataFrame({"Insight": insights, "Summary": summaries})
    output_csv_path = 'enhanced_patient_insights_summaries.csv'
    output_df.to_csv(output_csv_path, index=False)

    print(f"Enhanced insights and summaries saved to {output_csv_path}")
