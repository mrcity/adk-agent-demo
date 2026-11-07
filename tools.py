import os
import json
from google.cloud import firestore
from google.genai import Client
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
genai_client = Client(vertexai=True, project=PROJECT_ID, location="us-central1")

# --- TOOL 1: Local JSON (Phase 1) ---
def get_local_menu() -> str:
    """Returns the entire menu catalog, prices, and allergen notes."""
    with open("menu.json", "r") as f:
        return f.read()

# --- TOOL 2: Firestore Vector Search (Phase 2) ---
def search_menu_vector(query: str) -> str:
    """Finds matching coffee, beans, or pastries in Firestore using Vector ANN search."""
    db = firestore.Client(project=PROJECT_ID, database="coffee-menu")
    collection_ref = db.collection("menu")

    # Generate query embedding
    emb = genai_client.models.embed_content(
        model="text-embedding-005",
        contents=query
    )
    query_vector = emb.embeddings[0].values

    # Query nearest neighbors
    search = collection_ref.find_nearest(
        vector_field="embedding",
        query_vector=Vector(query_vector),
        distance_measure=DistanceMeasure.COSINE,
        limit=2
    )

    results = []
    for doc in search.stream():
        d = doc.to_dict()
        d.pop("embedding", None)  # Strip raw vectors to save prompt context
        results.append(d)

    return json.dumps(results)
