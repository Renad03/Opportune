# -*- coding: utf-8 -*-
"""
Interview Preparation Module — VS Code / Local Version
Converted from Google Colab notebook.
Run with: python main.py
"""

# ─────────────────────────────────────────────────────────────
# 0) CONFIGURATION — SET YOUR KEYS AND PATHS HERE
# ─────────────────────────────────────────────────────────────
#nest_asyncio.apply()
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyAfV8cIq5jl-1XjywLYfdeXTLF6U0RdiNM"
GROQ_API_KEY                 = "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"
NGROK_AUTH_TOKEN             = "3BzzJ2cVvVzzJiCHoMjYHkC8AC8_3tPV6dMUVJy2tDqRJ76mC"


DATA_FOLDER = "Data"
DS1_JSON    = "Cleaned_Computer_Science_Questions.json"
DS2_CSV     = "dataset_cleaned.csv"
DS3_JSON    = "train_cleaned.json"
DS4_CSV     = "software_questions_cleaned.csv"
DS5_JSON = "generated_cache.json"


# ─────────────────────────────────────────────────────────────
# 1) STANDARD LIBRARY IMPORTS
# ─────────────────────────────────────────────────────────────
import json
import re
import time
import random
import tempfile
import threading
import builtins
from collections import defaultdict, Counter

# ─────────────────────────────────────────────────────────────
# 2) THIRD-PARTY IMPORTS
# ─────────────────────────────────────────────────────────────
import numpy as np
import pandas as pd
import torch
import faiss
import fitz
import uvicorn
import nest_asyncio
import unicodedata
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sentence_transformers import SentenceTransformer, util
from transformers import T5ForConditionalGeneration, T5Tokenizer
from groq import Groq
from google import genai
from google.genai import types
from pyngrok import ngrok
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
# ─────────────────────────────────────────────────────────────
# 3) ENVIRONMENT SETTINGS
# ─────────────────────────────────────────────────────────────
os.environ["TOKENIZERS_PARALLELISM"] = "false"
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️  Device: {device}")

# ─────────────────────────────────────────────────────────────
# 4) GEMINI CLIENT  (saved BEFORE Groq so it is never overwritten)
# ─────────────────────────────────────────────────────────────
try:
    gemini_client = genai.Client()
    MODEL_NAME    = "gemini-2.5-flash"
    print("✅ Gemini Client initialized.")
except Exception as e:
    print(f"❌ Gemini init error: {e}")
    gemini_client = None

# ─────────────────────────────────────────────────────────────
# 5) GROQ CLIENT
# ─────────────────────────────────────────────────────────────
groq_client = Groq(api_key=GROQ_API_KEY)

# ─────────────────────────────────────────────────────────────
# 6) GEMINI SCHEMA + SKILL EXTRACTION
# ─────────────────────────────────────────────────────────────
JD_TECH_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "jd_tech_skills": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
            description=(
                "A deduplicated list of ONLY technical skills found in the job description. "
                "Include programming languages, frameworks, libraries, databases, cloud platforms, DevOps tools, "
                "data tools, ML/AI tools, APIs, OS/tools, etc. Exclude soft skills."
            ),
        ),
    },
    required=["jd_tech_skills"],
)


def parse_jd_tech_skills_with_llm(jd_path: str):
    text = ""
    try:
        if jd_path.lower().endswith(".pdf"):
            doc = fitz.open(jd_path)
            for page in doc:
                text += page.get_text()
        else:
            with open(jd_path, "r", encoding="utf-8") as f:
                text = f.read()
        if len(text) > 15000:
            text = text[:15000]
        if not text.strip():
            return {"error": "No text found in JD."}
    except Exception as e:
        return {"error": str(e)}

    prompt = f"""
You are a senior technical recruiter and ATS parser.

Extract ONLY technical skills from the job description text and return JSON with exactly:
{{"jd_tech_skills": ["..."]}}

IMPORTANT: Be EXHAUSTIVE. Include both:
1) Concrete technologies/tools (languages, frameworks, libraries, databases, cloud services, DevOps tools, platforms).
2) Technical concepts/domains explicitly mentioned (e.g., API design/APIs, cloud-native services, multitenancy, distributed systems, infrastructure security, cost optimization, observability, automation, data warehouses, metrics analysis).

Rules:
- Use the ENTIRE text. Do not limit to a single section.
- Technical items ONLY. EXCLUDE soft skills/behavioral traits.
- EXCLUDE benefits/perks, culture statements, and general HR text.
- Keep items short and "skill-like" (1-6 words).
- Deduplicate aggressively: include each skill ONCE.
- Normalize: "Amazon Web Services" -> "AWS", "Google Cloud Platform" -> "GCP", "Postgres" -> "PostgreSQL", "Infrastructure as Code" -> "IaC".
- Keep acronyms when common (CI/CD, ECS).

Return ONLY valid JSON matching the schema.

JOB DESCRIPTION TEXT:
---
{text}
"""

    try:
        response = gemini_client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=JD_TECH_SCHEMA,
            ),
        )
        data = json.loads(response.text)
        skills = data.get("jd_tech_skills", [])
        cleaned, seen = [], set()
        for s in skills:
            if not isinstance(s, str):
                continue
            s2 = s.strip()
            if not s2:
                continue
            key = s2.lower()
            if key not in seen:
                seen.add(key)
                cleaned.append(s2)
        return {"jd_tech_skills": cleaned}
    except Exception as e:
        return {"error": f"API Error: {e}"}


