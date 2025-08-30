
import os
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

def fallback_keyword_extractor(jd_text):
    """
    Very simple heuristic extractor for skills/titles/keywords:
    - picks capitalized words and common skill tokens
    - returns unique normalized keywords
    """
    tokens = re.findall(r"[A-Za-z\+\#\.\-]{2,}", jd_text)
    stops = {"with","and","in","for","the","years","yrs","experience","exp","job","role","skills","skill","based","at","location","prefer"}
    tokens = [t.strip() for t in tokens if t.lower() not in stops]
    # heuristics: include tokens with uppercase or common skill words
    common_skills = {"java","python","spring","django","flask","microservices","aws","docker","kubernetes","react","node","sql","nosql","j2ee","springboot","spring-boot"}
    out = []
    for t in tokens:
        tl = t.lower()
        if t[0].isupper() or tl in common_skills or len(tl)>3:
            out.append(t)
    # de-dup preserving order
    seen = set()
    result = []
    for k in out:
        kk = k.lower()
        if kk not in seen:
            seen.add(kk)
            result.append(k)
    # produce aliases for some entries
    synonyms = {}
    for k in result:
        kl = k.lower()
        if kl == "spring":
            synonyms.setdefault(k, []).append("spring boot")
        if kl == "java":
            synonyms.setdefault(k, []).append("j2ee")
    return {
        "keywords": result,
        "synonyms": synonyms
    }

def extract_keywords(jd_text):
    """
    Try Groq LLM if configured, otherwise fallback to the simple extractor.
    When using Groq, we expect the model to return a short CSV or JSON-like list.
    """
    if GROQ_API_KEY:
        try:
            # Try to call groq if available
            import groq
            client = groq.Client(api_key=GROQ_API_KEY)
            prompt = (
                "Extract a short comma-separated list of primary skills, role titles, synonyms, "
                "and related tags from this job description. Output only a JSON with keys: keywords, synonyms.\n\n"
                f"JOB DESCRIPTION:\n{jd_text}\n\n"
                "Example output:\n{\"keywords\": [\"Java\",\"Spring Boot\",\"Microservices\"], \"synonyms\": {\"Java\": [\"J2EE\"]}}"
            )
            # Some groq SDKs expose chat.completions; adapt if needed
            try:
                resp = client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[{"role":"user","content":prompt}],
                    max_tokens=300
                )
                raw = resp.choices[0].message.content
            except Exception:
                # older/newer APIs may differ
                raw = client.completions.create(prompt=prompt, max_tokens=300).choices[0].text
            # crude attempt to parse JSON from model output
            import json
            # strip leading/trailing content
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1:
                json_text = raw[start:end+1]
                parsed = json.loads(json_text)
                return parsed
        except Exception as e:
            print("Groq extraction failed or groq sdk unavailable — using fallback. Error:", e)

    # fallback
    return fallback_keyword_extractor(jd_text)

def generate_boolean_string(keywords, role=None, location=None, experience=None):
    """
    Construct a simple boolean string using keywords + optional role/location.
    """
    if not keywords:
        return ""
    # create OR blocks; treat titles separately if first keyword looks like a title
    # we will simply OR the keywords and join with AND for role/location
    or_block = " OR ".join([f'"{k}"' if " " in k else k for k in keywords[:6]])
    parts = [f"({or_block})"]
    if role:
        parts.append(f'("{role}" OR {role})')
    if location:
        parts.append(location)
    if experience:
        parts.append(f'("{experience} years" OR "{experience} yrs" OR {experience})')
    boolean = " AND ".join(parts)
    # basic cleanup
    return boolean

def generate_xray_templates(boolean_str):
    """
    Provide X-Ray templates for Naukri, LinkedIn and Google.
    """
    templates = {
        "Naukri": f'site:naukri.com/resume {boolean_str}',
        "LinkedIn": f'site:linkedin.com/in {boolean_str}',
        "Google": f'site:google.com "resume" {boolean_str}'
    }
    return templates
