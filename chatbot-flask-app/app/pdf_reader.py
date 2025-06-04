from PyPDF2 import PdfReader

def read_pdf(file_path, start_page=0, end_page=None):
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            # Adjust for 0-based indexing: page 13 is index 12, page 27 is index 26
            start = start_page - 1 if start_page else 0
            end = end_page if end_page else len(reader.pages)
            for page in reader.pages[start:end]:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text.strip()

# Extract pages 13 to 27 (inclusive)
file_path = "../../SRB’s Manual of Surgery.pdf"
pdf_text = read_pdf(file_path, start_page=13, end_page=27)

# Write the extracted text to a .txt file
output_txt_path = "../../SRB’s Manual of Surgery.txt"
with open(output_txt_path, "w", encoding="utf-8") as txt_file:
    txt_file.write(pdf_text)

print(f"PDF text (pages 13-27) extracted and saved to {output_txt_path}")