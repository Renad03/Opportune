"""
Converted from the Colab notebook: interview_preparation_RAGT5_(3)_(1) (2).ipynb

Notes:
- Colab-only `!pip install ...` lines were moved to requirements.txt.
- Colab Secrets were replaced with environment variables.
- No functions or core logic were intentionally changed.

Before running:
1) Install packages: pip install -r requirements.txt
2) Set GROQ_API_KEY in your terminal or VS Code environment.
3) Update any dataset paths that still point to /content/Data/... to your local files.
"""

# %% [cell 0]
# ==============================
# Install required libraries (run once)
# ==============================

# ==============================
# Imports
# ==============================
import os
import json
from groq import Groq
import json
import re
from dotenv import load_dotenv
load_dotenv()

# ==============================
# Initialize Groq client
# ==============================
try:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    client = Groq(api_key=GROQ_API_KEY)
    print("Groq Client initialized successfully.")
except Exception as e:
    print(f"Error initializing Groq Client: {e}")
    print("Make sure GROQ_API_KEY is set in your environment or .env file.")

# ==============================
# Helper function (DO NOT CHANGE)
# ==============================
def get_completion(prompt, model="llama-3.1-8b-instant"):
    """
    Send a prompt to Groq LLaMA and return the generated text.
    """
    chat_completion = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content


# %% [cell 2]
# ==============================
# CV / JD parsing - extract technical skills only
# Groq version (replaces Gemini schema-based version)
# ==============================

import fitz  # PyMuPDF for reading PDF files

def extract_json_from_text(text: str):
    """
    Safely extract the first JSON object from model output.
    This helps if the model adds extra text before/after the JSON.
    """
    text = text.strip()

    # Try direct parsing first
    try:
        return json.loads(text)
    except:
        pass

    # Fallback: extract first {...} block
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError("No valid JSON object found in model response.")


def parse_jd_tech_skills_with_llm(jd_path: str):
    """
    Read a job description file (PDF or TXT),
    then use Groq LLaMA to extract ONLY technical skills as JSON.

    Returns:
        {"jd_tech_skills": [...]}   on success
        {"error": "..."}            on failure
    """

    # ==============================
    # 1) Read JD text from file
    # ==============================
    text = ""
    try:
        if jd_path.lower().endswith(".pdf"):
            doc = fitz.open(jd_path)
            for page in doc:
                text += page.get_text()
        else:
            with open(jd_path, "r", encoding="utf-8") as f:
                text = f.read()

        # Truncate very long text to keep prompt reasonable
        if len(text) > 15000:
            text = text[:15000]

        if not text.strip():
            return {"error": "No text found in JD."}

    except Exception as e:
        return {"error": f"File reading error: {e}"}

    # ==============================
    # 2) Prompt the model
    # ==============================
    prompt = f"""
You are a senior technical recruiter and ATS parser.

Extract ONLY technical skills from the following job description.

Return ONLY valid JSON in exactly this format:
{{
  "jd_tech_skills": ["skill 1", "skill 2", "skill 3"]
}}

IMPORTANT:
- Be EXHAUSTIVE.
- Include both:
  1) Concrete technologies/tools:
     programming languages, frameworks, libraries, databases,
     cloud services, DevOps tools, platforms, APIs, operating systems, etc.
  2) Technical concepts/domains explicitly mentioned:
     such as API design, cloud-native services, multitenancy,
     distributed systems, infrastructure security, cost optimization,
     observability, automation, data warehouses, metrics analysis, etc.

Rules:
- Use the ENTIRE text.
- Include technical items ONLY.
- EXCLUDE soft skills and behavioral traits.
- EXCLUDE benefits, perks, company culture, and HR text.
- Keep items short and skill-like:
  prefer noun phrases of 1 to 6 words.
- Avoid full sentences.
- Deduplicate aggressively.
- Normalize common names when appropriate:
  - Amazon Web Services -> AWS
  - Google Cloud Platform / Google Cloud -> GCP
  - Postgres -> PostgreSQL
  - Infrastructure as Code -> IaC
  - Shell scripting -> Shell
- Keep common acronyms like CI/CD, ECS.
- If examples are listed like "Shell, Bash, Python", include each separately.

Return JSON only. No explanation. No markdown fences.

JOB DESCRIPTION TEXT:
---
{text}
"""

    # ==============================
    # 3) Call Groq model
    # ==============================
    try:
        raw_response = get_completion(prompt, model="llama-3.1-8b-instant")

        # Parse JSON from model response
        data = extract_json_from_text(raw_response)

        # ==============================
        # 4) Final cleaning and deduplication
        # ==============================
        skills = data.get("jd_tech_skills", [])
        cleaned = []
        seen = set()

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
        return {"error": f"LLM/API Error: {e}"}