def extract_skills_from_text(job_description_text: str):
    """API wrapper: converts raw text → temp file → parse_jd_tech_skills_with_llm."""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.txt', delete=False, encoding='utf-8'
    ) as tmp:
        tmp.write(job_description_text)
        tmp_path = tmp.name
    try:
        result = parse_jd_tech_skills_with_llm(tmp_path)
        print(f"DEBUG skills result: {result}")
        return result.get("jd_tech_skills", [])
    finally:
        os.unlink(tmp_path)

# ─────────────────────────────────────────────────────────────
# 7) CLUSTERING HELPERS
# ─────────────────────────────────────────────────────────────
def is_skill_like(text: str, max_tokens=6, max_chars=45):
    if not text:
        return False
    t = str(text).strip().lower()
    t = " ".join(t.split())
    if len(t) > max_chars or len(t.split()) > max_tokens or len(t) < 2:
        return False
    if re.search(r"\b(i|we|they|built|developed|implemented|responsible|manage|leading)\b", t):
        return False
    return True


def normalize_skill(x: str) -> str:
    x = str(x).strip().lower()
    return " ".join(x.split())


def clean_list(xs):
    out, seen = [], set()
    for x in xs:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def build_skill_candidates_from_jd(jd_data):
    raw = jd_data.get("jd_tech_skills", []) or []
    cleaned = [normalize_skill(x) for x in raw if is_skill_like(normalize_skill(x))]
    return clean_list(cleaned)


def pick_k_silhouette(embeddings, k_min=2, k_max=6, random_state=42):
    n = embeddings.shape[0]
    if n < 3:
        return 1
    k_max = min(k_max, n - 1)
    if k_max < 2:
        return 1
    k_min = max(2, min(k_min, k_max))
    best_k, best_score = k_min, -1
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, n_init="auto", random_state=random_state)
        labels = km.fit_predict(embeddings)
        if len(set(labels)) < 2:
            continue
        score = silhouette_score(embeddings, labels, metric="cosine")
        if score > best_score:
            best_score, best_k = score, k
    return best_k


def cluster_skills_kmeans(skills, model_sim, k=None, k_min=3, k_max=10, random_state=42):
    skills = clean_list(skills)
    if len(skills) == 0:
        return {"k": 0, "clusters": {}}
    if len(skills) == 1:
        return {"k": 1, "clusters": {0: skills}}
    emb = model_sim.encode(skills, convert_to_numpy=True, normalize_embeddings=True)
    if k is None:
        k = pick_k_silhouette(emb, k_min=k_min, k_max=k_max, random_state=random_state)
        if k == 1:
            return {"k": 1, "clusters": {0: skills}}
    km = KMeans(n_clusters=k, n_init="auto", random_state=random_state)
    labels = km.fit_predict(emb)
    clusters = defaultdict(list)
    for skill, lab in zip(skills, labels):
        clusters[int(lab)].append(skill)
    return {"k": k, "clusters": dict(clusters)}

