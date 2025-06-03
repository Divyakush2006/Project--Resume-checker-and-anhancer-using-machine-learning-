# Resume & Job Description Matcher and Enhancer using Machine Learning

## Overview

This project is a web-based application designed to assist job seekers in tailoring their resumes to specific job descriptions. It leverages Natural Language Processing (NLP) and keyword matching to analyze your resume against a target job description, providing insights into skill alignment, resume completeness, and recruiter readiness.

The application allows users to upload their resume and a job description (both in PDF format), processes them, and then presents a detailed analysis, including:
* Skill comparison (matched, missing, and extra skills)
* Overall compatibility scores
* Actionable feedback and recommendations to improve your resume's relevance.

## Features

* **PDF Upload:** Easily upload your resume and the job description as PDF files via a user-friendly interface.
* **Skill Extraction & Comparison:** Automatically extracts skills from both documents and categorizes them into:
    * **Matched Skills:** Skills present in both your resume and the JD.
    * **Missing Skills:** Skills required by the JD but not found in your resume.
    * **Extra Skills:** Skills present in your resume but not explicitly mentioned in the JD.
* **Performance Scores:** Generates three key scores to gauge your resume's effectiveness:
    * **Overall Skill Match Score:** Percentage of job description skills found in your resume.
    * **Recruiter Readiness Score:** Assesses how well your resume is optimized for quick review by recruiters.
    * **Resume Completeness Score:** Indicates if essential sections (skills, education, organizations) were successfully extracted.
* **Actionable Feedback:** Provides personalized suggestions based on the analysis to help you enhance your resume for a better match.
* **Extracted Information:** Displays key information parsed from your resume, such as education details and organizations, for your review.
* **Salary Guidance:** Includes a disclaimer and recommendations for researching salary expectations using external resources, as direct salary estimation from resumes is unreliable.

## Technologies Used

The project is built using a combination of frontend and backend technologies:

### Frontend
* **HTML5:** For structuring the web content.
* **Tailwind CSS:** For rapid and responsive UI development.
* **JavaScript:** For dynamic client-side interactions and handling file uploads and results display.

### Backend
* **Python:** The core language for backend logic and NLP processing.
* **Flask:** A micro web framework for Python, used to handle HTTP requests and serve the analysis results.
* **Flask-CORS:** Enables Cross-Origin Resource Sharing for seamless communication between the frontend and backend.
* **pdfplumber:** A Python library for extracting text and data from PDF files.
* **spaCy:** An industrial-strength natural language processing library, used for Named Entity Recognition (NER) to extract organizations.
* **re (Regex):** Python's built-in regular expression module for pattern matching and keyword extraction.
* **werkzeug.utils.secure_filename:** For securely handling uploaded filenames.
* **tempfile & shutil:** For managing temporary file storage and cleanup of uploaded PDFs.

## Setup and Installation

Follow these steps to set up and run the project locally:

### Prerequisites

* Python 3.8+
 `pip` (Python package installer)
* Git

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone [https://github.com/Divyakush2006/Project--Resume-checker-and-anhancer-using-machine-learning-](https://github.com/Divyakush2006/Project--Resume-checker-and-anhancer-using-machine-learning-)
cd Project--Resume-checker-and-anhancer-using-learning-
```
### 2. Virtual Environment Creation and Activation (Recommended Practice)
The establishment and activation of a virtual environment are strongly recommended for efficient dependency management:

```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```
### 3. Dependency Installation
Proceed with the installation of the requisite Python packages. It is advisable to utilize a `requirements.txt` file if available within the repository (which can be generated via `pip freeze > requirements.txt`).

```bash
pip install -r requirements.txt
# Alternatively, individual installations can be performed if a requirements.txt file is absent:
# pip install Flask Flask-CORS pdfplumber spacy
```

### 4. spaCy Model Download
This project necessitates the download of a compact English language model for spaCy to facilitate its NLP functionalities:

```bash
python -m spacy download en_core_web_sm
```

### 5. Flask Backend Execution
Navigate to the root directory of the project (the location of `app.py`) and initiate the Flask application:

```bash
python app.py
```
The Flask application is typically accessible at `http://127.0.0.1:5000/`. Confirmation of its operational status will be indicated by console output similar to `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`.


### 6. Frontend Access
Access the frontend interface by opening the `index.html` file directly within a web browser. This file encapsulates the entirety of the user interface.

* **Crucial Note:** It is imperative to ensure that the Flask backend is actively running (python app.py) prior to accessing index.html, as the frontend initiates API requests to http://127.0.0.1:5000/analyze.


## Usage Protocol

* **Backend Initialization:** Initially, verify the operational status of the Flask application by executing python app.py in the terminal.

* **Frontend Access:** Access the index.html file within your preferred web browser.

* **Document Upload:**

   * Initiate the resume upload process by clicking the designated "Upload Your Resume (PDF)" area or by dragging and dropping the resume PDF file into this zone.

   * Similarly, for the job description, click the "Upload Job Description (PDF)" area or drag and dropping the job description PDF file into its respective zone.

* **Analysis Commencement:** Activate the analytical process by selecting the "Analyze My Resume" button.

* **Report Review:** A comprehensive analysis report will subsequently be rendered on the display interface, presenting scores, skill comparisons, and personalized feedback.


## Project Structure

```bash
.
├── app.py                  # Flask backend application, responsible for handling file uploads and API endpoints.
├── resume_parser.py        # Contains the core logic for PDF parsing, skill extraction, scoring, and feedback generation.
├── index.html              # Frontend user interface, comprising HTML, CSS, and JavaScript components.
└── requirements.txt        # Delineates the Python dependencies necessary for the project's operation (to be created if not present).


```


## Contributing

Contributions to this project are highly encouraged and appreciated. Individuals possessing suggestions for enhancements, novel functionalities, or defect resolutions are invited to:

* **Fork** the repository.

* **Create a new branch** (e.g., `git checkout -b feature/DescriptiveFeatureName` or `bugfix/IssueResolution`).

* **Implement the desired modifications.**

* **Commit** the changes with a clear and concise message (e.g., `git commit -m "Add new feature"`).

* **Push** the local branch to the forked repository (`git push origin feature/DescriptiveFeatureName`).

* **Submit a Pull Request** to the `main` branch of this repository for review.


## License
This project is distributed under an open-source license and is available under the [MIT License](https://opensource.org/licenses/MIT).

### Disclaimer:
This tool offers automated analytical insights and feedback. Users are advised to critically evaluate all suggestions and exercise independent judgment when modifying their resumes. It is important to note that salary estimations are inherently complex and necessitate research utilizing credible and current industry resources.


## Check out my Linkedin:
[Linkedin Profile](https://www.linkedin.com/in/divyakush-punjabi/)
