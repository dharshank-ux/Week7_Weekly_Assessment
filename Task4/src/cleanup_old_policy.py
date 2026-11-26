from pathlib import Path
from qdrant_client import QdrantClient, models

ROOT = Path(__file__).resolve().parents[2]
DB_DIR = ROOT / "Task1" / "qdrant_db"

client = QdrantClient(path=str(DB_DIR))

COLLECTION_NAME = "company_policies"

# Find only outdated policy records
client.delete(
    collection_name=COLLECTION_NAME,
    points_selector=models.FilterSelector(
        filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="source",
                    match=models.MatchValue(
                        value="old_leave_policy.txt"
                    )
                )
            ]
        )
    )
)

print("Old policy records cleanup completed!")

client.close()