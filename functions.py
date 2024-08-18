import fitz
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import os, csv, re

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
                        if span['size'] >= 18 and 'Technology' not in span['text']:
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
    def add(Question_id,Question_marks,Question_type,COptions,WOptions):
        if Question_id==None:
            return None
        Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
    Qcount=0;Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
    for i in range(len(doc)):
        page = doc[i]
        blocks = page.get_text("dict")["blocks"]
        # text_instances = page.get_text("dict")
        for b in blocks:
            if b['type'] == 1: # image block
                if b['width'] == b['height'] == 16: # tick or cross image
                        rect = fitz.Rect(b['bbox'])
                        page.add_redact_annot(rect, fill=(1, 1, 1)) # Add a redaction annotation to cover the image
                        page.apply_redactions()
            elif b['type'] == 0:
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if s['size']==18 and s['text'][:5]!='Group':
                            # add file name on top right corner in bold brown
                            text = filename
                            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                            page.insert_text(fitz.Point(20,20), text, fontsize=17, fontname='helv', color=(0.6, 0.3, 0))
                            if Question_id!=None: 
                                add(Question_id,Question_marks,Question_type,COptions,WOptions)
                            Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
                        elif ('Question Id' in s['text'] and 'COMPREHENSION' not in s['text']):
                            if Question_id!=None: add(Question_id,Question_marks,Question_type,COptions,WOptions)
                            Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
                            Qcount+=1
                            row = s['text'].split(' ')
                            Question_id = row[7];Question_marks=0;Question_type=row[11];COptions=[];WOptions=[]
                        elif 'Correct Marks' in s['text']:
                            Question_marks = s['text'].split()[3]
                        elif color(s['color']) in ['Green','Red']:
                            if Question_type!='SA': # not write SA answers in black
                                text = s['text']
                                rect = fitz.Rect(s['bbox'])
                                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                                page.insert_text(rect.tl, text, fontsize=s['size'], fontname='helv', color=(0,0,0))
                            if len(s['text'])==len('6406531931004. ') and str(s['text'][:4])=='6406531931004. '[:4]:
                                if color(s['color'])=='Green':
                                    COptions.append(s['text'][:-2])
                                elif color(s['color'])=='Red':
                                    WOptions.append(s['text'][:-2])
                            elif Question_type=='SA' and color(s['color'])=='Green':
                                COptions.append(s['text'])
                                add(Question_id,Question_marks,Question_type,COptions,WOptions)
                                Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
                                # hide answer
                                rect = fitz.Rect(b['bbox'])
                                page.add_redact_annot(rect, fill=(1, 1, 1)) # Add a redaction annotation to cover the image
                                page.apply_redactions()
                        if (i== len(doc)-1 and blocks.index(b)==len(blocks)-1):
                            add(Question_id,Question_marks,Question_type,COptions,WOptions)
                            Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
    page.apply_redactions()
    doc.save(os.path.join('2 QuestionPTQs',filename))
    doc.close()
    print(f'Questions convered!')


def filter_pdfs(pdf_list):
    def extract_info(filename):
        match = re.search(r'(\d{4})_(T\d)_(Et)_(\w+)\.pdf', filename)
        if match:
            year, term, quiz, session = match.groups()
            return year, term, quiz, session
        return None
    file_dict = {}
    for pdf in pdf_list:
        info = extract_info(pdf)
        if info:
            year, term, quiz, session = info
            key = (year, term, quiz)
            if key in file_dict:
                del file_dict[key] # If a file with the same year, term, quiz but different session exists, remove it
            file_dict[key] = pdf
    return list(file_dict.values())


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