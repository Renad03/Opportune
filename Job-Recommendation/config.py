from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import ssl

URI = "neo4j://be29599c.databases.neo4j.io"
AUTH = ("be29599c", "Vvmm49Tbvs4_zdwXjvEA2-W_-0_Baw6sA__AgZdsL3g") # your password
# Create an SSL context that ignores certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

driver = GraphDatabase.driver(
    URI,
    auth=AUTH,
    ssl_context=ssl_context  # only needed if ignoring SSL
)

# Sentence transformer
encoder = SentenceTransformer("all-MiniLM-L6-v2", device='cpu')

# Experience mapping
experience_map = {
    "intern": 0,
    "fresher": 1,
    "junior": 2,
    "mid": 3,
    "senior": 4,
    "lead": 5,
    "unspecified": 0
}