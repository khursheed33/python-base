from neo4j import GraphDatabase
from transformers import AutoTokenizer, AutoModel
import torch
import uuid


# Initialize the Neo4j driver
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(user, password))

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def generate_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().tolist()
    return embeddings

def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def create_user(tx, user_id, user_name):
    query = "CREATE (u:User {id: $user_id, name: $user_name})"
    tx.run(query, user_id=user_id, user_name=user_name)

def create_chunk(tx, chunk):
    query = """
    MATCH (u:User {id: $user_id})
    CREATE (c:Chunk {id: $chunk_id, name: $name, embeddings: $embeddings, text: $text, file_id: $file_id, user_id: $user_id})
    CREATE (u)-[:HAS_CHUNK]->(c)
    """
    tx.run(query, chunk_id=chunk['id'], name=chunk['name'], embeddings=chunk['embeddings'], text=chunk['text'], file_id=chunk['file_id'], user_id=chunk['user_id'])

def store_chunks(user_id, user_name, text, file_id, chunk_size=512, overlap=50):
    chunks = chunk_text(text, chunk_size, overlap)
    with driver.session() as session:
        session.write_transaction(create_user, user_id, user_name)
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            chunk_name = f"Chunk {i+1}"
            embeddings = generate_embeddings(chunk)
            chunk_data = {
                'id': chunk_id,
                'name': chunk_name,
                'embeddings': embeddings,
                'text': chunk,
                'file_id': file_id,
                'user_id': user_id
            }
            session.write_transaction(create_chunk, chunk_data)

def find_similar_chunks(query_text, top_k=5):
    query_embeddings = generate_embeddings(query_text)
    with driver.session() as session:
        result = session.run("MATCH (c:Chunk) RETURN c.id AS id, c.embeddings AS embeddings, c.text AS text")

        chunks = []
        for record in result:
            chunk_embeddings = record["embeddings"]
            similarity = torch.nn.functional.cosine_similarity(
                torch.tensor(query_embeddings).unsqueeze(0),
                torch.tensor(chunk_embeddings).unsqueeze(0)
            ).item()
            chunks.append((record["id"], record["text"], similarity))

        chunks.sort(key=lambda x: x[2], reverse=True)
        return chunks[:top_k]

# Example usage:
user_id = str(uuid.uuid4())
user_name = "John Doe"
file_id = str(uuid.uuid4())
text = """
Virat Kohli is an Indian cricketer and former captain of the Indian national team. Known for his aggressive batting style and exceptional leadership, Kohli is considered one of the best batsmen in the world. He has numerous records to his name, including the fastest century in One Day Internationals (ODIs) and the highest number of centuries in T20 Internationals. Kohli's dedication to fitness and consistency has earned him accolades both on and off the field. Beyond cricket, he is a successful entrepreneur, running a fashion brand and owning a stake in several business ventures.
"""

store_chunks(user_id, user_name, text, file_id, chunk_size=100, overlap=20)

query_text = "Who is known for being the former captain of the Indian national cricket team?"
similar_chunks = find_similar_chunks(query_text)
print("Chunks: ",similar_chunks)