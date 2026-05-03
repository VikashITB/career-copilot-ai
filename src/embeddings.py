"""
embeddings.py – FAISS vector index creation and similarity search.

Uses sentence-transformers (all-MiniLM-L6-v2) to embed text,
then stores/searches via FAISS (CPU).
"""

import os
import pickle
import numpy as np
from typing import Optional
from src.utils import get_env, truncate

# Lazy imports to keep startup fast
_embedder = None
_faiss = None


# ── Embedding model ────────────────────────────────────────────────────────────

def _get_embedder():
    """Lazily load the SentenceTransformer model."""
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        model_name = get_env("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        _embedder = SentenceTransformer(model_name)
    return _embedder


def _get_faiss():
    """Lazily import faiss."""
    global _faiss
    if _faiss is None:
        import faiss
        _faiss = faiss
    return _faiss


def embed_text(text: str) -> np.ndarray:
    """
    Embed a single text string into a float32 numpy vector.
    The vector is L2-normalised for cosine similarity via FAISS IndexFlatIP.
    """
    embedder = _get_embedder()
    text = truncate(text, max_chars=2000)
    vector = embedder.encode([text], normalize_embeddings=True)
    return vector.astype(np.float32)


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed multiple texts and return a (N, D) float32 array."""
    embedder = _get_embedder()
    texts = [truncate(t, 2000) for t in texts]
    vectors = embedder.encode(texts, normalize_embeddings=True, batch_size=32)
    return vectors.astype(np.float32)


# ── FAISS index management ─────────────────────────────────────────────────────

VECTORSTORE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "vectorstore",
)
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "jobs.index")
META_PATH  = os.path.join(VECTORSTORE_DIR, "jobs_meta.pkl")


def build_index(job_texts: list[str], job_names: list[str]) -> None:
    """
    Build a FAISS IndexFlatIP (inner product = cosine for normalised vectors)
    from *job_texts* and persist it to disk.

    Parameters
    ----------
    job_texts : list[str]
        Raw job description strings.
    job_names : list[str]
        Corresponding job title / identifier strings.
    """
    faiss = _get_faiss()
    vectors = embed_texts(job_texts)
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump({"names": job_names, "texts": job_texts}, f)


def load_index():
    """Load the persisted FAISS index and metadata. Returns (index, meta_dict)."""
    faiss = _get_faiss()
    if not os.path.exists(INDEX_PATH):
        return None, None
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)
    return index, meta


def search_jobs(resume_text: str, top_k: int = 5) -> list[dict]:
    """
    Search the FAISS index for jobs most similar to *resume_text*.

    Returns a list of dicts:
      [{"name": str, "text": str, "score": float (0–1)}, ...]
    sorted by descending similarity.
    """
    index, meta = load_index()
    if index is None:
        return []

    query_vec = embed_text(resume_text)
    distances, indices = index.search(query_vec, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        results.append(
            {
                "name": meta["names"][idx],
                "text": meta["texts"][idx],
                "score": float(dist),   # cosine similarity (0–1 range for normalised)
            }
        )
    return results


def index_exists() -> bool:
    """Return True if a built FAISS index is present on disk."""
    return os.path.exists(INDEX_PATH) and os.path.exists(META_PATH)
