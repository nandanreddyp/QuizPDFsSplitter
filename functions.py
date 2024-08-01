import fitz
from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf_by_heading(pdf_link):
    document = fitz.open(pdf_link)
    term_info = os.path.basename(pdf_link).split('.')[0]
    split_points = []; current_split_start = 0
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] == 0: # text block
                for line in block['lines']:
                    for span in line['spans']:
                        # print(span['text'],span['size'])
                        if span['size'] >= 18:
                            split_points.append((page_num, span['text']))
                            current_split_start = page_num
                            break
    split_points.append((len(document),None)); split_points=split_points[1:]
    # print('Page numbers, Course name: ',split_points)

    reader = PdfReader(pdf_link)
    for i in range(len(split_points) - 1):
        start_page, heading = split_points[i]
        end_page, _ = split_points[i + 1]

        writer = PdfWriter()
        for page_num in range(start_page, end_page+1):
            if page_num != len(document):
                writer.add_page(reader.pages[page_num])
        # Save the split PDF
        heading_dir = os.path.join('SplittedPDFfiles', heading)
        os.makedirs(heading_dir, exist_ok=True)
        output_pdf_path = os.path.join(heading_dir, f"{term_info}.pdf")
        with open(output_pdf_path, "wb") as output_pdf_file:
            writer.write(output_pdf_file)
        
    print(f"Saved splited pdfs from {term_info}")


