# main.py
"""
Core workflow orchestrator.
Tries to use langgraph if available; otherwise runs a simple pipeline.
"""

import os
from utils import extract_keywords, generate_boolean_string, generate_xray_templates
from mock_data import fetch_mock_candidates

def pipeline_run(job_description, role=None, experience=None, location=None):
    """
    Runs the pipeline:
      1. keyword extraction (Groq if configured, fallback otherwise)
      2. boolean & x-ray generation
      3. mock candidate fetch & scoring
    Returns a dict with keys:
      - keywords, synonyms, boolean_query, xray_queries, candidates
    """
    # 1) extract keywords
    extracted = extract_keywords(job_description)
    keywords = extracted.get("keywords", [])
    synonyms = extracted.get("synonyms", {})

    # 2) generate boolean & xray
    boolean_query = generate_boolean_string(keywords, role=role, location=location, experience=experience)
    xray = generate_xray_templates(boolean_query)

    # 3) fetch mock candidates
    candidates = fetch_mock_candidates(n=6, keywords=keywords, role=role, location=location)

    return {
        "keywords": keywords,
        "synonyms": synonyms,
        "boolean_query": boolean_query,
        "xray_queries": xray,
        "candidates": candidates,
    }

# Small wrapper so other code can import a single callable
def workflow_invoke(initial_state):
    """
    initial_state: dict that can contain:
      - job_description (required)
      - role, experience, location (optional)
    """
    jd = initial_state.get("job_description", "") or ""
    role = initial_state.get("role")
    exp = initial_state.get("experience")
    loc = initial_state.get("location")
    return pipeline_run(jd, role=role, experience=exp, location=loc)

# If run as script, simple demo
if __name__ == "__main__":
    jd = "Hiring Java Developer with 3-5 yrs experience in Bangalore. Skills: Java, Spring Boot, Microservices, Docker"
    res = workflow_invoke({"job_description": jd, "role": "Java Developer", "experience": "3-5", "location": "Bangalore"})
    import json
    print(json.dumps(res, indent=2))
