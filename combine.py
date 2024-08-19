import os, re, fitz
from functions import combine_pdfs, add_term_info

add_term_info()

for course in os.listdir('4 SelectCourses'):
    course_path = os.path.join('4 SelectCourses', course)
    if 'Answers' in os.listdir(course_path) and 'Questions' in os.listdir(course_path) and len(os.listdir(course_path)) == 2:

        # Answers
        answers_folder = os.path.join(course_path, 'Answers')
        answer_pdfs = sorted([os.path.join(answers_folder, pdf) for pdf in os.listdir(answers_folder) if pdf.endswith('.pdf')],reverse=True)
        combine_pdfs(answer_pdfs, os.path.join('5 CombinedCourses',course,'Combined_Answers.pdf'))

        # Questions
        questions_folder = os.path.join(course_path, 'Questions')
        question_pdfs = sorted([os.path.join(questions_folder, pdf) for pdf in os.listdir(questions_folder) if pdf.endswith('.pdf')],reverse=True)
        combine_pdfs(question_pdfs, os.path.join('5 CombinedCourses',course,'Combined_Questions.pdf'))

    else:
        print('Check if there are ONLY Answers and Questions folders in Course folder')


for course in os.listdir('5 CombinedCourses'):
    course_path = os.path.join('5 CombinedCourses', course)
    pdfs = sorted([os.path.join(course_path, pdf) for pdf in os.listdir(course_path) if pdf.endswith('.pdf')],reverse=True)
    first_file = pdfs[0]
    doc = fitz.open(first_file)
    last_page = doc[-1] # Insert "~ The End ~" at the end of the last page
    text = "~ The End ~"
    last_page.insert_text(
        fitz.Point(45, last_page.rect.height - 72),  # Position the text near the bottom
        text,
        fontsize=90,
        fontname="helv",
        color=(1, 0, 0),
        rotate=0
    )
    doc.save('temp.pdf')
    doc.close()
    os.replace('temp.pdf', first_file)
    combine_pdfs(pdfs, os.path.join('6 FinalOutput',f'{course}.pdf'))


print("~ Combined! ~")