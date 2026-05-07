"""ATS keyword scoring for resume-job matching."""

import re
from dataclasses import dataclass
from src.utils import clean_text, extract_sections

# Common technical action verbs
TECH_ACTION_VERBS = {
    "developed", "built", "designed", "implemented", "architected",
    "optimised", "automated", "deployed", "integrated", "led",
    "managed", "created", "improved", "reduced", "increased",
    "delivered", "launched", "collaborated", "analysed", "researched",
    "maintained", "migrated", "refactored", "tested", "documented",
}

REQUIRED_SECTIONS = {"experience", "education", "skills"}


@dataclass
class ATSResult:
    """ATS scoring results with detailed feedback."""
    score: int
    matched_keywords: list[str]
    missing_keywords: list[str]
    section_scores: dict[str, int]
    action_verb_count: int
    word_count: int
    feedback: list[str]


def _tokenize(text: str) -> set[str]:
    """Extract unique words from text, lowercase and cleaned."""
    words = re.findall(r"[a-z][a-z0-9\+\#\.]*", text.lower())
    return set(words)


def _extract_keywords(job_text: str, top_n: int = 40) -> list[str]:
    """Extract meaningful keywords from job description."""
    stopwords = {
        "the", "and", "or", "a", "an", "in", "on", "at", "to", "for",
        "of", "is", "are", "will", "be", "with", "we", "you", "your",
        "our", "this", "that", "have", "has", "not", "as", "by", "from",
        "their", "which", "can", "may", "should", "must", "able", "work",
        "team", "position", "role", "company", "experience", "skills",
        "years", "working", "including", "such", "who",
    }
    words = re.findall(r"[a-z][a-z0-9\+\#\.]*", job_text.lower())
    freq: dict[str, int] = {}
    for w in words:
        if w not in stopwords and len(w) > 2:
            freq[w] = freq.get(w, 0) + 1
    # Sort by frequency, return top_n
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:top_n]]


def score_resume(resume_text: str, job_description: str) -> ATSResult:
    """Score resume against job description (0-100 scale)."""
    resume_clean = clean_text(resume_text).lower()
    jd_clean = clean_text(job_description).lower()

    resume_tokens = _tokenize(resume_clean)
    jd_keywords = _extract_keywords(jd_clean, top_n=40)

    # Keyword matching (50 pts)
    matched = [kw for kw in jd_keywords if kw in resume_tokens]
    missing = [kw for kw in jd_keywords if kw not in resume_tokens]
    keyword_score = int((len(matched) / max(len(jd_keywords), 1)) * 50)

    # Section completeness (20 pts)
    sections_found = extract_sections(resume_text)
    found_lower = {k.lower() for k in sections_found}
    section_hit = sum(
        1 for s in REQUIRED_SECTIONS
        if any(s in f for f in found_lower)
    )
    section_score = int((section_hit / len(REQUIRED_SECTIONS)) * 20)

    section_scores = {
        s.title(): (10 if any(s in f for f in found_lower) else 0)
        for s in REQUIRED_SECTIONS
    }

    # Action verb density (15 pts)
    resume_words = resume_clean.split()
    verb_count = sum(1 for w in resume_words if w in TECH_ACTION_VERBS)
    action_score = min(15, int((verb_count / max(len(resume_words), 1)) * 1500))

    # Length score (15 pts)
    wc = len(resume_words)
    if wc >= 400:
        length_score = 15
    elif wc >= 250:
        length_score = 10
    elif wc >= 100:
        length_score = 5
    else:
        length_score = 2

    total_score = keyword_score + section_score + action_score + length_score
    total_score = max(0, min(100, total_score))

    # Generate feedback
    feedback: list[str] = []
    if keyword_score < 25:
        feedback.append("⚠️  Add more keywords from the job description to improve ATS matching.")
    if section_score < 15:
        feedback.append("⚠️  Ensure your resume has clear EXPERIENCE, EDUCATION, and SKILLS sections.")
    if verb_count < 5:
        feedback.append("⚠️  Use more action verbs (e.g., Developed, Led, Optimised) to strengthen bullets.")
    if wc < 250:
        feedback.append("⚠️  Your resume is too short. Aim for 300–600 words for better ATS parsing.")
    if not missing:
        feedback.append("✅  Great keyword coverage! Your resume aligns well with the job description.")
    elif len(missing) <= 10:
        feedback.append(f"✅  Good match! Consider adding: {', '.join(missing[:5])}.")

    return ATSResult(
        score=total_score,
        matched_keywords=matched,
        missing_keywords=missing[:15],
        section_scores=section_scores,
        action_verb_count=verb_count,
        word_count=wc,
        feedback=feedback,
    )
