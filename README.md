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
* `pip` (Python package installer)
* Git

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone [https://github.com/Divyakush2006/Project--Resume-checker-and-anhancer-using-machine-learning-](https://github.com/Divyakush2006/Project--Resume-checker-and-anhancer-using-machine-learning-)
cd Project--Resume-checker-and-anhancer-using-learning-
