import fitz
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import os, re


def Convert2QuestionPDF(filename):
    file = os.path.join('1 PTQs',filename)
    def color(num):
        if num in [32768, 32512, ]:
            return 'Green'
        elif num in [16711680, ]:
            return 'Red'
        else:
            return 'Other'
    doc = fitz.open(file)
    Question_type=None
    for i in range(len(doc)):
        page = doc[i]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 1: # image block
                if b['width'] == b['height'] == 16: # tick or cross image
                        rect = fitz.Rect(b['bbox'])
                        page.add_redact_annot(rect, fill=(1, 1, 1)) # Add a redaction annotation to cover the image
                        page.apply_redactions()
            elif b['type'] == 0:
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        # print(s['text'])
                        if s['size'] >= 18: # reset question type
                            Question_type=None
                        elif ('Question Type' in s['text'] and 'COMPREHENSION' not in s['text']):
                            match = re.search(r'Question Type\s*:\s*(\w+)', s['text'])
                            Question_type=match.group(1)
                        elif color(s['color']) in ['Green','Red']:
                            if Question_type!='SA': # not write SA answers in black
                                text = s['text']
                                rect = fitz.Rect(s['bbox'])
                                point = rect.tl
                                point = fitz.Point(point.x, point.y+15)
                                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                                page.insert_text(point, text, fontsize=s['size'], fontname='helv', color=(0.39,0.36,0))
                            elif Question_type=='SA' and color(s['color'])=='Green':
                                Question_type=None
                                # hide answer
                                rect = fitz.Rect(b['bbox'])
                                new_rect = fitz.Rect(rect.x0-3, rect.y0-3, rect.x0 + 100, rect.y0 + 30)
                                page.add_redact_annot(rect, fill=(1, 1, 1)) # Add a redaction annotation to cover the text
                                page.draw_rect(new_rect, color=(0.39,0.36,0), width=1)
                                page.apply_redactions()
                        if (i== len(doc)-1 and blocks.index(b)==len(blocks)-1):
                            Question_type=None
    page.apply_redactions()
    doc.save(os.path.join('2 QuestionPTQs',filename))
    doc.close()
    print(f'Questions convered!')


def split_pdf_by_heading(pdf_link, type):
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
                        if span['size'] >= 18 and all(word not in span['text'] for word in ['Technology', 'Education', 'Group']):
                            split_points.append((page_num, span['text']))
                            current_split_start = page_num
                            # break
    split_points.append((len(document),None))
    # print(term_info,split_points)
    reader = PdfReader(pdf_link)
    for i in range(len(split_points) - 1):
        start_page, heading = split_points[i]
        end_page, _ = split_points[i + 1]

        writer = PdfWriter()
        for page_num in range(start_page, end_page+1):
            if page_num != len(document):
                writer.add_page(reader.pages[page_num])
        # Save the split PDF
        if type=='Questions':
            heading_dir = os.path.join('3 SplittedPTQs','Questions', heading)
        elif type=='Answers':
            heading_dir = os.path.join('3 SplittedPTQs','Answers', heading)
        else: raise KeyError
        os.makedirs(heading_dir, exist_ok=True)
        output_pdf_path = os.path.join(heading_dir, f"{term_info}.pdf")
        with open(output_pdf_path, "wb") as output_pdf_file:
            writer.write(output_pdf_file)
    print(f"Saved splited pdfs from {term_info}")


def add_term_info():
    for course in os.listdir('4 SelectCourses'):
        course_path = os.path.join('4 SelectCourses', course)
        pdfs = [os.path.join(course_path, 'Questions', pdf) for pdf in os.listdir(os.path.join(course_path, 'Questions')) if pdf.endswith('.pdf')]
        pdfs.extend([os.path.join(course_path, 'Answers', pdf) for pdf in os.listdir(os.path.join(course_path, 'Answers')) if pdf.endswith('.pdf')])
        for pdf in pdfs:
            doc = fitz.open(pdf)
            last_page = doc[0] # Insert at begining
            text = os.path.basename(pdf).split('.')[0]
            last_page.insert_text(
                fitz.Point(10, 20),  # Position the text near the bottom
                text,
                fontsize=18,
                fontname="helv",
                color=(1, 0, 1),
                rotate=0
            )
            doc.save('temp.pdf')
            doc.close()
            os.replace('temp.pdf', pdf)


def combine_pdfs(pdf_files, output_path):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    pdf_writer = PyPDF2.PdfWriter()
    for pdf_file in pdf_files:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    print(f'Combined PDF saved as {output_path}')

