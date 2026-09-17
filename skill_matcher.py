# -*- coding: utf-8 -*-
"""NLP utilities for skill recommendation and resume/job matching."""

import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("skills_dataset.csv")
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["job_title"].fillna(""))


def _normalise_skill(skill):
    return re.sub(r"\s+", " ", str(skill).strip().lower())


def suggest_skills(job_title, user_skills):
    """Suggest skills associated with the most similar job title."""
    if not job_title:
        return []

    user_vec = vectorizer.transform([job_title])
    similarities = cosine_similarity(user_vec, tfidf_matrix)
    best_index = similarities.argmax()
    best_score = similarities.max()

    if best_score < 0.2:
        return []

    matched_job = df.iloc[best_index]
    skills = [s.strip() for s in str(matched_job["skills"]).split(",") if s.strip()]
    existing = {_normalise_skill(s) for s in user_skills}
    return [s for s in skills if _normalise_skill(s) not in existing]


def match_resume_to_job(resume_text, job_description, user_skills=None):
    """Return an interpretable TF-IDF/cosine-similarity job match.

    This is deliberately lightweight: no neural network or external model is
    required. It also reports keyword coverage using the project's skills CSV.
    """
    resume_text = str(resume_text or "").strip()
    job_description = str(job_description or "").strip()
    user_skills = user_skills or []

    if not job_description:
        return {"match_score": None, "matched_skills": [], "missing_skills": []}

    texts = [resume_text, job_description]
    matcher = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = matcher.fit_transform(texts)
    similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])

    # Extract skills from the project's existing skill dataset.
    all_skills = []
    for value in df["skills"].dropna():
        all_skills.extend(s.strip() for s in str(value).split(",") if s.strip())

    unique_skills = {}
    for skill in all_skills:
        unique_skills.setdefault(_normalise_skill(skill), skill)

    combined_resume = " " + resume_text.lower() + " " + " ".join(map(str, user_skills)).lower() + " "
    combined_job = job_description.lower()

    job_skills = [display for key, display in unique_skills.items()
                  if re.search(r"(?<!\w)" + re.escape(key) + r"(?!\w)", combined_job)]
    matched = [skill for skill in job_skills
               if re.search(r"(?<!\w)" + re.escape(_normalise_skill(skill)) + r"(?!\w)", combined_resume)]
    missing = [skill for skill in job_skills if skill not in matched]

    return {
        "match_score": round(similarity * 100, 1),
        "matched_skills": matched[:12],
        "missing_skills": missing[:12],
    }
