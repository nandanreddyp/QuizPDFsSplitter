from functions import split_pdf_by_heading, Convert2QuestionPDF
import os

print("Om gum ganapataye namaha!")

to_create = [
    "1 PTQs",
    "2 QuestionPTQs",
    "3 SplittedPTQs",
    "4 SelectCourses",
    "5 CombinedCourses",
    "6 FinalOutput"
]

# Create directories if they don't exist
for directory in to_create:
    os.makedirs(directory, exist_ok=True)

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

# combine splitted files

print("~ Splitted! ~")