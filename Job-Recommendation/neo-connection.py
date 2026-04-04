import ssl
from neo4j import GraphDatabase


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
try:
    with driver.session() as session:
        result = session.run("RETURN 1 AS test")
        for record in result:
            print("Connection successful! Test query returned:", record["test"])
finally:
    driver.close()