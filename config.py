from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH        = BASE_DIR / "fine_tuned_model (2)"
DATASET_PATH      = BASE_DIR / "Coursera.csv"
EMBEDDINGS_PATH   = BASE_DIR / "skill_embeddings.npy"
COURSE_INDEX_PATH = BASE_DIR / "flat_course_idx.npy"
FLAT_SKILLS_PATH  = BASE_DIR / "flat_skills.npy"

MIN_SIMILARITY    = 0.50
DEFAULT_TOP_K     = 5