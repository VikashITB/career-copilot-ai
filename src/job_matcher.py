"""
job_matcher.py – Orchestrates FAISS similarity search + LLM explanation
                 to produce ranked job match results for a given resume.
"""

from dataclasses import dataclass, field
from src.embeddings import search_jobs, build_index, index_exists
from src.rag_chain import job_match_chain
from src.utils import load_job_files, truncate


@dataclass
class JobMatch:
    job_name: str
    job_text: str
    similarity: float        # 0.0 – 1.0
    match_percent: int       # similarity * 100 rounded
    explanation: str = ""


# ── Index management ───────────────────────────────────────────────────────────

def ensure_index_built() -> None:
    """Build the FAISS index from data/jobs/*.txt if not already present."""
    if index_exists():
        return
    jobs = load_job_files()
    if not jobs:
        return
    build_index(list(jobs.values()), list(jobs.keys()))


# ── Matching ───────────────────────────────────────────────────────────────────

def match_jobs(resume_text: str, top_k: int = 5, explain: bool = True) -> list[JobMatch]:
    """
    Match *resume_text* against indexed job descriptions.

    Parameters
    ----------
    resume_text : str
        Full resume text.
    top_k : int
        Number of top matches to return.
    explain : bool
        If True, call the LLM to generate a fit explanation per match.

    Returns
    -------
    list[JobMatch]
        Ranked list of job matches, best first.
    """
    ensure_index_built()
    raw_results = search_jobs(resume_text, top_k=top_k)

    matches: list[JobMatch] = []
    chain = job_match_chain() if explain else None

    for result in raw_results:
        sim = max(0.0, min(1.0, result["score"]))   # clamp to [0, 1]
        match_pct = int(sim * 100)

        explanation = ""
        if explain and chain is not None:
            try:
                explanation = chain.invoke(
                    {
                        "resume_snippet": truncate(resume_text, 600),
                        "job_description": truncate(result["text"], 600),
                        "similarity_score": sim,
                    }
                )
            except Exception as exc:
                explanation = f"(Explanation unavailable: {exc})"

        matches.append(
            JobMatch(
                job_name=result["name"],
                job_text=result["text"],
                similarity=sim,
                match_percent=match_pct,
                explanation=explanation,
            )
        )

    return sorted(matches, key=lambda m: m.similarity, reverse=True)


def add_custom_job(name: str, description: str) -> None:
    """
    Add a single custom job description to the FAISS index at runtime.
    This rebuilds the index with the new job appended.
    """
    from src.embeddings import load_index, embed_texts, VECTORSTORE_DIR, INDEX_PATH, META_PATH
    import pickle, os, faiss

    index, meta = load_index()
    if index is None:
        build_index([description], [name])
        return

    names = meta["names"] + [name]
    texts = meta["texts"] + [description]
    build_index(texts, names)
