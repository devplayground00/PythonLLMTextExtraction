import time
import glob
import google.generativeai as genai
import json
import os
import re
import asyncio
from Prompt.Payslip import get_payslip_prompt
from Helper.PdfHelper import extract_text_from_pdf
from Helper.DatabaseHelper import DatabaseHelper
from Helper.ExcelHelper import save_data_excel

async def main():
    # Start timer
    start = time.time()

    #get profile detail
    profile: Dict[str, str] = await DatabaseHelper.get_profile()
    working_folder = profile.get("WorkingFolder", "")
    history_folder = profile.get("HistoryFolder", "")
    fault_folder = profile.get("FaultFolder", "")
    email = profile.get("UserId", "")
    password = profile.get("Password", "")
    host = profile.get("Host", "")

    # Configure Gemini API
    genai.configure(api_key=password)  # gemini-2.0-flash gemma-3-4b-it
    model = genai.GenerativeModel("gemma-3-4b-it")

    # PDF text extraction
    pdf_files = glob.glob(os.path.join(working_folder, "*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {working_folder}")

    # Use the first PDF in the folder
    path = pdf_files[0]
    pdf_text = extract_text_from_pdf(path)

    #get return prompt
    prompt = get_payslip_prompt(pdf_text)

    # Call Gemini API
    response = model.generate_content(prompt)

    # Parse the Gemini response (extract valid JSON only)
    match = re.search(r'{\s*"extracted_data".*}', response.text, re.DOTALL)
    if match:
        cleaned_json_str = match.group(0)
        gemini_json = json.loads(cleaned_json_str)
    else:
        raise ValueError("No valid JSON found in Gemini response.")

    # Prepare data
    data = gemini_json["extracted_data"]
    output_excel = save_data_excel(data,path)

    # Show result
    elapsed_time = time.time() - start
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    print(response.text)
    print(f"Excel saved to: {output_excel}")
    print(f"Processed took: {minutes} minutes and {seconds:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
