import sys
import pyperclip
from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def chapter_title(self, level, title):
        if level == 1:
            self.set_font('Arial', 'B', 16)
        elif level == 2:
            self.set_font('Arial', 'B', 14)
        elif level == 3:
            self.set_font('Arial', 'B', 12)
        elif level == 4:
            self.set_font('Arial', 'B', 10)
        elif level == 5:
            self.set_font('Arial', 'B', 8)
        elif level == 6:
            self.set_font('Arial', 'B', 6)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_list_item(self, item):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'• {item}', 0, 1, 'L')

    def add_numbered_item(self, item, number):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'{number}. {item}', 0, 1, 'L')

def parse_markdown(md_text):
    lines = md_text.split('\n')
    parsed_lines = []

    for line in lines:
        if line.startswith('# '):
            parsed_lines.append(('heading1', line[2:]))
        elif line.startswith('## '):
            parsed_lines.append(('heading2', line[3:]))
        elif line.startswith('### '):
            parsed_lines.append(('heading3', line[4:]))
        elif line.startswith('#### '):
            parsed_lines.append(('heading4', line[5:]))
        elif line.startswith('##### '):
            parsed_lines.append(('heading5', line[6:]))
        elif line.startswith('###### '):
            parsed_lines.append(('heading6', line[7:]))
        elif line.startswith('* '):
            parsed_lines.append(('list_item', line[2:]))
        elif re.match(r'\d+\.\s', line):
            parsed_lines.append(('numbered_item', re.sub(r'\d+\.\s', '', line)))
        else:
            parsed_lines.append(('paragraph', line))
    
    return parsed_lines

def add_to_pdf(pdf, parsed_lines):
    number = 1
    for line_type, content in parsed_lines:
        if line_type == 'heading1':
            pdf.chapter_title(1, content)
        elif line_type == 'heading2':
            pdf.chapter_title(2, content)
        elif line_type == 'heading3':
            pdf.chapter_title(3, content)
        elif line_type == 'heading4':
            pdf.chapter_title(4, content)
        elif line_type == 'heading5':
            pdf.chapter_title(5, content)
        elif line_type == 'heading6':
            pdf.chapter_title(6, content)
        elif line_type == 'list_item':
            pdf.add_list_item(content)
        elif line_type == 'numbered_item':
            pdf.add_numbered_item(content, number)
            number += 1
        else:
            pdf.chapter_body(content)

def main():
    if len(sys.argv) != 2:
        print("Usage: mdtodoc <output_pdf_name>")
        sys.exit(1)

    output_pdf_name = sys.argv[1] + '.pdf'

    # Get the current string from the clipboard
    md_text = pyperclip.paste()

    # Parse the markdown text
    parsed_lines = parse_markdown(md_text)

    # Create a new PDF document
    pdf = PDF()
    pdf.add_page()

    # Add parsed content to the PDF
    add_to_pdf(pdf, parsed_lines)

    # Save the PDF
    pdf.output(output_pdf_name)
    print(f"PDF saved as {output_pdf_name}")

if __name__ == "__main__":
    main()