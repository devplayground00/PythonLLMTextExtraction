from html.entities import entitydefs


def get_payslip_prompt(pdf_text: str) -> str:
    # Entity prompt
    entity = (
        "Company Name, Department, Job Title, Account Number, Employee ID, Employee Name, IC Number, Basic Salary, "
        "Travelling Allowance, EPF (EE), SOCSO (EE), EIS (EE), EPF (ER), SOCSO (ER), EIS (ER), Overtime, "
        "Total Earnings, Net Salary"
    )

    return f"""
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

