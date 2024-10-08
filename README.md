# QuizPDFsSplitter

## Create requirements

1. **Run the Python script to create folders**
   ```
   python run.py
   ```

2. **Create a Virtual Environment and Activate It**
   ```bash
   python -m venv venv
   venv/scripts/activate
   ```

## Download Quiz PDFs and prepare input

1. **Download the Quiz Key PDFs**  
   Download the Quiz key PDFs from the following link: [Quiz Key PDFs](https://docs.google.com/spreadsheets/d/1ceOGXoHpqpq2yB_v5qwcWftOXEVeO1XqkkDo_Vn5CHA/edit?usp=sharing).

2. **Rename the Quiz PDF File**  
   Rename each downloaded Quiz PDF file using the format:  
   `"Year_Term_Quiz_Session"`  
   - Example: `2023_T3_Q1`, `2021_T1_Q2`, `2024_T2_Et_Fn`, `2022_T3_Et_An`

   **Format Breakdown:**
   - `Year`: Which year quiz (e.g., 2022, 2023)
   - `Term`: Term id (e.g., T1, T2, T3)
   - `Quiz`: Quiz id (e.g., Q1, Q2, Et)
   - `Session`: Session id (An for Afternoon, Fn for Forenoon; required only for Et Quiz)

3. **Save the Renamed Files**  
   Save the renamed files in the `1 PTQs` folder.

## Run Python Script to split files

1. **Run the Python script**
   ```bash
   python split.py
   ```
   Subject wise splits will be in `3 SplittedPTQs` folder.

## Select Course Splits to Combine

1. **Handling Multiple Folders for the Same Course in `2 Question PTQs`**  
   - If a course has different folder names inside the `3 SplittedPTQs` directory under `Answers` or `Questions`, do the following:
     - Create a single, consistently named folder for that course.
     - Move all files related to that course into the newly created folder within both the `Answers` and `Questions` directories.

2. **Arrange Course Splits for Combining**  
   - In the `4 SelectCourses` folder, create folders with your selected courses names.
   - Inside each course folders you have created create `Answers` and `Questions` folders.
   - Place the respective Answer PDFs and Question PDFs into their corresponding course folders from `3 SplittedPTQs`.

## Run Python Script to combine splits

1. **Run the Python script**  
   ```bash
   python combine.py
   ```
