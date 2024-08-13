from functions import split_pdf_by_heading, Convert2QuestionPDF
import os

print("Om gum ganapataye namaha!")

for file in os.listdir('1 PTQs'):
    if file.lower().endswith('.pdf'):
        Convert2QuestionPDF(file)

for file in os.listdir('1 PTQs'):
    if file.lower().endswith('.pdf'):
        file = os.path.join('1 PTQs',file)
        split_pdf_by_heading(file, type='Answers')

for file in os.listdir('2 QuestionPTQs'):
    if file.lower().endswith('.pdf'):
        file = os.path.join('2 QuestionPTQs',file)
        split_pdf_by_heading(file, type='Questions')

# combine sp

print("~ The End ~")