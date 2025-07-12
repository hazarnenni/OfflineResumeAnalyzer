# Offline Resume Analyzer

A Streamlit app that analyzes your resume (PDF) offline — no internet or API required!  
It checks for key sections, extracts technical and soft skills, counts words, and matches your resume against a job description.

## Features
- Extracts text from PDF resumes
- Checks for required sections like Experience, Education, Skills, etc.
- Detects technical and soft skills from uploaded CSV lists
- Provides basic suggestions to improve your resume
- Matches resume skills with a job description (upload or paste)
- Calculates skill match percentages and missing skills

## Requirements
- Python 3.7+
- Streamlit
- PyPDF2
- pandas
- re (built-in)

## Installation

```bash
pip install streamlit PyPDF2 pandas
```

## Usage

```bash
streamlit run app.py
```

Upload your resume and optionally a job description to get feedback.
