# Endpoint to parse CV
from fastapi import FastAPI
import os
from fastapi import UploadFile, File
from OpportuneParsing import parse_document_with_llm, CV_SCHEMA, JD_SCHEMA

# Import your parsing module
# from your_module import parse_text

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Parsing Module Running!"}

@app.post("/parse/cv/")
async def parse_cv(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    return parse_document_with_llm(temp_path, CV_SCHEMA, "CV")

# Endpoint to parse Job Description
@app.post("/parse/jd/")
async def parse_jd(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    return parse_document_with_llm(temp_path, JD_SCHEMA, "Job Description")