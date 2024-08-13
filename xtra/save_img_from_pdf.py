import fitz  # PyMuPDF
import io
from PIL import Image

# Open the PDF
pdf_document = "QuizPDFfiles/Jan2024.pdf"
doc = fitz.open(pdf_document)

## Loop over each page
# for page_num in range(len(doc)):
page = doc[0]
text_instances = page.get_text("dict"); i=0
for block in text_instances["blocks"]:
    if block['type'] == 1:
        i+=1
        print(block.keys())
        image = Image.open(io.BytesIO(block['image']))
        image.save(f"img{i}.png")
        break
    # if 'lines' in block.keys():
    #     for line in block["lines"]:
    #         for span in line["spans"]:
    #             print(span.keys())
    #             print(span['text'],'color: ',span['color'])

# Close the document
doc.close()


# green color code is 32768
#   red color code is 16711680
