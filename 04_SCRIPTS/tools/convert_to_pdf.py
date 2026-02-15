
import sys
import markdown2
from weasyprint import HTML

def convert_md_to_pdf(md_file, pdf_file):
    """
    Converts a Markdown file to a PDF file.
    """
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html_content = markdown2.markdown(md_content)

        html = HTML(string=html_content)
        html.write_pdf(pdf_file)

        print(f"Successfully converted '{md_file}' to '{pdf_file}'")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_pdf.py <input.md> <output.pdf>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_md_to_pdf(input_file, output_file)
