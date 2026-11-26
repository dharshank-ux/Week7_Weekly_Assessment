import hashlib
import uuid
from pathlib import Path

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = BASE_DIR / "Task1" / "documents"
DB_DIR = BASE_DIR / "Task1" / "qdrant_db"

COLLECTION_NAME = "company_policies"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

# Connect to local Qdrant database
client = QdrantClient(path=str(DB_DIR))

# Create collection if it does not exist
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE
        )
    )

def get_department(filename):
    name = filename.lower()

    if "leave" in name or "attendance" in name:
        return "HR"
    elif "salary" in name:
        return "Finance"
    elif "security" in name:
        return "IT"
    elif "travel" in name or "expense" in name:
        return "Finance"
    else:
        return "General"

def load_and_chunk():
    chunks = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")

        print(f"Loading: {file_path.name}")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for page, line in enumerate(lines[1:], start=1):
            if len(line) < 10:
                continue

            chunks.append({
                "text": line,
                "source": file_path.name,
                "page": 1,
                "department": get_department(file_path.name),
                "year": 2026
            })

    return chunks

def stable_id(chunk):
    unique_text = (
        chunk["source"] + "|" +
        str(chunk["page"]) + "|" +
        chunk["text"]
    )

    return str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_text))

def index_documents():
    chunks = load_and_chunk()

    print(f"\nTotal chunks: {len(chunks)}")
    print("Generating embeddings...")

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts).tolist()

    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            models.PointStruct(
                id=stable_id(chunk),
                vector=embedding,
                payload=chunk
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True
    )

    info = client.get_collection(COLLECTION_NAME)

    print("\nINDEXING COMPLETED")
    print("===================")
    print(f"Documents: {len(list(DOCUMENTS_DIR.glob('*.txt')))}")
    print(f"Chunks processed: {len(chunks)}")
    print(f"Vectors stored: {info.points_count}")
    print("Stable IDs: Enabled")
    print("Metadata: Enabled")

if __name__ == "__main__":
    index_documents()
    client.close()