# ─────────────────────────────────────────────────────────────
# 8) DATASET LOADING
# ─────────────────────────────────────────────────────────────
def load_all_datasets():
    unified  = []
    ds1_path = os.path.join(DATA_FOLDER, DS1_JSON)
    ds2_path = os.path.join(DATA_FOLDER, DS2_CSV)
    ds3_path = os.path.join(DATA_FOLDER, DS3_JSON)
    ds4_path = os.path.join(DATA_FOLDER, DS4_CSV)
    CACHE_JSON = "generated_cache.json"

    print("📂 Loading Dataset 1 (Main JSON)...")
    with open(ds1_path, "r") as f:
        raw = json.load(f)
    data1 = raw if isinstance(raw, list) else next(iter(raw.values()))
    for r in data1:
        q = str(r.get("question", "")).strip()
        a = str(r.get("answer", "")).strip()
        if q and a:
            unified.append({"question": q, "answer": a, "subject": r.get("subject", r.get("subfield", "General")), "field": "Computer Science", "source": "dataset_main"})
    print(f"   ✅ {len(data1)} records")

    print("📂 Loading Dataset 2 (Machine Learning CSV)...")
    df2 = pd.read_csv(ds2_path)
    for _, row in df2.iterrows():
        q = str(row.get("question", "")).strip()
        a = str(row.get("answer", "")).strip()
        if q and a:
            unified.append({"question": q, "answer": a, "subject": "Machine Learning", "field": "Computer Science", "source": "dataset_ml"})
    print(f"   ✅ {len(df2)} records")

    print("📂 Loading Dataset 3 (General CS JSON)...")
    with open(ds3_path, "r") as f:
        data3 = json.load(f)
    for r in data3:
        q = str(r.get("question", "")).strip()
        a = str(r.get("answer", "")).strip()
        if q and a:
            unified.append({"question": q, "answer": a, "subject": "General Computer Science", "field": "Computer Science", "source": "dataset_jsonl"})
    print(f"   ✅ {len(data3)} records")

    print("📂 Loading Dataset 4 (Software Engineering CSV)...")
    df4 = pd.read_csv(ds4_path)
    for _, row in df4.iterrows():
        q = str(row.get("question", "")).strip()
        a = str(row.get("answer", "")).strip()
        cat  = str(row.get("category", "Software Engineering")).strip()
        diff = str(row.get("difficulty", "")).strip()
        if q and a:
            unified.append({"question": q, "answer": a, "subject": cat if cat != "nan" else "Software Engineering", "field": "Computer Science", "source": "dataset_software", "difficulty": diff if diff != "nan" else ""})
    print(f"   ✅ {len(df4)} records")

    cache_path = os.path.join(DATA_FOLDER, CACHE_JSON)
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        print("📂 Loading Generated Cache...")
        with open(cache_path, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        print(f"   DEBUG: cache file has {len(cache_data)} entries")
        before_cache = len(unified)
        for r in cache_data:
            q = str(r.get("question", "")).strip()
            a = str(r.get("answer", "")).strip()
            if q and a:
                unified.append({
                    "question": q,
                    "answer":   a,
                    "subject":  r.get("subject", ""),
                    "field":    r.get("subject", ""),
                    "source":   "dataset_generated_cache"
                })
        print(f"   DEBUG: added {len(unified) - before_cache} from cache to unified")
        print(f"   ✅ {len(cache_data)} cached records")
    else:
        print(f"⚠️ Cache file missing or empty: {cache_path}")




    print(f"\n🔍 Removing cross-dataset duplicates...")
    before = len(unified)
    seen, deduped = set(), []
    for r in unified:
        key = " ".join(re.sub(r'[^\w\s]', '', r["question"].lower().strip()).split())
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    print(f"   Removed {before - len(deduped)} cross-dataset duplicates")

    cache_in_final = sum(1 for r in deduped if r.get("source") == "dataset_generated_cache")
    print(f"   DEBUG: cache records surviving dedup: {cache_in_final}")
    print(f"\n{'='*40}")
    print(f"📦 TOTAL RECORDS: {len(deduped)}")
    for src, count in Counter(r["source"] for r in deduped).items():
        print(f"   {src}: {count}")
    print(f"{'='*40}")
    return deduped

# ─────────────────────────────────────────────────────────────
# 9) GROQ HELPER
# ─────────────────────────────────────────────────────────────
def get_completion(prompt, model="llama-3.1-8b-instant"):
    chat_completion = groq_client.chat.completions.create(
        model=model, temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content

# ─────────────────────────────────────────────────────────────
# 10) RAG / QUESTION GENERATION FUNCTIONS
# ─────────────────────────────────────────────────────────────
def retrieve_relevant_questions(skills, index, data, embedder, top_k=3):
    query = "interview question about " + ", ".join(skills)
    query_embedding = embedder.encode([query], normalize_embeddings=True)
    scores, indices = index.search(query_embedding, top_k)
    retrieved = []
    for idx in indices[0]:
        record = data[idx]
        retrieved.append({"question": record.get("question", ""), "answer": record.get("answer", ""), "subject": record.get("subject", "")})
    return retrieved


def generate_ideal_answer_groq(question, skills):
    skills_str = ", ".join(skills)
    prompt = (
        f"You are a senior software engineer conducting a technical interview.\n"
        f"The candidate is being evaluated on: {skills_str}\n\n"
        f"Interview Question: {question}\n\n"
        f"Provide a model answer that a strong candidate should give.\n"
        f"Requirements:\n"
        f"- Be technically accurate and specific\n"
        f"- Cover the key concepts related to {skills_str}\n"
        f"- Write 4-6 clear sentences\n"
        f"- Do not include phrases like 'Great question' or 'As an AI'\n"
        f"- Go straight to the answer\n\nAnswer:"
    )
    return get_completion(prompt, model="llama-3.1-8b-instant").strip()

def save_to_cache(result: dict, cache_path="Data/generated_cache.json"):
    try:
        new_entry = {
            "question": result["question"],
            "answer":   result["answer"],
            "subject":  ", ".join(result["skills"]),
            "field":    ", ".join(result["skills"]),
            "source":   "dataset_generated_cache"
        }
        
        # Save to disk
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cache = []
        cache.append(new_entry)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        
        # Also add to live in-memory data so current session can use it
        builtins.data_global.append(new_entry)
        
        # Rebuild FAISS index entry for this new record
        new_corpus = f"{new_entry['subject']} {new_entry['field']} {new_entry['question']}".strip()
        new_emb = builtins.embedder_global.encode([new_corpus], convert_to_numpy=True, normalize_embeddings=True)
        builtins.index_global.add(new_emb)

        print(f"   DEBUG save path: {cache_path}")           # ← add this
        print(f"   DEBUG cache now has: {len(cache)} entries") # ← add this
        print(f"✅ Cached + added to live index")
    except Exception as e:
        print(f"⚠️ Cache save failed: {e}")


# def generate_rag_question(cluster_id, skills, index, data, embedder, difficulty="intermediate"):
#     retrieved  = retrieve_relevant_questions(skills, index, data, embedder, top_k=3)
#     context    = ""
#     for i, r in enumerate(retrieved[:3]):   
#         clean_q = r['question'].split("|")[0].strip()[:100]  
#         context += f"Example {i+1}: {clean_q}\n"  

#     skills_str       = ", ".join(skills)
#     question_prompt  = (
#         f"Generate a {difficulty} level technical interview question "
#         f"about {skills_str}. "
#         f"The question must be directly about {skills_str}. "
#         f"Use these examples as style reference only: {context}"
#         f"Generate one new question without any prefix like Q: or A::"
#     )

#     inputs = gen_tokenizer(question_prompt, return_tensors="pt", max_length=512, truncation=True).to(device)
#     q_outputs = gen_model.generate(
#         input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"],
#         max_length=80, min_length=10, num_beams=1,
#         no_repeat_ngram_size=3, repetition_penalty=2.5,
#         length_penalty=1.0, early_stopping=True,
#     )
#     question = gen_tokenizer.decode(q_outputs[0], skip_special_tokens=True).strip()
#     question = question.replace("A:", "").replace("Q:", "").split("|")[0].strip()

#     print(f"     💭 Generating ideal answer with LLaMA...")
#     ideal_answer = generate_ideal_answer_groq(question, skills)
    
#     result = {"cluster_id": cluster_id, "skills": skills, "question": question, "answer": ideal_answer, "source": "generated"}
#     save_to_cache(result)  # ← save before returning
#     return result


def generate_rag_question(cluster_id, skills, index, data, embedder, difficulty="intermediate"):
    skills_str = ", ".join(skills)
    
    prompt = (
        f"You are a technical interviewer. Generate exactly ONE {difficulty}-level "
        f"technical interview question specifically about: {skills_str}.\n\n"
        f"Rules:\n"
        f"- The question MUST be directly about {skills_str}\n"
        f"- No generic questions like 'what is a bug' or 'how to get a job'\n"
        f"- No prefix like Q: or A: or numbering\n"
        f"- Return only the question text, nothing else\n\n"
        f"Question:"
    )
    
    question = get_completion(prompt, model="llama-3.1-8b-instant").strip()
    question = question.replace("Q:", "").replace("A:", "").split("\n")[0].strip()
    
    print(f"     💭 Generating ideal answer with LLaMA...")
    ideal_answer = generate_ideal_answer_groq(question, skills)
    
    result = {"cluster_id": cluster_id, "skills": skills, "question": question, "answer": ideal_answer, "source": "generated"}
    save_to_cache(result)
    return result

def question_is_relevant(question, skills):
    question_lower = question.lower()
    skills_words   = " ".join(skills).lower().split()
    return any(word in question_lower for word in skills_words)


def questions_are_similar(q1, q2, threshold=0.85):
    """Use semantic similarity instead of word overlap — much more accurate."""
    emb1 = embedder.encode(q1, convert_to_tensor=True, normalize_embeddings=True)
    emb2 = embedder.encode(q2, convert_to_tensor=True, normalize_embeddings=True)
    score = float(util.cos_sim(emb1, emb2)[0][0])
    return score > threshold

def normalize_text_basic(x: str) -> str:
    x = str(x).strip().lower()
    x = re.sub(r"[^\w\s/+\-\.]", " ", x)
    return " ".join(x.split())


def exact_match_score(record, skill):
    skill_text      = normalize_text_basic(skill)
    record_subject  = normalize_text_basic(record.get("subject", ""))
    record_field    = normalize_text_basic(record.get("field", ""))
    record_question = normalize_text_basic(record.get("question", ""))
    score = 0.0
    if skill_text == record_subject:        score += 5.0
    elif skill_text and skill_text in record_subject:  score += 3.0
    if skill_text == record_field:          score += 3.5
    elif skill_text and skill_text in record_field:    score += 5.0
    if skill_text and skill_text in record_question:   score += 0.8
    return score


def is_valid_record(record):
    return bool(record.get("question", "").strip()) and bool(record.get("answer", "").strip())


def retrieve_exact_matches(skill, data, top_k=20):
    candidates = []
    for r in data:
        if not is_valid_record(r):
            continue
        score = exact_match_score(r, skill)   # computed ONCE
        if score > 0:
            candidates.append((score, r))
    print(f"  [exact_match] skill='{skill}' → {len(candidates)} candidates before top_k cut")
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[:top_k]


def retrieve_exact_matches_for_cluster(skills, data, top_k=5):
    score_map = {}
    for skill in skills:
        for score, record in retrieve_exact_matches(skill, data, top_k=20):
            key = record.get("question", "").strip().lower()
            if key not in score_map:
                score_map[key] = {"score": 0.0, "record": record}
            score_map[key]["score"] += score
    sorted_matches = sorted(score_map.values(), key=lambda x: x["score"], reverse=True)
    return [(item["score"], item["record"]) for item in sorted_matches[:top_k]]


# def get_question_for_cluster(cluster_id, skills, index, data, embedder, difficulty="intermediate"):
#     exact_matches = retrieve_exact_matches_for_cluster(skills, data, top_k=5)
#     if exact_matches:
#         best_score, best_record = exact_matches[0]
#         if best_score >= 5.0:
#             question = best_record.get("question", "").replace("A:", "").replace("Q:", "").split("|")[0].strip()
#             answer   = best_record.get("answer", "").strip()
#             if question and answer:
#                 print(f"  📖 Exact match found (score: {best_score:.1f}): {question[:60]}...")
#                 return {"cluster_id": cluster_id, "skills": skills, "question": question, "answer": answer, "source": "dataset_exact", "match_score": best_score}

#     skills_str  = ", ".join(skills)
#     query       = f"interview question about {skills_str}"
#     query_emb   = embedder.encode([query], normalize_embeddings=True)
#     scores, indices = index.search(query_emb, 1)
#     match_score = float(scores[0][0])
#     best_match  = data[indices[0][0]]

#     if match_score >= 0.75:
#         question = best_match.get("question", "").replace("A:", "").replace("Q:", "").split("|")[0].strip()
#         answer   = best_match.get("answer", "").strip()
#         if question and answer:
#             print(f"  📚 Using dataset question directly (match: {match_score:.2f})")
#             return {"cluster_id": cluster_id, "skills": skills, "question": question, "answer": answer, "source": "dataset_direct", "match_score": match_score}

#     print(f"  🔄 Generating new question (best match: {match_score:.2f})")
#     return generate_rag_question(cluster_id, skills, index, data, embedder, difficulty)


# 


def get_question_for_cluster(cluster_id, skills, index, data, embedder,
                              difficulty="intermediate", exact_matches_cache=None,
                              used_questions=None):  # ← add this parameter
    if used_questions is None:
        used_questions = set()

    if exact_matches_cache is None:
        exact_matches = retrieve_exact_matches_for_cluster(skills, data, top_k=5)
    else:
        exact_matches = exact_matches_cache

    if exact_matches:
        for score, record in exact_matches:  # ← iterate all matches, not just best
            question = record.get("question", "").replace("A:", "").replace("Q:", "").split("|")[0].strip()
            answer   = record.get("answer", "").strip()
            key      = question.strip().lower()[:100]
            
            if key in used_questions:  # ← skip already used
                continue
                
            if score >= 3.0 and question and answer:
                print(f"  📖 Exact match found (score: {score:.1f}): {question[:60]}...")
                return {"cluster_id": cluster_id, "skills": skills, "question": question,
                        "answer": answer, "source": "dataset_exact", "match_score": score}

    skills_str  = ", ".join(skills)
    query       = f"interview question about {skills_str}"
    query_emb   = embedder.encode([query], normalize_embeddings=True)
    
    # Search more candidates to find one not already used
    scores, indices = index.search(query_emb, 10)  # ← search top 10 instead of 1
    for i in range(len(indices[0])):
        match_score = float(scores[0][i])
        best_match  = data[indices[0][i]]
        question = best_match.get("question", "").replace("A:", "").replace("Q:", "").split("|")[0].strip()
        answer   = best_match.get("answer", "").strip()
        key      = question.strip().lower()[:100]
        
        if key in used_questions:  # ← skip already used
            continue
            
        if match_score >= 0.6 and question and answer:
            print(f"  📚 Using dataset question directly (match: {match_score:.2f})")
            return {"cluster_id": cluster_id, "skills": skills, "question": question,
                    "answer": answer, "source": "dataset_direct", "match_score": match_score}

    print(f"  🔄 Generating new question...")
    return generate_rag_question(cluster_id, skills, index, data, embedder, difficulty)

# def generate_question_for_cluster_task(args):
#     cid, skills, index, data, embedder, questions_per_cluster = args
#     difficulties     = ["junior", "intermediate", "senior"]
#     actual_questions = 1 if len(skills) <= 2 else questions_per_cluster
#     results          = []
#     generated_qs     = []

#     for i in range(actual_questions):
#         difficulty = difficulties[i % len(difficulties)]
#         for attempt in range(1):
#             skills_subset = random.sample(skills, max(2, len(skills) // 2)) if attempt > 0 and len(skills) > 2 else skills
#             result        = get_question_for_cluster(cid, skills_subset, index, data, embedder, difficulty)
#             is_duplicate  = any(questions_are_similar(result["question"], prev_q) for prev_q in generated_qs)
#             is_relevant   = question_is_relevant(result["question"], skills_subset)
#             if not is_duplicate and is_relevant:
#                 generated_qs.append(result["question"])
#                 results.append(result)
#                 break
#     return results
def generate_question_for_cluster_task(args):
    cid, skills, index, data, embedder, questions_per_cluster = args
    difficulties = ["junior", "intermediate", "senior"]
    actual_questions = 1 if len(skills) <= 2 else questions_per_cluster
    results = []
    generated_qs = []

    exact_matches_cache = retrieve_exact_matches_for_cluster(skills, data, top_k=10)

    for i in range(actual_questions):
        difficulty = difficulties[i % len(difficulties)]
        
        for attempt in range(3):  # retry up to 3 times if duplicate
            result = get_question_for_cluster(
                cid, skills, index, data, embedder, difficulty,
                exact_matches_cache=exact_matches_cache
            )

            is_duplicate = any(questions_are_similar(result["question"], prev_q)
                               for prev_q in generated_qs)
            is_relevant  = question_is_relevant(result["question"], skills)
            source       = result.get("source", "")
            is_from_dataset = source in ("dataset_exact", "dataset_direct")
            is_generated    = source == "generated"

            if not is_duplicate and (is_relevant or is_from_dataset or is_generated):
                generated_qs.append(result["question"])
                results.append(result)
                break

            if is_from_dataset:
                break  # dataset will always return same record, no point retrying

            print(f"  ⚠️ Attempt {attempt+1} duplicate detected, retrying...")

    return results

# def generate_rag_questions_for_clusters(clustering_result, index, data, embedder, questions_per_cluster=2):
#     cluster_items = list(clustering_result["clusters"].items())
#     tasks         = [(cid, skills, index, data, embedder, questions_per_cluster) for cid, skills in cluster_items]
#     all_results   = []

#     print(f"\n⚡ Generating questions for {len(tasks)} clusters IN PARALLEL...")
#     max_workers = min(len(tasks), 4)

#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = {executor.submit(generate_question_for_cluster_task, task): task[0] for task in tasks}
#         for future in as_completed(futures):
#             cid = futures[future]
#             try:
#                 cluster_results = future.result()
#                 all_results.extend(cluster_results)
#                 print(f"  ✅ Cluster {cid} done — {len(cluster_results)} question(s)")
#             except Exception as e:
#                 print(f"  ❌ Cluster {cid} failed: {e}")

#     return all_results

def generate_rag_questions_for_clusters(clustering_result, index, data, embedder, questions_per_cluster=1):
    cluster_items = list(clustering_result["clusters"].items())
    all_results = []
    used_questions = set()  # track across all clusters

    print(f"\n⚡ Generating questions for {len(cluster_items)} clusters...")

    for cid, skills in cluster_items:
        try:
            results = generate_question_for_cluster_task_v2(
                cid, skills, index, data, embedder, questions_per_cluster, used_questions
            )
            for r in results:
                used_questions.add(r["question"].strip().lower()[:100])
            all_results.extend(results)
            print(f"  ✅ Cluster {cid} done — {len(results)} question(s)")
        except Exception as e:
            print(f"  ❌ Cluster {cid} failed: {e}")

    return all_results

def generate_question_for_cluster_task_v2(cid, skills, index, data, embedder, questions_per_cluster, used_questions):
    difficulties = ["junior", "intermediate", "senior"]
    actual_questions = 1 if len(skills) <= 2 else questions_per_cluster
    results = []
    generated_qs = list(used_questions)
    local_used = set(used_questions)

    exact_matches_cache = retrieve_exact_matches_for_cluster(skills, data, top_k=10)

    for i in range(actual_questions):
        difficulty = difficulties[i % len(difficulties)]
        got_question = False

        for attempt in range(3):
            # Always pass local_used so get_question_for_cluster skips already used questions
            result = get_question_for_cluster(
                cid, skills, index, data, embedder, difficulty,
                exact_matches_cache=exact_matches_cache,
                used_questions=local_used  # ← this is the key fix
            )

            is_duplicate = any(questions_are_similar(result["question"], prev_q)
                               for prev_q in generated_qs)
            is_relevant  = question_is_relevant(result["question"], skills)
            source       = result.get("source", "")
            is_from_dataset = source in ("dataset_exact", "dataset_direct")
            is_generated    = source == "generated"

            if not is_duplicate and (is_relevant or is_from_dataset or is_generated):
                generated_qs.append(result["question"])
                local_used.add(result["question"].strip().lower()[:100])
                results.append(result)
                got_question = True
                break

            print(f"  ⚠️ Cluster {cid} attempt {attempt+1}: duplicate detected, forcing generation...")
            
            # Mark the duplicate as used so next attempt skips it
            local_used.add(result["question"].strip().lower()[:100])
            
            # Force LLaMA generation directly, skip dataset lookup
            result = generate_rag_question(cid, skills, index, data, embedder, difficulty)
            is_duplicate = any(questions_are_similar(result["question"], prev_q)
                               for prev_q in generated_qs)
            if not is_duplicate:
                generated_qs.append(result["question"])
                local_used.add(result["question"].strip().lower()[:100])
                results.append(result)
                got_question = True
                break

        if not got_question:
            print(f"  ⚠️ Cluster {cid}: could not find unique question after 3 attempts")

    return results

def sanitize_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2013', '-').replace('\u2014', '-')
    return text.strip()
# ─────────────────────────────────────────────────────────────
# 11) EVALUATION FUNCTIONS
# ─────────────────────────────────────────────────────────────
def compute_cosine_similarity(sentence_a, sentence_b):
    embedding_a = embedder.encode(sentence_a, convert_to_tensor=True, normalize_embeddings=True)
    embedding_b = embedder.encode(sentence_b, convert_to_tensor=True, normalize_embeddings=True)
    score = util.cos_sim(embedding_a, embedding_b)
    return round(float(score[0][0]), 3)


def compute_hybrid_score(user_answer, correct_answer, question):
    correctness = compute_cosine_similarity(user_answer, correct_answer)
    relevance   = compute_cosine_similarity(user_answer, question)
    final_score = (correctness + relevance) / 2
    return {"hybrid_score": round(final_score, 3), "correctness": round(correctness, 3), "relevance": round(relevance, 3)}


def get_grade(score):
    if score >= 0.67:   return "Excellent ✅"
    elif score >= 0.6:  return "Good 👍"
    elif score >= 0.49: return "Partial ⚠️"
    else:               return "Needs Improvement ❌"


def evaluate_question(question, user_answer, correct_answer, cluster_id, skills):
    scores = compute_hybrid_score(user_answer, correct_answer, question)
    return {"cluster_id": cluster_id, "skills": skills, "question": question, "user_answer": user_answer, "correct_answer": correct_answer, "grade": get_grade(scores["hybrid_score"]), **scores}


def generate_cluster_feedback(cluster_results):
    clusters = defaultdict(list)
    for r in cluster_results:
        clusters[r["cluster_id"]].append(r)
    report = {}
    for cid, results in clusters.items():
        avg_score    = np.mean([r["hybrid_score"] for r in results])
        avg_correct  = np.mean([r["correctness"]  for r in results])
        avg_relevant = np.mean([r["relevance"]    for r in results])
        skills       = results[0]["skills"]
        grade        = get_grade(avg_score)
        weak_metrics = []
        if avg_score < 0.68:
            if avg_correct  < 0.55: weak_metrics.append("answer correctness (key concepts missing)")
            if avg_relevant < 0.55: weak_metrics.append("answer relevance (answer may be off-topic)")
        report[cid] = {
            "cluster_id": cid, "skills": skills,
            "avg_score": round(avg_score, 3), "avg_correct": round(avg_correct, 3),
            "avg_relevant": round(avg_relevant, 3), "grade": grade,
            "weak_metrics": weak_metrics, "num_questions": len(results), "details": results
        }
    return report

# ─────────────────────────────────────────────────────────────
# 12) FASTAPI APP  ← TWO SEPARATE ENDPOINTS
# ─────────────────────────────────────────────────────────────
app = FastAPI(title="Interview Preparation Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ─────────────────────────────────
class GenerateQuestionsRequest(BaseModel):
    """Call 1 — send the job description, get back questions."""
    job_description: str


class AnswerItem(BaseModel):
    """A single answered question to evaluate."""
    cluster_id:     int
    skills:         List[str]
    question:       str
    user_answer:    str
    correct_answer: str


class EvaluateAnswersRequest(BaseModel):
    """Call 2 — send the answered questions, get back the report."""
    answers: List[AnswerItem]


# ── ENDPOINT 1 : Generate Questions ──────────────────────────
@app.post("/interview/generate")
async def generate_questions(request: GenerateQuestionsRequest):
    print(f"DEBUG received: {request}")          # ← add this
    print(f"DEBUG job_description: '{request.job_description}'")
    """
    Receives a job description and returns personalised interview questions.

    Request  : { "job_description": "..." }
    Response : {
        "status":    "questions_ready",
        "skills":    [...],
        "questions": [
            { "cluster_id": 0, "skills": [...], "question": "...", "answer": "..." },
            ...
        ]
    }
    """
    try:
        _index     = builtins.index_global
        _data      = builtins.data_global
        _model_sim = builtins.model_sim_global

        # Step 1 — extract skills
        skills = extract_skills_from_text(request.job_description)
        if not skills:
            raise HTTPException(status_code=400, detail="No skills could be extracted from the job description")

        # Step 2 — cluster skills
        clustering_result = cluster_skills_kmeans(skills, _model_sim, k=None, k_min=3, k_max=9)

        # Step 3 — generate questions
        questions = generate_rag_questions_for_clusters(
            clustering_result, _index, _data, embedder, questions_per_cluster=2
        )
                # After generating questions, deduplicate across clusters
        seen_questions = set()
        unique_questions = []
        for q in questions:
            key = q["question"].strip().lower()[:100]  # use first 100 chars as key
            if key not in seen_questions:
                seen_questions.add(key)
                unique_questions.append(q)
        questions = unique_questions

        return {
            "status":    "questions_ready",
            "skills":    skills,
            "questions": [
                {
                    "cluster_id": q["cluster_id"],
                    "skills":     q["skills"],
                   "question":   sanitize_text(q["question"]),
                   "answer":     sanitize_text(q["answer"]),
                }
                for q in questions
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── ENDPOINT 2 : Evaluate Answers ────────────────────────────
@app.post("/interview/evaluate")
async def evaluate_answers(request: EvaluateAnswersRequest):
    """
    Receives answered questions and returns a per-cluster feedback report.

    Request  : {
        "answers": [
            {
                "cluster_id": 0,
                "skills": ["docker", "ecs"],
                "question": "...",
                "user_answer": "...",
                "correct_answer": "..."
            }
        ]
    }
    Response : {
        "status":        "report_ready",
        "overall_score": 0.72,
        "overall_grade": "Good 👍",
        "clusters": {
            "0": {
                "cluster_id": 0,
                "skills": [...],
                "avg_score": 0.75,
                "grade": "Excellent ✅",
                "weak_metrics": []
            }
        }
    }
    """
    try:
        if not request.answers:
            raise HTTPException(status_code=400, detail="No answers provided")

        results = []
        for item in request.answers:
            scores = compute_hybrid_score(item.user_answer, item.correct_answer, item.question)
            grade  = get_grade(scores["hybrid_score"])
            results.append({
                "cluster_id":     item.cluster_id,
                "skills":         item.skills,
                "question":       item.question,
                "user_answer":    item.user_answer,
                "correct_answer": item.correct_answer,
                "grade":          grade,
                **scores
            })

        report        = generate_cluster_feedback(results)
        all_scores    = [d["avg_score"] for d in report.values()]
        overall       = round(float(np.mean(all_scores)), 3)
        overall_grade = get_grade(overall)

        clusters = {}
        for cid, d in report.items():
            clusters[str(cid)] = {
                "cluster_id":   d["cluster_id"],
                "skills":       d["skills"],
                "avg_score":    d["avg_score"],
                "grade":        d["grade"],
                "weak_metrics": d["weak_metrics"],
            }

        return {
            "status":        "report_ready",
            "overall_score": overall,
            "overall_grade": overall_grade,
            "clusters":      clusters
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Health check ──────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "running", "module": "Interview Preparation"}


# ─────────────────────────────────────────────────────────────
# 13) MAIN — LOAD MODELS, THEN START API
# ─────────────────────────────────────────────────────────────
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    print("Loading SentenceTransformer (all-MiniLM-L6-v2)...")
    model_sim = SentenceTransformer('all-MiniLM-L6-v2')
    embedder  = model_sim
    print("✅ SentenceTransformer loaded")

    gen_model_name = "google/flan-t5-large"
    print(f"Loading {gen_model_name}...")
    gen_tokenizer = T5Tokenizer.from_pretrained(gen_model_name)
    gen_model     = T5ForConditionalGeneration.from_pretrained(gen_model_name).to(device)
    print(f"✅ {gen_model_name} loaded")

    data = load_all_datasets()

    print("🔄 Building FAISS index...")
    corpus = [f"{r.get('subject','')} {r.get('field','')} {r.get('question','')}".strip() for r in data]
    corpus_embeddings = embedder.encode(corpus, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=True)
    dimension = corpus_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(corpus_embeddings)
    print(f"✅ FAISS index ready with {index.ntotal} entries")

    builtins.embedder_global       = embedder
    builtins.index_global          = index
    builtins.data_global           = data
    builtins.model_sim_global      = model_sim
    builtins.gen_model_global      = gen_model
    builtins.gen_tokenizer_global  = gen_tokenizer
    builtins.gemini_client_global  = gemini_client
    print("✅ All models stored in builtins")

    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(8001)

    print("="*60)
    print(f"✅ API is live at: {public_url}")
    print(f"📖 Docs: {public_url}/docs")
    print("="*60)
    print(f"\nShare with backend team:")
    print(f"  Generate : POST {public_url}/interview/generate")
    print(f"  Evaluate : POST {public_url}/interview/evaluate")

    nest_asyncio.apply()
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()

    print("\n🟢 Server is running. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        ngrok.kill()