# %% [cell 4]
# =========================
# 0) CONFIG: put your JD file path
# =========================
JD_PATH = r"E:\Opportune\Opportune\interview-preparation-openEndedQuestions\integration\job1.txt" #change this to your JD file path

# =========================
# 1) Parse JD TECH SKILLS ONLY
# Uses the function we already adapted
# =========================
print("Parsing Job Description (TECH skills only)...")
jd_data = parse_jd_tech_skills_with_llm(JD_PATH)

if "error" in jd_data:
    raise ValueError(f"JD parse error: {jd_data['error']}")

# =========================
# 2) Quick preview of extracted skills
# =========================
jd_tech_skills = jd_data.get("jd_tech_skills", [])

print(f"\nExtracted JD technical skills: {len(jd_tech_skills)}")
print(" - " + "\n - ".join(jd_tech_skills[:30]) + ("" if len(jd_tech_skills) <= 30 else "\n - ..."))


# %% [cell 5]
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import defaultdict
import re
from sentence_transformers import SentenceTransformer

# Load a lightweight, high-quality model for text similarity
model_sim = SentenceTransformer('all-MiniLM-L6-v2')

# --------------------
# Helpers
# --------------------
def is_skill_like(text: str, max_tokens=6, max_chars=45):
    """
    Keep technical skill/tool-like phrases.
    Remove sentence fragments and obvious business / non-technical phrases.
    """
    if not text:
        return False

    t = str(text).strip().lower()
    t = " ".join(t.split())

    if len(t) > max_chars:
        return False
    if len(t.split()) > max_tokens:
        return False
    if len(t) < 2:
        return False

    # sentence / action fragments
    if re.search(r"\b(i|we|they|built|developed|implemented|responsible|manage|leading)\b", t):
        return False

    # obvious non-technical/business noise
    banned_phrases = {
        "branded customer service",
        "insurance industry",
        "digital strategy",
        "lead management",
        "computer science",
        "data-driven",
        "modern deployment tools"
    }
    if t in banned_phrases:
        return False

    # must contain at least one technical hint
    technical_hints = [
        "api", "aws", "gcp", "azure", "docker", "kubernetes", "linux", "bash", "shell",
        "python", "mysql", "postgresql", "mongodb", "mongo", "elasticsearch", "ecs",
        "iac", "terraform", "ansible", "ci/cd", "devops", "automation", "observability",
        "distributed", "multiten", "infrastructure", "database", "cloud", "scaling",
        "security", "script", "data warehouse", "metrics"
    ]

    if not any(h in t for h in technical_hints):
        return False

    return True


def normalize_skill(x: str) -> str:
    x = str(x).strip().lower()
    x = " ".join(x.split())
    return x


def clean_list(xs):
    """Deduplicate while keeping order."""
    out, seen = [], set()
    for x in xs:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def build_skill_candidates_from_jd(jd_data):
    """
    Read jd_data['jd_tech_skills'], normalize, filter, deduplicate.
    """
    raw = jd_data.get("jd_tech_skills", []) or []

    cleaned = []
    for x in raw:
        nx = normalize_skill(x)
        if is_skill_like(nx):
            cleaned.append(nx)

    return clean_list(cleaned)


def pick_k_silhouette(embeddings, k_min=2, k_max=10, random_state=42):
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


def cluster_skills_kmeans(skills, model_sim, k=None, k_min=2, k_max=10, random_state=42):
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


# --------------------
# Run clustering on extracted JD technical skills
# --------------------
skills_for_clustering = build_skill_candidates_from_jd(jd_data)

print("JD TECH skills to cluster:", len(skills_for_clustering))
for s in skills_for_clustering:
    print("-", s)

clustering_result = cluster_skills_kmeans(
    skills_for_clustering,
    model_sim,
    k=None,
    k_min=2,
    k_max=10
)

