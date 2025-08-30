# mock_data.py
import random

SAMPLE_POOL = [
    {"name": "Ankit Sharma", "skills": ["Java", "Spring Boot", "SQL"], "exp": 4, "location": "Bangalore"},
    {"name": "Priya Verma", "skills": ["Java", "Microservices", "Docker"], "exp": 5, "location": "Bangalore"},
    {"name": "Rahul Gupta", "skills": ["Python", "Django", "Postgres"], "exp": 3, "location": "Hyderabad"},
    {"name": "Sneha Joshi", "skills": ["Java", "Spring", "Kubernetes"], "exp": 6, "location": "Pune"},
    {"name": "Neha Singh", "skills": ["JavaScript", "React", "Node"], "exp": 4, "location": "Bangalore"},
]

def score_candidate(candidate, keywords, role=None, location=None):
    """
    Simple match scoring:
      - +30 if candidate has any exact keyword in skills
      - +10 per matching skill (up to 40)
      - +10 if location matches
      - +5 per year of experience up to 25
    Normalize to 0-100.
    """
    score = 0
    cand_skills = set([s.lower() for s in candidate.get("skills", [])])
    kw = [k.lower() for k in keywords]
    # any exact keyword
    if any(k in cand_skills for k in kw):
        score += 30
    # per skill match
    matches = sum(1 for k in kw if k in cand_skills)
    score += min(matches * 10, 40)
    # location
    if location and candidate.get("location") and location.lower() in candidate.get("location","").lower():
        score += 10
    # experience
    exp = candidate.get("exp", 0)
    score += min(exp * 5, 25)
    # random small noise
    score += random.randint(-3, 3)
    return max(0, min(100, score))

def fetch_mock_candidates(n=5, keywords=None, role=None, location=None):
    # pick some from SAMPLE_POOL and score them
    chosen = SAMPLE_POOL[:]
    random.shuffle(chosen)
    chosen = chosen[:n]
    results = []
    for c in chosen:
        sc = score_candidate(c, keywords or [], role=role, location=location)
        results.append({
            "name": c["name"],
            "skills": c["skills"],
            "exp": c["exp"],
            "location": c.get("location", ""),
            "match": sc
        })
    # sort by match desc
    results.sort(key=lambda x: x["match"], reverse=True)
    return results
