# Opportune 🚀

**Opportune** is an AI-powered career recommendation platform that matches job seekers and students with personalized job and course recommendations based on their skills and experience level.

## 📌 Overview

Opportune combines machine learning, graph neural networks (HGT), and semantic search to deliver intelligent career guidance. The platform consists of three main components:

1. **Job Recommendation** - Recommends jobs based on user skills and experience using HGT (Heterogeneous Graph Transformer)
2. **Course Recommendation** - Suggests relevant Coursera courses to fill skill gaps
3. **Data Parsing** - Extracts and parses job descriptions and other career-related data

---

## 🗂️ Project Structure

```
Opportune/
├── Job-Recommendation/          # HGT-based job recommendation API
│   ├── main.py                  # FastAPI app & routes
│   ├── model.py                 # HGT model & predictor classes
│   ├── graph.py                 # Neo4j graph builder
│   ├── recommend.py             # Recommendation logic
│   ├── config.py                # Configuration settings
│   ├── export_checkpoint.py     # Model export utility
│   ├── final_model.pt           # Trained model weights
│   └── requirements.txt
│
├── Course-Recommendation/       # Coursera course recommendation API
│   ├── main.py                  # FastAPI app & routes
│   ├── recommend.py             # Course matching logic
│   ├── build_embeddings.py      # Embedding generation
│   ├── config.py                # Configuration settings
│   └── requirements.txt
│
├── JD-Preprocessing/            # Job description preprocessing
├── JS-Preprocessing/            # Job seeker profile preprocessing
├── Parsing-Notebook/            # Data parsing utilities
│   ├── OpportuneParsing.py      # Parsing logic
│   ├── main.py                  # Parsing API
│   ├── requirements.txt
│   └── DockerFile
│
└── interview-preparation-openEndedQuestions/  # Interview prep resources
```

---

## 🎯 Key Features

### Job Recommendation
- **Graph Neural Network** - Uses Heterogeneous Graph Transformer (HGT) to understand relationships between users, jobs, and skills
- **Experience-Aware** - Matches users to roles appropriate for their experience level (intern, fresher, junior, mid, senior, lead)
- **Skill Matching** - Identifies matched and unmatched skills with detailed feedback
- **REST API** - FastAPI-based endpoints for easy integration

### Course Recommendation
- **Semantic Search** - Uses sentence transformers for intelligent skill-to-course matching
- **Skill Gap Analysis** - Recommends courses to fill gaps identified from job descriptions
- **Experience-Level Filtering** - Tailors course difficulty to user level
- **Multi-Skill Recommendations** - Suggests multiple courses for comprehensive skill development

### Data Processing
- Job description parsing and extraction
- Job seeker profile preprocessing
- Docker-based deployment for scalability

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Neo4j database (for Job Recommendation)
- pip or conda

### Installation

#### 1. Job Recommendation API

```bash
cd Job-Recommendation

# Copy and configure environment
cp .env.example .env
# Edit .env with your Neo4j credentials and model settings

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Interactive Docs**: http://localhost:8000/docs

#### 2. Course Recommendation API

```bash
cd Course-Recommendation

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload --host 0.0.0.0 --port 8004
```

**Interactive Docs**: http://localhost:8004/docs

---

## 📚 API Endpoints

### Job Recommendation API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Liveness check |
| GET | `/skills` | List all available skills |
| GET | `/experience-levels` | List valid experience levels |
| POST | `/recommend` | Get job recommendations |

**Example Request:**
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "Docker", "FastAPI", "AWS", "Pandas"],
    "experience": "senior",
    "top_k": 5
  }'
```

**Example Response:**
```json
{
  "recommendations": [
    {
      "job_title": "Data Engineer",
      "recommended_skills": ["Python", "AWS", "Airflow", "Pandas", "Docker"],
      "contributing_skills": ["python", "aws", "pandas", "docker"],
      "final_score": 1.3842
    }
  ],
  "matched_skills": ["Python", "Docker", "AWS", "Pandas"],
  "unmatched_skills": ["FastAPI"]
}
```

### Course Recommendation API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Liveness check |
| POST | `/recommend` | Get course recommendations |