print("\nChosen K:", clustering_result["k"])
for cid, items in sorted(clustering_result["clusters"].items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\nCluster {cid} (size={len(items)}):")
    for s in items:
        print(" -", s)


# %% [cell 7]
# ==============================
# Install additional libraries needed for retrieval
# Run once
# ==============================

# ==============================
# Imports for retrieval / generation pipeline
# ==============================
import json
import numpy as np
import faiss
import torch
import pandas as pd
import re

from collections import defaultdict, Counter
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer

CACHE_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcq_generated_cache.json")
# %% [cell 8]
def load_all_datasets():
    """
    Load your MCQ dataset safely and convert it into a unified format
    for retrieval and generation.
    """
    unified = []

    file_path = r"E:\Opportune\Opportune\interview-preparation-openEndedQuestions\integration\test_dataset.csv"   # <-- CHANGE THIS

    # ======================================================
    # Load CSV safely
    # ======================================================
    print("📂 Loading Main MCQ Dataset...")

    try:
        df = pd.read_csv(
            file_path,
            engine="python",
            on_bad_lines="skip",
            encoding="utf-8",
            encoding_errors="ignore"
        )
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        raise

    print(f"   ✅ Loaded rows: {len(df)}")

    # ======================================================
    # Show columns + preview
    # ======================================================
    print("\n🧾 Columns:")
    print(df.columns.tolist())

    print("\n🔍 Sample rows:")
    print(df.head(2))

    # ======================================================
    # Convert to unified format
    # ======================================================
    for _, row in df.iterrows():
        question = str(row.get("question", "")).strip()
        if not question:
            continue

        item = {
            "skill": str(row.get("skill", "")).strip().lower(),
            "subskill": str(row.get("subskill", "")).strip().lower(),
            "question_type": str(row.get("question_type", "")).strip().lower(),
            "question": question,

            "option_a": str(row.get("option_a", "")).strip(),
            "option_b": str(row.get("option_b", "")).strip(),
            "option_c": str(row.get("option_c", "")).strip(),
            "option_d": str(row.get("option_d", "")).strip(),

            "correct_answer": str(row.get("correct_answer", "")).strip().lower(),
            "explanation": str(row.get("explanation", "")).strip(),

            "has_image": str(row.get("has_image", "")).strip().lower(),
            "image_url": str(row.get("image_url", "")).strip(),
            "image_alt_text": str(row.get("image_alt_text", "")).strip(),

            "question_number": str(row.get("question_number", "")).strip(),
            "topic": str(row.get("topic", "")).strip().lower(),
            "source_url": str(row.get("source_url", "")).strip(),

            "source": "dataset_main_mcq"
        }

        # light safety filter only
        if item["question_type"] != "mcq":
            continue
        if item["correct_answer"] not in {"a", "b", "c", "d"}:
            continue
        if not all([item["option_a"], item["option_b"], item["option_c"], item["option_d"]]):
            continue

        unified.append(item)

    print(f"\n   ✅ Processed valid questions: {len(unified)}")

    # ======================================================
    # Remove duplicate questions
    # ======================================================
    print("\n🔍 Removing duplicate questions...")
    before = len(unified)

    seen = set()
    deduped = []

    for r in unified:
        key = re.sub(r"[^\w\s]", "", r["question"].lower().strip())
        key = " ".join(key.split())

        if key not in seen:
            seen.add(key)
            deduped.append(r)

    after = len(deduped)
    print(f"   Removed {before - after} duplicate questions")

# Load generated cache
    # Replace is_valid_mcq(r) with the inline check:
    if os.path.exists(CACHE_JSON_PATH) and os.path.getsize(CACHE_JSON_PATH) > 0:
        print("📂 Loading Generated Cache...")
        try:
            with open(CACHE_JSON_PATH, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            before_cache = len(deduped)
            for r in cache_data:
                # inline validation instead of is_valid_mcq(r)
                if not str(r.get("question", "")).strip():
                    continue
                if str(r.get("correct_answer", "")).strip().lower() not in {"a", "b", "c", "d"}:
                    continue
                if not all([str(r.get("option_a", "")).strip(),
                            str(r.get("option_b", "")).strip(),
                            str(r.get("option_c", "")).strip(),
                            str(r.get("option_d", "")).strip()]):
                    continue
                key = re.sub(r"[^\w\s]", "", r["question"].lower().strip())
                key = " ".join(key.split())
                if key not in seen:
                    seen.add(key)
                    deduped.append(r)
            print(f"   ✅ {len(deduped) - before_cache} new cached records added")
        except Exception as e:
            print(f"⚠️ Cache load failed: {e}")

    # ======================================================
    # Final summary
    # ======================================================
    print(f"\n{'='*40}")
    print(f"📦 FINAL RECORDS: {after}")
    print(f"{'='*40}")

    return deduped


# Run
data = load_all_datasets()


# %% [cell 9]
from sentence_transformers import SentenceTransformer
import faiss

embedder = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Embedder loaded!")


# %% [cell 10]
print("🔄 Building FAISS index...")

corpus = []
metadata = []   # ← IMPORTANT

for record in data:
    text = f"{record.get('skill','')} {record.get('subskill','')} {record.get('topic','')} {record.get('question','')}".strip()

    corpus.append(text)
    metadata.append(record)   # ← store full record

# Generate embeddings
corpus_embeddings = embedder.encode(
    corpus,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

# Build FAISS index
dimension = corpus_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(corpus_embeddings)

print(f"✅ FAISS index ready with {index.ntotal} entries")


# %% [cell 11]
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Define device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load flan-t5-large as generator
gen_model_name = "google/flan-t5-large"
gen_tokenizer  = T5Tokenizer.from_pretrained(gen_model_name)
gen_model      = T5ForConditionalGeneration.from_pretrained(gen_model_name).to(device)
print("✅ flan-t5-large loaded!")


# %% [cell 12]
def extract_last_json_object(text: str):
    text = text.strip()

    # Try direct JSON first
    try:
        return json.loads(text)
    except:
        pass

    start_positions = [i for i, ch in enumerate(text) if ch == "{"]

    for start in reversed(start_positions):
        depth = 0
        in_string = False
        escape = False

        for i in range(start, len(text)):
            ch = text[i]

            if escape:
                escape = False
                continue

            if ch == "\\":
                escape = True
                continue

            if ch == '"':
                in_string = not in_string
                continue

            if not in_string:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        candidate = text[start:i+1]
                        try:
                            return json.loads(candidate)
                        except:
                            break

    raise ValueError("No valid JSON object found in model response.")


def repair_json_with_groq(raw_text, max_retries=1):
    for _ in range(max_retries):
        repair_prompt = f"""
Convert the following content into VALID JSON ONLY.

Required schema:
{{
  "option_a": "text",
  "option_b": "text",
  "option_c": "text",
  "option_d": "text",
  "correct_answer": "a",
  "explanation": "text"
}}

Rules:
- Return JSON only.
- No markdown fences.
- No code.
- No commentary.
- correct_answer must be exactly one of: "a", "b", "c", "d"

CONTENT:
{raw_text}
"""
        repaired = get_completion(repair_prompt, model="llama-3.1-8b-instant")
        try:
            return extract_last_json_object(repaired)
        except:
            continue

    raise ValueError("Could not repair malformed JSON.")


def generate_mcq_details_groq(question, skills, max_retries=4):
    skills_str = ", ".join(skills)

    for attempt in range(max_retries):
        prompt = f"""
You are creating a technical multiple-choice interview question.

Target skills: {skills_str}

Question:
{question}

Return ONLY valid JSON in exactly this format:
{{
  "option_a": "text",
  "option_b": "text",
  "option_c": "text",
  "option_d": "text",
  "correct_answer": "a",
  "explanation": "text"
}}

STRICT RULES:
- Output JSON ONLY.
- Do not use markdown fences.
- Do not output code or scripts.
- Do not explain your answer.
- Do not include labels like json, bash, python, or example.
- Escape all double quotes inside values.
- Exactly 4 options.
- Only ONE correct answer.
- correct_answer must be exactly one of: "a", "b", "c", "d"
- Keep explanation short and clear.
- Keep each option concise.
"""

        raw = get_completion(prompt, model="llama-3.1-8b-instant")

        try:
            parsed = extract_last_json_object(raw)
        except Exception:
            try:
                parsed = repair_json_with_groq(raw, max_retries=1)
            except Exception as e:
                if attempt == max_retries - 1:
                    print("⚠️ Raw Groq output that failed to parse:")
                    print(raw)
                    raise ValueError(f"Groq returned invalid JSON after {max_retries} attempts: {e}")
                continue

        result = {
            "option_a": str(parsed.get("option_a", "")).strip(),
            "option_b": str(parsed.get("option_b", "")).strip(),
            "option_c": str(parsed.get("option_c", "")).strip(),
            "option_d": str(parsed.get("option_d", "")).strip(),
            "correct_answer": str(parsed.get("correct_answer", "")).strip().lower(),
            "explanation": str(parsed.get("explanation", "")).strip(),
        }

        for key in ["option_a", "option_b", "option_c", "option_d"]:
            result[key] = re.sub(r"^[a-dA-D][\.\)]\s*", "", result[key]).strip()

        if (
            result["option_a"] and result["option_b"] and
            result["option_c"] and result["option_d"] and
            result["explanation"] and
            result["correct_answer"] in {"a", "b", "c", "d"}
        ):
            return result

    raise ValueError("Groq returned incomplete MCQ details after retries.")


# %% [cell 13]
required_vars = [
    "jd_tech_skills",
    "index",
    "metadata",
    "generate_mcq_details_groq",
    "get_completion"
]

for var in required_vars:
    print(f"{var}:", var in globals())


# %% [cell 14]
# ============================================================
# FINAL CELL 12: Question Generation Strategy
#   (a) Exact Matching
#   (b) FAISS Retrieval
#   (c) LLM Generation (Groq + T5)
# ============================================================

import re
from collections import defaultdict

TARGET_TOTAL_QUESTIONS = 10


def normalize_text_basic(x: str) -> str:
    x = str(x).strip().lower()
    x = re.sub(r"[^\w\s/+\-\.]", " ", x)
    x = " ".join(x.split())
    return x


def compute_questions_per_skill(skills, target_total=TARGET_TOTAL_QUESTIONS, max_per_skill=2):
    """
    Distribute a reasonable number of questions across skills.
    Capped to reduce duplicates for small JD skill sets.
    """
    skills = [s for s in skills if str(s).strip()]
    n = len(skills)

    if n == 0:
        return {}

    if n >= target_total:
        return {s: 1 for s in skills[:target_total]}

    base = max(1, target_total // n)
    extra = target_total % n

    allocation = {}
    for i, s in enumerate(skills):
        allocation[s] = min(max_per_skill, base + (1 if i < extra else 0))

    return allocation


def is_valid_mcq(record):
    if not str(record.get("question", "")).strip():
        return False

    if str(record.get("correct_answer", "")).strip().lower() not in {"a", "b", "c", "d"}:
        return False

    if not all([
        str(record.get("option_a", "")).strip(),
        str(record.get("option_b", "")).strip(),
        str(record.get("option_c", "")).strip(),
        str(record.get("option_d", "")).strip(),
    ]):
        return False

    return True


def record_search_text(record):
    parts = [
        record.get("skill", ""),
        record.get("subskill", ""),
        record.get("topic", ""),
        record.get("question", ""),
    ]
    return " | ".join(str(p) for p in parts if str(p).strip())


def exact_match_score(record, skill):
    """
    Exact/lexical matching should be the FIRST mechanism.
    Uses only generic text matching across metadata/question fields.
    """
    skill_text = normalize_text_basic(skill)

    record_skill = normalize_text_basic(record.get("skill", ""))
    record_subskill = normalize_text_basic(record.get("subskill", ""))
    record_topic = normalize_text_basic(record.get("topic", ""))
    record_question = normalize_text_basic(record.get("question", ""))

    score = 0.0

    # strongest signals
    if skill_text == record_skill:
        score += 5.0
    elif skill_text and skill_text in record_skill:
        score += 3.0

    if skill_text == record_subskill:
        score += 4.0
    elif skill_text and skill_text in record_subskill:
        score += 2.5

    if skill_text == record_topic:
        score += 3.5
    elif skill_text and skill_text in record_topic:
        score += 2.0

    # weak fallback signal
    if skill_text and skill_text in record_question:
        score += 0.8

    return score


def retrieve_exact_matches(skill, metadata, top_k=20):
    candidates = []

    for record in metadata:
        if not is_valid_mcq(record):
            continue

        score = exact_match_score(record, skill)
        if score > 0:
            candidates.append((score, record))

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[:top_k]


def retrieve_faiss_matches(skill, index, metadata, embedder, top_k=20):
    """
    FAISS is the SECOND mechanism after exact matching.
    """
    query = f"technical interview mcq about {skill}"
    query_emb = embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True)

    scores, indices = index.search(query_emb, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        record = metadata[idx]
        results.append((float(score), record))

    return results


def rerank_faiss_matches(skill, candidates, embedder):
    """
    Re-rank FAISS candidates using semantic similarity between:
    skill text and combined record text.
    """
    if not candidates:
        return []

    skill_emb = embedder.encode([skill], convert_to_numpy=True, normalize_embeddings=True)[0]
    texts = [record_search_text(r) for _, r in candidates]
    text_embs = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    reranked = []
    for (faiss_score, record), txt_emb in zip(candidates, text_embs):
        semantic_score = float(skill_emb @ txt_emb)

        combined_text = normalize_text_basic(record_search_text(record))
        lexical_bonus = 0.10 if normalize_text_basic(skill) in combined_text else 0.0

        final_score = (0.75 * semantic_score) + (0.25 * faiss_score) + lexical_bonus
        reranked.append((final_score, semantic_score, faiss_score, record))

    reranked.sort(key=lambda x: x[0], reverse=True)
    return reranked


def is_relevant_faiss_candidate(skill, record, semantic_score, min_semantic_score=0.30):
    """
    Keep FAISS generic but slightly filtered to reduce obvious noise.
    """
    combined_text = normalize_text_basic(record_search_text(record))
    skill_text = normalize_text_basic(skill)

    if semantic_score >= min_semantic_score:
        return True

    if semantic_score >= 0.24 and skill_text in combined_text:
        return True

    return False


def dedup_key(question_text: str) -> str:
    q = normalize_text_basic(question_text)
    q = q.replace("which of the following best describes", "")
    q = " ".join(q.split())
    return q


def clean_selected_record(record, target_skill, source_name):
    r = dict(record)
    r["source"] = source_name
    r["skill"] = target_skill
    r["skills"] = [target_skill]
    return r


def generate_mcq_fallback(skill):
    """
    LLM generation is the THIRD and last mechanism.
    """
    print(f"  🔄 Generating fallback MCQ for: {skill}")

    question = f"Which of the following best describes {skill}?"
    mcq = generate_mcq_details_groq(question, [skill])

    result = {
        "cluster_id": -1,
        "skills": [skill],
        "skill": skill,
        "subskill": skill,
        "question_type": "mcq",
        "question": question,
        "option_a": mcq["option_a"],
        "option_b": mcq["option_b"],
        "option_c": mcq["option_c"],
        "option_d": mcq["option_d"],
        "correct_answer": mcq["correct_answer"],
        "explanation": mcq["explanation"],
        "has_image": "no",
        "image_url": "",
        "image_alt_text": "",
        "question_number": "",
        "topic": skill,
        "source_url": "",
        "source": "generated_fallback"
    }
    
    save_to_cache(result)  
    return result

def save_to_cache(record: dict):
    try:
        # Save to disk
        try:
            with open(CACHE_JSON_PATH, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            cache = []

        # Deduplicate before saving
        existing_questions = {e.get("question", "").strip().lower() for e in cache}
        if record.get("question", "").strip().lower() not in existing_questions:
            cache.append(record)
            with open(CACHE_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)

            # Add to live metadata so current session can find it
            metadata.append(record)

            # Add to live FAISS index
            new_text = f"{record.get('skill','')} {record.get('subskill','')} {record.get('topic','')} {record.get('question','')}".strip()
            new_emb = embedder.encode([new_text], convert_to_numpy=True, normalize_embeddings=True)
            index.add(new_emb)

            print(f"✅ Cached + added to live index: {record.get('skill','')}")
        else:
            print(f"⚠️ Duplicate skipped in cache: {record.get('question','')[:60]}")

    except Exception as e:
        print(f"⚠️ Cache save failed: {e}")



def generate_questions_per_skill(skills, index, metadata, embedder):
    """
    Main strategy:
      1) Exact Matching
      2) FAISS Retrieval
      3) LLM Generation
    """
    allocation = compute_questions_per_skill(skills)

    all_results = []
    seen_questions = set()

    print("\n📊 Question allocation:")
    for k, v in allocation.items():
        print(f" - {k}: {v}")

    for skill, needed in allocation.items():
        print(f"\n📦 Skill: {skill} | Need: {needed}")

        selected = []

        # =====================================================
        # (a) EXACT MATCHING
        # =====================================================
        exact_candidates = retrieve_exact_matches(skill, metadata, top_k=20)

        for score, record in exact_candidates:
            q_text = str(record.get("question", "")).strip()
            q_key = dedup_key(q_text)

            if not q_text or q_key in seen_questions:
                continue

            selected_record = clean_selected_record(record, skill, "dataset_exact")
            selected.append(selected_record)
            seen_questions.add(q_key)

            print(f"  ✅ Exact match (score={score:.2f}): {q_text[:90]}")

            if len(selected) >= needed:
                break

        # =====================================================
        # (b) FAISS RETRIEVAL
        # =====================================================
        if len(selected) < needed:
            remaining = needed - len(selected)
            print(f"  🔎 Need {remaining} more → trying FAISS")

            faiss_candidates = retrieve_faiss_matches(skill, index, metadata, embedder, top_k=25)
            reranked_faiss = rerank_faiss_matches(skill, faiss_candidates, embedder)

            for final_score, semantic_score, faiss_score, record in reranked_faiss:
                if not is_valid_mcq(record):
                    continue

                if not is_relevant_faiss_candidate(skill, record, semantic_score):
                    continue

                q_text = str(record.get("question", "")).strip()
                q_key = dedup_key(q_text)

                if not q_text or q_key in seen_questions:
                    continue

                selected_record = clean_selected_record(record, skill, "dataset_faiss")
                selected.append(selected_record)
                seen_questions.add(q_key)

                print(
                    f"  📚 FAISS match (final={final_score:.3f}, semantic={semantic_score:.3f}, faiss={faiss_score:.3f}): "
                    f"{q_text[:90]}"
                )

                if len(selected) >= needed:
                    break

        # =====================================================
        # (c) LLM GENERATION
        # =====================================================
        fallback_attempts = 0
        max_fallback_attempts = 2

        while len(selected) < needed and fallback_attempts < max_fallback_attempts:
            fallback_attempts += 1
            fallback = generate_mcq_fallback(skill)

            q_text = str(fallback["question"]).strip()
            q_key = dedup_key(q_text)

            if not q_text or q_key in seen_questions:
                break

            selected.append(fallback)
            seen_questions.add(q_key)

        all_results.extend(selected)

    return all_results


# ============================================================
# RUN PIPELINE
# ============================================================

all_questions = generate_questions_per_skill(
    jd_tech_skills,
    index,
    metadata,
    embedder
)

# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 60)
print("📋 FINAL MCQ QUESTIONS (SKILL-BASED)")
print("=" * 60)

for r in all_questions:
    print(f"\n🔹 Skill: {r['skill']}")
    print(f"   📚 Source: {r['source']}")
    print(f"   Q: {r['question']}")
    print(f"   A) {r['option_a']}")
    print(f"   B) {r['option_b']}")
    print(f"   C) {r['option_c']}")
    print(f"   D) {r['option_d']}")
    print(f"   Correct Answer: {r['correct_answer']}")
    print(f"   Explanation: {r['explanation']}")
    print("-" * 60)


# %% [cell 17]
# ==============================
# Install
# ==============================

# ==============================
# Imports
# ==============================

import uuid
import tempfile
import os
import threading
import time
import nest_asyncio
nest_asyncio.apply()

import uvicorn

from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pyngrok import ngrok


# %% [cell 18]

# ==============================
# SET YOUR NGROK TOKEN
# ==============================
NGROK_TOKEN = os.getenv("NGROK_TOKEN", "3BvkWzFSIfJZ68jStIIGNDFutBM_2EvpRkJxwcAjJfVFYKCkY")

# ==============================
# In-memory session store
# ==============================
SESSIONS: Dict[str, Dict] = {}

# ==============================
# FastAPI app
# ==============================
app = FastAPI(title="Interview Preparation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Request Models
# ==============================
class GenerateQuestionsRequest(BaseModel):
    job_description: str = Field(..., min_length=10)

class AnswerItem(BaseModel):
    question_id: str
    user_answer: str

class EvaluateAnswersRequest(BaseModel):
    session_id: str
    answers: List[AnswerItem]

# ==============================
# Helper: root
# ==============================
@app.get("/")
async def root():
    return {
        "message": "Interview Preparation API is running",
        "docs": "/docs",
        "health": "/health"
    }

# ==============================
# Health
# ==============================
@app.get("/health")
async def health():
    return {"status": "running"}

# ==============================
# Helper: extract skills from raw text
# ==============================
def extract_skills_from_text(job_description_text: str):
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8"
    ) as tmp:
        tmp.write(job_description_text)
        tmp_path = tmp.name

    try:
        result = parse_jd_tech_skills_with_llm(tmp_path)

        if "error" in result:
            raise ValueError(result["error"])

        skills = result.get("jd_tech_skills", [])

        cleaned = []
        seen = set()

        for s in skills:
            if isinstance(s, str):
                s = s.strip()
                if s and s.lower() not in seen:
                    seen.add(s.lower())
                    cleaned.append(s)

        return cleaned

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

# ==============================
# Helper: normalize question text
# ==============================
def normalize_question_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(str(text).strip().lower().split())

# ==============================
# Helper: safely get skill from generated row
# ==============================
def get_skill_from_question_obj(q: dict):
    if q.get("skill"):
        return q["skill"]

    if q.get("skills") and isinstance(q["skills"], list) and len(q["skills"]) > 0:
        return q["skills"][0]

    return None

# ==============================
# Generate Questions
# ==============================
@app.post("/generate-questions")
async def generate_questions(request: GenerateQuestionsRequest):
    try:
        # 1) Extract JD skills
        skills = extract_skills_from_text(request.job_description)

        if not skills:
            raise HTTPException(status_code=400, detail="No skills could be extracted from the job description")

        # 2) Generate questions per skill
        generated_questions = generate_questions_per_skill(
            skills,
            index,
            metadata,
            embedder
        )

        if not generated_questions:
            raise HTTPException(status_code=500, detail="No questions were generated")

        # 3) Deduplicate + limit
        # Adjust this number if you want more/fewer questions per skill
        MAX_QUESTIONS_PER_SKILL = 2

        public_questions = []
        answer_key = {}

        seen_questions = set()
        per_skill_count = defaultdict(int)

        for q in generated_questions:
            question_text = (q.get("question") or "").strip()
            skill_name = get_skill_from_question_obj(q)

            if not question_text or not skill_name:
                continue

            normalized_q = normalize_question_text(question_text)

            # skip duplicates
            if normalized_q in seen_questions:
                continue

            # limit number per skill
            if per_skill_count[skill_name.lower()] >= MAX_QUESTIONS_PER_SKILL:
                continue

            seen_questions.add(normalized_q)
            per_skill_count[skill_name.lower()] += 1

            qid = str(uuid.uuid4())

            public_questions.append({
                "question_id": qid,
                "skill": skill_name,
                "question": question_text,
                "option_a": q.get("option_a"),
                "option_b": q.get("option_b"),
                "option_c": q.get("option_c"),
                "option_d": q.get("option_d"),
            })

            answer_key[qid] = {
                "skill": skill_name,
                "question": question_text,
                "correct_answer": q.get("correct_answer"),
            }

        if not public_questions:
            raise HTTPException(status_code=500, detail="Questions were generated, but all were filtered out as duplicates/invalid")

        session_id = str(uuid.uuid4())

        SESSIONS[session_id] = {
            "job_description": request.job_description,
            "skills": skills,
            "answer_key": answer_key
        }

        return {
            "status": "questions_ready",
            "session_id": session_id,
            "skills": skills,
            "questions": public_questions
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================
# Evaluate Answers
# ==============================
@app.post("/evaluate-answers")
async def evaluate_answers(request: EvaluateAnswersRequest):
    try:
        if request.session_id not in SESSIONS:
            raise HTTPException(status_code=404, detail="Invalid session_id")

        session = SESSIONS[request.session_id]
        answer_key = session["answer_key"]

        results = []

        for item in request.answers:
            if item.question_id not in answer_key:
                continue

            ref = answer_key[item.question_id]

            scores = compute_hybrid_score(
                item.user_answer,
                ref["correct_answer"],
                ref["question"]
            )

            grade = get_grade(scores["hybrid_score"])

            results.append({
                "question_id": item.question_id,
                "skill": ref["skill"],
                "question": ref["question"],
                "user_answer": item.user_answer,
                "correct_answer": ref["correct_answer"],
                "grade": grade,
                **scores
            })

        if not results:
            raise HTTPException(status_code=400, detail="No valid answers were submitted")

        # optional summary by skill
        skill_groups = defaultdict(list)
        for r in results:
            skill_groups[r["skill"]].append(r)

        skill_summary = {}
        all_scores = []

        for skill, items in skill_groups.items():
            avg_score = round(sum(x["hybrid_score"] for x in items) / len(items), 3)
            all_scores.append(avg_score)

            skill_summary[skill] = {
                "skill": skill,
                "avg_score": avg_score,
                "grade": get_grade(avg_score),
                "num_questions": len(items)
            }

        overall_score = round(sum(all_scores) / len(all_scores), 3) if all_scores else 0.0
        overall_grade = get_grade(overall_score)

        return {
            "status": "report_ready",
            "overall_score": overall_score,
            "overall_grade": overall_grade,
            "skill_summary": skill_summary,
            "question_results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================
# Start server
# ==============================
def start_server():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())
# ==============================
# Start ngrok
# ==============================
def start_ngrok(port=8000):
    ngrok.kill()
    time.sleep(2)

    if not NGROK_TOKEN or NGROK_TOKEN == "PUT_YOUR_REAL_NGROK_TOKEN_HERE":
        raise Exception("Please set your real ngrok token first")

    ngrok.set_auth_token(NGROK_TOKEN)
    tunnel = ngrok.connect(port)
    return tunnel.public_url

# ==============================
# Launch API
# ==============================
# ==============================
# Launch API
# ==============================
if __name__ == "__main__":
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()

    time.sleep(5)

    public_url = start_ngrok(8000)

    print("=" * 60)
    print(f"✅ API URL: {public_url}")
    print(f"📖 Docs: {public_url}/docs")
    print("=" * 60)

    while True:
        time.sleep(1)