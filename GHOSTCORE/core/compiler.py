from modules.exporter_pdf import PDFExporter
from modules.exporter_docx import DOCXExporter
from modules.uploader import Uploader
import os

class Compiler:
    def __init__(self):
        self.pdf = PDFExporter()
        self.docx = DOCXExporter()
        self.up = Uploader()

    def compile(self, case):
        outputs = []

        if case.get("outputs", {}).get("pdf"):
            pdf_path = self.pdf.build(case)
            outputs.append(pdf_path)

        if case.get("outputs", {}).get("docx"):
            docx_path = self.docx.build(case)
            outputs.append(docx_path)

        # ZIP packaging
        zip_path = "build/case_package.zip"
        self.up.pack(outputs, zip_path)

        return zip_path
