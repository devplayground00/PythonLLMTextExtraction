# Gemini API Version
import time
import glob
import google.generativeai as genai
import json
import os
import re
import asyncio
from openpyxl import Workbook
from openpyxl.styles import numbers
from typing import Dict, List
from Helper.PdfHelper import extract_text_from_pdf
from Helper.DatabaseHelper import DatabeHelper

async def main():
    profile: Dict[str, str] = await DatabeHelper.get_profile()

    working_folder = profile.get("WorkingFolder", "")
    history_folder = profile.get("HistoryFolder", "")
    fault_folder = profile.get("FaultFolder", "")
    email = profile.get("UserId", "")
    password = profile.get("Password", "")
    host = profile.get("Host", "")

    # Configure Gemini API
    genai.configure(api_key=password)  # gemini-2.0-flash gemma-3-4b-it
    model = genai.GenerativeModel("gemma-3-4b-it")

    # Start timer
    start = time.time()

    # PDF text extraction
    pdf_files = glob.glob(os.path.join(working_folder, "*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {working_folder}")

    # Use the first PDF in the folder
    path = pdf_files[0]

    pdf_text = extract_text_from_pdf(path)

    #Entity prompt
    entity = (
        "Company Name, Department, Job Title, Account Number, Employee ID, Employee Name, IC Number, Basic Salary, "
        "Travelling Allowance, EPF (EE), SOCSO (EE), EIS (EE), EPF (ER), SOCSO (ER), EIS (ER), Overtime, "
        "Total Earnings, Net Salary"
    )

    prompt = f"""
    Extract the following {entity} from the provided {pdf_text}. Return the result as a flat JSON structure under the key "extracted_data". 
    
    Each entity must include:
        - `value`: the extracted data
        - `type`: the data type (`string`, `number`, `currency`, `date`, etc.)
    
    ### Requirements:
        - Flatten the hierarchy of fields.
        - Currency values must retain their original currency symbol or code (e.g., "RM", "USD") in the `value`. For example:
            - `"Basic Salary": {{"value": "SGD 2,600.00", "type": "currency"}}`.
            - `"Net Salary": {{"value": "USD 1,200.50", "type": "currency"}}`
            - DO NOT return just numbers. You must preserve the **currency symbol** in the `value` field.
        - Normalize all numbers and dates.
        - Accurately extract quantities with units and preserve language context if multilingual.
        - Match each entity precisely as written in the entity list below.
    
    ### JSON output :
    {{
      "extracted_data": {{
        "Date": {{"value": "[extracted value]", "type": "[data type]"}},
        "Company Name": {{"value": "[extracted value]", "type": "[data type]"}},
        "Department": {{"value": "[extracted value]", "type": "[data type]"}},
        "Job Title": {{"value": "[extracted value]", "type": "[data type]"}},
        "Account Number": {{"value": "[extracted value]", "type": "[data type]"}},
        "Employee ID": {{"value": "[extracted value]", "type": "[data type]"}},
        "Employee Name": {{"value": "[extracted value]", "type": "[data type]"}},
        "IC Number": {{"value": "[extracted value]", "type": "[data type]"}},
        "Basic Salary": {{"value": "[extracted value]", "type": "[data type]"}},
        "Travelling Allowance": {{"value": "[extracted value]", "type": "[data type]"}},
        "EPF (EE)": {{"value": "[extracted value]", "type": "[data type]"}},
        "SOCSO (EE)": {{"value": "[extracted value]", "type": "[data type]"}},
        "EIS (EE)": {{"value": "[extracted value]", "type": "[data type]"}},
        "EPF (ER)": {{"value": "[extracted value]", "type": "[data type]"}},
        "SOCSO (ER)": {{"value": "[extracted value]", "type": "[data type]"}},
        "EIS (ER)": {{"value": "[extracted value]", "type": "[data type]"}},
        "Overtime": {{"value": "[extracted value]", "type": "[data type]"}},
        "Total Earnings": {{"value": "[extracted value]", "type": "[data type]"}},
        "Net Salary": {{"value": "[extracted value]", "type": "[data type]"}}
      }}
    }}
    
    """

    # Call Gemini API
    response = model.generate_content(prompt)

    # Show result
    elapsed_time = time.time() - start
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    print(response.text)
    print(f"Processed took: {minutes} minutes and {seconds:.2f} seconds")

    # Parse the Gemini response (extract valid JSON only)
    match = re.search(r'{\s*"extracted_data".*}', response.text, re.DOTALL)
    if match:
        cleaned_json_str = match.group(0)
        gemini_json = json.loads(cleaned_json_str)
    else:
        raise ValueError("No valid JSON found in Gemini response.")


    # Prepare data
    data = gemini_json["extracted_data"]
    headers = list(data.keys())
    row = [str(data[key].get("value", "")) for key in headers]

    # Create workbook
    wb = Workbook()
    ws = wb.active

    # Write headers
    ws.append(headers)

    # Write row with all cells as text format
    for col_index, value in enumerate(row, start=1):
        cell = ws.cell(row=2, column=col_index, value=value)
        cell.number_format = numbers.FORMAT_TEXT  # Forces Excel to treat it as plain text

    # Save Excel file
    original_filename_no_ext = os.path.splitext(os.path.basename(path))[0]  # "Payslip202405"
    output_excel = os.path.join(os.path.dirname(path), f"{original_filename_no_ext}.xlsx")
    wb.save(output_excel)

    print(f"Excel saved to: {output_excel}")


if __name__ == "__main__":
    asyncio.run(main())
