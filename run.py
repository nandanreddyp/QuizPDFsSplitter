from functions import split_pdf_by_heading
import os

for file in os.listdir('QuizPDFfiles'):
    if file.lower().endswith('.pdf'):
        file = os.path.join('QuizPDFfiles',file)
        split_pdf_by_heading(file)