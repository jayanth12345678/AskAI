import faiss
import numpy as np
from app.services.embedding_service import embeddings

EMBEDDING_DIMENSION = 384

index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)

stored_chunks = []


def add_chunks(chunks: list[str], vectors: list[list[float]]) -> None:
    vector_array = np.array(vectors, dtype=np.float32)

    index.add(vector_array)

    stored_chunks.extend(chunks)


def search_chunks(query: str, k: int = 3) -> list[dict]:
    query_vector = embeddings.embed_query(query)

    query_array = np.array([query_vector], dtype=np.float32)

    scores, positions = index.search(query_array, k)

    results = []

    for score, position in zip(scores[0], positions[0]):
        if position == -1:
            continue

        results.append({
            "position": int(position),
            "score": float(score),
            "text": stored_chunks[position]
        })

    return results



def reset_vector_store() -> None:
    index.reset()
    stored_chunks.clear()   
