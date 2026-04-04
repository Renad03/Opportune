from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import ssl

uri = "neo4j://26fec051.databases.neo4j.io"  # your Neo4j URI
user = "26fec051"                                # your Neo4j username
password = "k9Fi0AQp81rctWyKOa8reWgYayH-LaK-BOcr-K2Qn60"  # your password
# Create an SSL context that ignores certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

driver = GraphDatabase.driver(
    uri,
    auth=(user, password),
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