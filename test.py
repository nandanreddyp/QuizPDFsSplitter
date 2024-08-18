import fitz  # PyMuPDF

# Open the PDF
pdf_document = "1 PTQs/2021_T3_Et_An.pdf"
doc = fitz.open(pdf_document)

## Loop over each page
# for page_num in range(len(doc)):
# for page_num in range(6):
page = doc[0]
text_instances = page.get_text("dict")
for block in text_instances["blocks"]:
    if block['type'] == 0:
        for line in block["lines"]:
            for span in line["spans"]:
                if span['size'] >= 18:
                    print('hi',span['text'])
                # if span['color'] in [32512, 16711680]:
                #     print(span['text'],'color: ',span['color'])
                #     text = span['text']
                #     rect = fitz.Rect(span['bbox'])

                #     # Add a white rectangle to cover the original text
                #     page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                    
                #     # Add new text with the desired color at the exact position
                #     page.insert_text(rect.tl, text, fontsize=span['size'], fontname='helv', color=(0,0,0))

# page.apply_redactions()
# # Close the document
# doc.save("Jan2024_modified.pdf")
doc.close()


# if type of block is 1 then its image, if block width and height is 16 then its ticks
# green color code is 32512
#   red color code is 16711680

# Types of Question Types
# COMPREHENSION neglect
# MSQ, MCQ, SA, 

# Types of Answers under Question Type: SA
# Equal, Range, Set