**Example Request:**
```bash
curl -X POST http://localhost:8004/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "missing_skills": ["Machine Learning", "Data Analysis"],
    "experience_level": "intermediate",
    "top_k": 10,
    "courses_per_skill": 5
  }'
```

---

## 🏗️ Architecture

### Job Recommendation Architecture
- **Graph Database**: Neo4j stores relationships between users, jobs, skills, and companies
- **GNN Model**: HGT (Heterogeneous Graph Transformer) learns embeddings from the graph
- **Inference**: FastAPI loads the model at startup and serves recommendations

### Course Recommendation Architecture
- **Embeddings**: Pre-computed semantic embeddings of courses and skills using Sentence Transformers
- **Matching**: Finds courses with similar skill embeddings to user's missing skills
- **Ranking**: Ranks courses by relevance and filters by experience level

---

## 🔧 Configuration

### Job Recommendation (.env.example)
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
CHECKPOINT_PATH=./final_model.pt
HIDDEN_DIM=256
NUM_LAYERS=2
DROPOUT=0.1
DEVICE=cuda  # or cpu
```

### Course Recommendation (config.py)
```python
MODEL_PATH = Path("path/to/sentence-transformer-model")
DATASET_PATH = Path("path/to/courses.csv")
EMBEDDINGS_PATH = Path("path/to/embeddings.npy")
DEFAULT_TOP_K = 10
```

---

## 📊 Data Requirements

### For Job Recommendation
- Neo4j graph with nodes: `User`, `Job`, `Skill`, `Company`, `Location`
- Trained HGT model checkpoint (`final_model.pt`)
- Experience levels and job categories

### For Course Recommendation
- CSV dataset of courses with columns: `Course Name`, `Skills`, `Difficulty Level`, `Platform`
- Pre-computed embeddings for all courses and skills
- Coursera course metadata

---

## 🤖 ML Models Used

- **HGT (Heterogeneous Graph Transformer)** - For job recommendations, learns from graph structure
- **Sentence Transformers** - For semantic similarity in course recommendations
- **Embedding-based Retrieval** - For efficient course-to-skill matching

---

## 🐳 Docker Deployment

For the Parsing-Notebook component:

```bash
cd Parsing-Notebook
docker build -t opportune-parsing .
docker run -p 8080:8080 opportune-parsing
```

---

## 📝 Model Training & Export

### Exporting a Trained Job Recommendation Model

After training in your notebook (e.g., Colab):

```python
import torch

# Your trained model and predictor
with torch.no_grad():
    _out = model(hetero_graph.x_dict, hetero_graph.edge_index_dict)

embed_dim = _out["JobSeeker"].shape[1]

torch.save(
    {
        "model_state_dict": model.state_dict(),
        "predictor_state_dict": predictor.state_dict(),
        "embed_dim": embed_dim,
        "best_val_score": best_val_score,
    },
    "final_model.pt",
)
```

Place `final_model.pt` in the `Job-Recommendation/` directory.

---

## ⚙️ Performance & Scalability

- **Startup Time**: ~30 seconds (graph initialization + model loading)
- **Per-Request Latency**: ~50-200ms depending on graph size
- **Concurrency**: For production use with high concurrency, implement request-level graph locking or cloning
- **Memory**: Typical production setup requires 4GB+ RAM for graph + model

---

## 🛠️ Troubleshooting

### torch-geometric Installation Issues
```bash
# For specific CUDA versions, see:
pip install torch-geometric==2.x.x -f https://data.pyg.org/whl/torch-2.x.x+cu118.html
```

### Neo4j Connection Errors
- Ensure Neo4j is running and accessible at the URI in `.env`
- Verify credentials and bolt protocol is enabled

### Model Not Found
- Verify `CHECKPOINT_PATH` in `.env` points to `final_model.pt`
- Ensure the checkpoint was exported correctly from training

---

## 👥 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## 📄 License

This project is open source. Check the repository for license details.

---

## 🔗 Related Projects

- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/) - GNN library
- [Neo4j Python Driver](https://neo4j.com/docs/drivers-manuals/python/) - Graph database
- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [Sentence Transformers](https://www.sbert.net/) - Semantic embeddings

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ by the Opportune team**
