# Install the PDF reader and the Google GenAI SDK
# %pip install PyMuPDF pillow google-genai
# %pip install sentence-transformers
# %pip install PyMuPDF google-genai


# **cv and job parsing**

from fastapi import FastAPI, UploadFile, File
import os
import json
import fitz
from google import genai
from google.genai import types
from google import genai


app = FastAPI(title="Resume & JD Parser API")

try:
    # Load the key securely from Colab Secrets
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # from environment variables
    client = genai.Client(api_key=GEMINI_API_KEY)
    MODEL_NAME = "gemini-2.5-flash"
    print("Gemini Client initialized successfully using Colab Secrets.")
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    print("Please ensure you have set your 'GEMINI_API_KEY' in Colab Secrets.")

# Schema for parsing a Candidate's CV
CV_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "name": types.Schema(type=types.Type.STRING, description="Full name of the candidate."),
        "email": types.Schema(type=types.Type.STRING, description="Candidate's email address."),
        "phone": types.Schema(type=types.Type.STRING, description="Candidate's phone number."),
        "experience_level": types.Schema(
            type=types.Type.STRING,
            description="Experience level (fresher, junior, mid, senior, lead). Use Unspecified if not mentioned"
        ),
        "skills": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
            description="A list of core technical and soft skills."
        ),
        "education": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "degree": types.Schema(type=types.Type.STRING),
                    "institution": types.Schema(type=types.Type.STRING),
                    "year": types.Schema(type=types.Type.STRING)
                }
            )
        ),
        "jobs": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "title": types.Schema(type=types.Type.STRING),
                    "company": types.Schema(type=types.Type.STRING),
                    "summary": types.Schema(type=types.Type.STRING)
                }
            )
        ),
        "projects": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "name": types.Schema(type=types.Type.STRING),
                    "description": types.Schema(type=types.Type.STRING),
                    "technologies": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING)
                    )
                }
            )
        ),
        "internships": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "title": types.Schema(type=types.Type.STRING),
                    "company": types.Schema(type=types.Type.STRING),
                    "duration": types.Schema(type=types.Type.STRING),
                    "summary": types.Schema(type=types.Type.STRING)
                }
            )
        )
    }
)


# Schema for parsing a Job Description (JD)
JD_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "job_title": types.Schema(type=types.Type.STRING, description="The official title of the role being advertised."),
        "company": types.Schema(type=types.Type.STRING, description="The name of the hiring company."),
        "min_experience_years": types.Schema(type=types.Type.NUMBER, description="The minimum required years of experience (numeric value, use null if none specified)."),
        "required_skills": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="A list of ESSENTIAL technical and soft skills."),
        "preferred_skills": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="A list of optional or 'nice-to-have' skills."),
        "qualifications": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="Required degrees or certifications (e.g., 'BS in Computer Science')."),
    }
)

#Parsing Function

def parse_document_with_llm(document_path, schema, document_type):
    """
    Reads a document (PDF or Text), extracts text, and uses Gemini
    to parse it into a structured Python dictionary based on the provided schema.
    """
    # 1. Extract Text from Document
    text = ""
    try:
        if document_path.lower().endswith('.pdf'):
            doc = fitz.open(document_path)
            for page in doc:
                text += page.get_text()
        else:
            with open(document_path, 'r', encoding='utf-8') as f:
                text = f.read()

        if not text:
            return {"error": f"Could not extract text from {document_type} file."}
    except Exception as e:
        return {"error": f"{document_type} reading failed: {e}"}

    # 2. Call the Gemini API for structured extraction
    prompt = f"""Analyze the following {document_type} text and extract the information based *strictly* on the provided JSON schema. Do not include any text outside of the JSON object.\n\n{document_type} Text:\n---\n{text}
    
               CRITICAL RULES:
                - DO NOT infer experience level.
                - ONLY use explicitly mentioned years of experience or job durations.
                - If NO clear experience duration is mentioned → return "Unspecified".
                - Internships or projects alone DO NOT count as experience.
                - Do NOT guess based on graduation year.
                
                Experience mapping:
                - fresher (<1 year)
                - junior (1–3)
                - mid (3–5)
                - senior (5–10)
                - lead (10+)
                - Unspecified (if not explicitly stated)"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        # Convert the response JSON string into a Python dictionary
        return json.loads(response.text)

    except Exception as e:
        return {"error": f"Gemini API call or JSON parsing failed: {e}"}
