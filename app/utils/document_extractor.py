import csv
import re
from typing import List
import openpyxl
import pdfplumber
import xlrd

class DocumentExtractor:
    def __init__(self, output_file: str = None) -> None:
        self.output_file = output_file

    def load_pdf(self, source: str, destination: str, filename: str = 'output', extension: str = '.txt'):
        # Define the path to the output text file
        output_path = f"{destination}/{filename}{extension}"

        # Open the PDF file using pdfplumber
        with pdfplumber.open(source) as pdf:
            # Open the output text file in write mode
            with open(output_path, 'w', encoding='utf-8') as txt_file:
                # Iterate through each page in the PDF
                for page in pdf.pages:
                    # Extract text from the page
                    text = page.extract_text()
                    # Write the text to the output file
                    if text:
                        txt_file.write(text)
                        txt_file.write('\n\n')  # Add a new line between pages

        print(f"Text extracted and saved to {output_path}")
        return output_path
    
    def extract_csv_content(self, source_path: str, destination_path: str) -> None:
        with open(source_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            with open(destination_path, mode='w', encoding='utf-8') as txt_file:
                for row in csv_reader:
                    txt_file.write(' '.join(row) + '\n')
                    
    def extract_excel_content(self, source_path: str, destination_path: str) -> None:
        if source_path.endswith('.xlsx'):
            workbook = openpyxl.load_workbook(source_path)
            sheet = workbook.active
        elif source_path.endswith('.xls'):
            workbook = xlrd.open_workbook(source_path)
            sheet = workbook.sheet_by_index(0)
        else:
            raise ValueError("The provided file is not an Excel file")

        with open(destination_path, mode='w', encoding='utf-8') as txt_file:
            if source_path.endswith('.xlsx'):
                for row in sheet.iter_rows(values_only=True):
                    txt_file.write(' '.join(str(cell) for cell in row) + '\n')
            elif source_path.endswith('.xls'):
                for row_idx in range(sheet.nrows):
                    row = sheet.row(row_idx)
                    txt_file.write(' '.join(str(cell.value) for cell in row) + '\n')
                    
    def extract_pdf_content(self, source_path, destination_path):
        content = ""

        # Open the PDF file using pdfplumber
        with pdfplumber.open(source_path) as pdf_document:
            # Iterate through each page
            for page in pdf_document.pages:
                content += page.extract_text()

        # Remove more than two consecutive new lines
        cleaned_content = re.sub(r'(\n\s*){3,}', '\n\n', content)

        # Write the cleaned content to the destination file
        with open(destination_path, 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_content)

    def extract_text_by_header(self, pdf_file_path: str, headers: list, destination: str):
        content = {header: "" for header in headers}

        # Open the PDF file using pdfplumber
        with pdfplumber.open(pdf_file_path) as document:
            current_header = None

            # Iterate over each page in the PDF
            for page in document.pages:
                text = page.extract_text()

                # Check for headers and update the current_header
                for header in headers:
                    if header in text:
                        current_header = header

                # If we are in a section, append the text to the current header's content
                if current_header:
                    content[current_header] += text

        # Write each header's content to a separate .txt file
        for header, text in content.items():
            # Create a valid filename from the header
            filename = re.sub(r'[\/:*?"<>|]', '', header) + '.txt'
            with open(f"{destination}/{filename}", 'w', encoding='utf-8') as file:
                file.write(text)

        print("Content has been extracted and saved to text files.")

    def extract_text_by_index(self, pdf_path, index_terms:List[str], pages_to_skip:int=0):
        full_text = []

        # Open the PDF file using pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from the PDF
            for i, page in enumerate(pdf.pages):
                full_text.append(page.extract_text())

        full_text = "\n".join(full_text)

        # Find the positions of index terms
        positions = [
            (term, match.start())
            for term in index_terms
            for match in re.finditer(rf'\b{re.escape(term)}\b', full_text, re.IGNORECASE)
        ]

        # Sort positions by their occurrence in the text
        positions.sort(key=lambda x: x[1])

        # Extract text between index terms
        extracted_sections = {}
        for i, (start_term, start_pos) in enumerate(positions):
            end_pos = positions[i + 1][1] if i + 1 < len(positions) else len(full_text)
            extracted_text = full_text[start_pos:end_pos].strip()
            extracted_sections[start_term] = extracted_text

        return extracted_sections
