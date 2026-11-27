
import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from qdrant_client import QdrantClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env", override=True)

url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_API_KEY")

if not url:
    raise ValueError("QDRANT_URL is missing")

if not api_key:
    raise ValueError("QDRANT_API_KEY is missing")

parsed = urlparse(url)

print("URL scheme:", parsed.scheme)
print("URL host:", parsed.hostname)
print("API key configured:", bool(api_key))

client = None

try:
    print("\nConnecting to Qdrant...")

    client = QdrantClient(
        url=url,
        api_key=api_key,
        timeout=20,
    )

    collections = client.get_collections()

    print("\nSUCCESS: Qdrant connection established!")

    for collection in collections.collections:
        print("-", collection.name)

except Exception as e:
    print("\nCONNECTION FAILED")
    print("Error type:", type(e).__name__)
    print("Error:", str(e))

finally:
    if client:
        client.close()
