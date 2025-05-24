from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    extracted_text = []
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted_text.append(page.extract_text() or "")
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

    # Normalize line breaks and remove empty lines
    return "\n".join(line.strip() for line in extracted_text if line.strip())