import os, fitz, re

file = os.path.join('1 PTQs','2021_T3_Et_An.pdf')
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
                    if s['size']==18 and s['text'][:5]!='Group':
                        # add file name on top right corner in bold brown
                        text = "2021_T3_Et_An"
                        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                        page.insert_text(fitz.Point(20,20), text, fontsize=17, fontname='helv', color=(0.6, 0.3, 0))
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
doc.save('test.pdf')
doc.close()
print(f'Questions convered!')