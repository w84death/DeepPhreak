import PyPDF2
from docx import Document
import pandas as pd
import csv
import os

class FileProcessor:
    @staticmethod
    def process_file(filepath):
        ext = os.path.splitext(filepath)[1].lower()
        
        try:
            if ext == '.pdf':
                return FileProcessor._read_pdf(filepath)
            elif ext == '.txt':
                return FileProcessor._read_txt(filepath)
            elif ext == '.docx':
                return FileProcessor._read_docx(filepath)
            elif ext in ['.xlsx', '.xls']:
                return FileProcessor._read_excel(filepath)
            elif ext == '.csv':
                return FileProcessor._read_csv(filepath)
            else:
                return "Unsupported file format"
        except Exception as e:
            return f"Error processing file: {str(e)}"

    @staticmethod
    def _read_pdf(filepath):
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text

    @staticmethod
    def _read_txt(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _read_docx(filepath):
        doc = Document(filepath)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    @staticmethod
    def _read_excel(filepath):
        df = pd.read_excel(filepath)
        return df.to_string()

    @staticmethod
    def _read_csv(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return "\n".join([",".join(row) for row in reader])
