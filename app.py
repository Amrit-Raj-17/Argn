from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
import docx
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and lemmatize
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    processed_tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token.isalnum() and token not in stop_words
    ]
    
    return " ".join(processed_tokens)

def calculate_ats_score(resume_text, job_description):
    # Vectorize the texts
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])
    
    # Calculate similarity
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    # Convert to percentage
    ats_score = round(similarity * 100, 2)
    return ats_score

def fetch_jobs(job_role, job_type):
    # This is a mock function - in production, you'd integrate with real job APIs
    # For demonstration, returning sample data
    sample_jobs = [
        {
            "title": f"Senior {job_role}",
            "company": "Tech Corp",
            "location": "New York, NY",
            "type": job_type,
            "description": f"We are looking for an experienced {job_role} to join our team...",
        },
        {
            "title": f"{job_role} Lead",
            "company": "Innovation Labs",
            "location": "San Francisco, CA",
            "type": job_type,
            "description": f"Exciting opportunity for a {job_role} professional...",
        },
        {
            "title": f"Staff {job_role}",
            "company": "Future Systems",
            "location": "Austin, TX",
            "type": job_type,
            "description": f"Join our growing team as a {job_role}...",
        }
    ]
    return sample_jobs

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    file = request.files['resume']
    job_role = request.form.get('job_role')
    job_type = request.form.get('job_type')
    
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
    
    if not job_role or not job_type:
        return jsonify({'error': 'Job role and type are required'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    try:
        # Extract text from resume
        if filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400
        
        # Fetch jobs and calculate scores
        jobs = fetch_jobs(job_role, job_type)
        analyzed_jobs = []
        
        for job in jobs:
            ats_score = calculate_ats_score(
                preprocess_text(resume_text),
                preprocess_text(job['description'])
            )
            job['ats_score'] = ats_score
            analyzed_jobs.append(job)
        
        # Sort jobs by ATS score in descending order
        analyzed_jobs.sort(key=lambda x: x['ats_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'jobs': analyzed_jobs
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app.run(debug=True)