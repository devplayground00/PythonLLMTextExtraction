
import os
from typing import Dict
from openpyxl import Workbook
from openpyxl.styles import numbers

def save_data_excel(data: Dict[str,Dict[str,str]],pdf_path:str) -> str:
    headers = list(data.keys())
    row = [str(data[key].get("value", "")) for key in headers]

    # Create workbook
    wb = Workbook()
    ws = wb.active

    # Write headers
    ws.append(headers)

    for column_index, value in enumerate(row, start=1):
        cell = ws.cell(row=2, column=column_index, value=value)
        cell.number_format = numbers.FORMAT_TEXT  # Forces Excel to treat it as plain text

    # Save Excel file
    original_filename_no_ext = os.path.splitext(os.path.basename(pdf_path))[0]  # "Payslip202405"
    output_excel = os.path.join(os.path.dirname(pdf_path), f"{original_filename_no_ext}.xlsx")
    wb.save(output_excel)

    return output_excel



