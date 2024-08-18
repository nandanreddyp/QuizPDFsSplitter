# from functions import Convert2QuestionPDF
# Convert2QuestionPDF('2021.pdf')

# import fitz  # PyMuPDF

# # Open the PDF
# pdf_document = "1 PTQs/2021.pdf"
# doc = fitz.open(pdf_document)

# ## Loop over each page
# # for page_num in range(len(doc)):
# # for page_num in range(6):
# page = doc[24]
# text_instances = page.get_text("dict")
# for block in text_instances["blocks"]:
#     if block['type'] == 0:
#         for line in block["lines"]:
#             for span in line["spans"]:
#                 print(span['text'],span['color'])
#                 # if span['color'] in [32512, 16711680]:
#                 #     print(span['text'],'color: ',span['color'])
#                 #     text = span['text']
#                 #     rect = fitz.Rect(span['bbox'])

#                 #     # Add a white rectangle to cover the original text
#                 #     page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                    
#                 #     # Add new text with the desired color at the exact position
#                 #     page.insert_text(rect.tl, text, fontsize=span['size'], fontname='helv', color=(0,0,0))

# page.apply_redactions()
# # Close the document
# doc.save("Jan2024_modified.pdf")
# doc.close()

