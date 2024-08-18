import os
import fitz  # PyMuPDF
import shutil

text = "Done by NandanReddyP : )"
text_position = (360, 20)

input_dir = '6 FinalOutput'

for course in os.listdir(input_dir):
    if course.lower().endswith('.pdf'):
        pdf_link = os.path.join(input_dir, course)
        document = fitz.open(pdf_link)
        first_page = document[0]
        first_page.insert_text(text_position, text, fontsize=18, fontname="helv", color=(0.16, 0.38, 0.12))
        document.save('temp.pdf', incremental=False)  # Save to a temporary file
        document.close()
        os.remove(pdf_link)
        shutil.move('temp.pdf', pdf_link)
