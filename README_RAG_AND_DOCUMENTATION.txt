Project Overview
This project involves searching through 27 PDFs to extract information efficiently. The code is implemented in Python, leveraging libraries designed for handling PDF documents and natural language processing.

Setup Instructions
Prerequisites
Ensure you have Python 3.8 or higher installed. No additional installations are assumed to be present on the system.

Step-by-Step Setup
1. Clone the Repository (if applicable):

git clone <repository-url>
cd <repository-directory>

2. Install Required Libraries:
Install the dependencies listed below. Run the following commands in the terminal or command prompt:

pip install PyPDF2
pip install pandas
pip install nltk
pip install scikit-learn

3. Set Up NLTK:
The project uses Natural Language Toolkit (NLTK) for text processing. Download the required NLTK resources:

import nltk
nltk.download('punkt')
nltk.download('stopwords')

4. Prepare Input Data:
Place all 27 PDF files in a directory named pdfs within the project folder. The code assumes the following directory structure:

/project-directory
  |-- main_script.py
  |-- pdfs/
      |-- file1.pdf
      |-- file2.pdf
      |-- ...

5. Run the Code:
Execute the main script to start the search functionality:

python main_script.py

Assumptions
	All input files are in PDF format and placed in the pdfs directory.
	The PDFs are text-based (not scanned images). OCR functionality is not implemented 	in this project.
Additional Notes
	Ensure your Python environment has write permissions for saving output or 	intermediate files.
	Customize the script as necessary to fit your specific project needs.
GitHub Push Instructions
1. Navigate to the Project Directory:
	cd <project-directory>
2. Initialize Git:
	git init
	git remote add origin <repository-url>

3. Stage and Commit Files: 

	git add .
	git commit -m "Initial commit"
4. Push to GitHub:

	git branch -M main
	git push -u origin main


