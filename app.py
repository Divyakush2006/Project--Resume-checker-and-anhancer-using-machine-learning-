import os
from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
from werkzeug.utils import secure_filename
import tempfile
import shutil
import traceback

# Import your analysis logic from your resume_parser.py file
from resume_parser import run_analysis

app = Flask(__name__)
CORS(app) # Enable CORS for your Flask app

# Configuration for file uploads
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    print("Home route accessed.")
    return "Welcome to the Resume & JD Matcher API! Use the frontend to upload files to /analyze."

@app.route('/analyze', methods=['POST'])
def analyze_documents():
    print("'/analyze' route accessed (POST request).")

    # Ensure both 'resume' and 'job_description' files are in the request
    if 'resume' not in request.files:
        print("Error: No resume file part.")
        return jsonify({"error": "No resume file part in the request."}), 400
    if 'job_description' not in request.files:
        print("Error: No job description file part.")
        return jsonify({"error": "No job description file part in the request."}), 400

    resume_file = request.files['resume']
    jd_file = request.files['job_description']

    # Check if files were actually selected
    if resume_file.filename == '':
        return jsonify({"error": "No resume file selected."}), 400
    if jd_file.filename == '':
        return jsonify({"error": "No job description file selected."}), 400

    # Validate file types
    if not (allowed_file(resume_file.filename) and allowed_file(jd_file.filename)):
        print("Error: Invalid file type.")
        return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

    print("Files received and validated. Attempting to save...")
    temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
    resume_path = None
    jd_path = None

    try:
        resume_filename_safe = secure_filename(resume_file.filename)
        jd_filename_safe = secure_filename(jd_file.filename)

        resume_path = os.path.join(temp_dir, resume_filename_safe)
        jd_path = os.path.join(temp_dir, jd_filename_safe)

        resume_file.save(resume_path)
        jd_file.save(jd_path)
        print(f"Files saved: {resume_path}, {jd_path}")

        print("Calling run_analysis...")
        analysis_results = run_analysis(resume_path, jd_path)

        # *** THESE ARE THE NEW DEBUGGING PRINT STATEMENTS ***
        print("run_analysis completed. Result type:", type(analysis_results))
        # Print a portion of the content, as it can be very long
        print("run_analysis result content (first 1000 chars):", str(analysis_results)[:1000])
        # ******************************************************

        print("Returning JSON.")
        return jsonify(analysis_results), 200

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        traceback.print_exc() # This is crucial for detailed error info
        return jsonify({"error": f"An internal server error occurred: {str(e)}. Please check server logs for details."}), 500
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary directory: {temp_dir}")

# if __name__ == '__main__':
#     # Ensure debug is True for development to see detailed errors
#     app.run(debug=True)
