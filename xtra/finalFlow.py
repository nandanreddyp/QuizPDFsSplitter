import fitz
from PyPDF2 import PdfReader, PdfWriter
import csv # MLP, JAVA, TDS, BA, PDSA

def ConvertNSaveAnswers(file):
    def color(num):
        return 'Green' if num==32512 else 'Red' if num==16711680 else 'Other'
    doc = fitz.open(file)
    answer = open('./AnswerCSVs/key.txt','w',newline='')
    write = csv.writer(answer)
    #writing question paper id in key
    text=doc[0].get_text().strip().split('\n')
    for x in text: 
        if 'IIT M' in x and 'QP' in x:
            write.writerow([x[x.index('QP'):].split()[0]])
            break
    #questions data saving
    def add(Question_id,Question_marks,Question_type,COptions,WOptions):
        if Question_id==None: return 
        if Question_type in ['MSQ','MCQ']:
            write.writerow([Question_id,Question_marks,Question_type,'$'.join(COptions),'$'.join(WOptions)])
        elif Question_type in ['SA']:
            write.writerow([Question_id,Question_marks,Question_type,':'.join(COptions[0].split(' to ')),'$'.join(WOptions)])
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
                            if Question_id!=None: 
                                add(Question_id,Question_marks,Question_type,COptions,WOptions)
                            Question_id=None;Question_marks=None;Question_type=None;COptions=[];WOptions=[]
                            write.writerow([s['text']])
                        elif ('Question Id' in s['text'] and 'COMPREHENSION' not in s['text']):
                            print('hi')
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
    doc.save("Jan2024_modified.pdf")
    doc.close()
    print(f'Total no of questions:{Qcount}')
    return "Jan2024_modified.pdf"

def AddAnswersEnd(split_pdf):
    split_pdf = open(split_pdf, 'rb')
    split_pdf = ConvertNSaveAnswers(split_pdf)  # Assuming this works correctly

    lines = []
    with open('./AnswerCSVs/key.txt', "r") as file:
        reader = csv.reader(file)
        subject_name = next(reader)[0]
        lines.append(f"Subject: {subject_name}")
        lines.append("-"*50)
        for row in reader:
            try:
                if row[1] == 0: continue
                question_number = row[0]
                question_type = row[2]
                correct_answers = ", ".join(row[-2].split('$'))
                if question_type in ["MCQ", "MSQ"]:
                    line = f"Q {question_number} [{question_type}]: Correct: {correct_answers}"
                else:  # For SA (Short Answer) questions
                    line = f"Q {question_number} [{question_type}]: Answer: {correct_answers}"
                lines.append(line)
            except:
                pass
    paragraph = "\n".join(lines)

    doc = fitz.open(split_pdf)
    page = doc._newPage()
    text_position = (50, 100)
    page.insert_text(text_position, paragraph, fontsize=12)
    doc.save("output.pdf")
    doc.close()

    # csv_file = './AnswerCSVs/key.txt'
    # with open(csv_file, 'r') as f:
    #     text_lines = f.readlines()

