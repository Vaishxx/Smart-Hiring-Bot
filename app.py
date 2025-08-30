# app.py
import streamlit as st
from main import workflow_invoke
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Smart Hiring Bot", layout="wide")

st.title("Smart Hiring Bot — Boolean & X-Ray Generator + Mock Search")
st.markdown("Enter a Job Description and get copy-paste ready Boolean/X-Ray strings and mock candidate results.")

with st.form("job_form"):
    jd = st.text_area("Paste Job Description (or type JD):", height=180)
    col1, col2, col3 = st.columns(3)
    role = col1.text_input("Role (optional)")
    experience = col2.text_input("Experience (e.g., 3-5 years) (optional)")
    location = col3.text_input("Location (optional)")
    submitted = st.form_submit_button("Generate")

if submitted:
    if not jd.strip():
        st.error("Please enter a job description.")
    else:
        result = workflow_invoke({
            "job_description": jd,
            "role": role or None,
            "experience": experience or None,
            "location": location or None
        })

        st.subheader("🔍 Extracted Keywords & Synonyms")
        cols = st.columns(2)
        cols[0].write("**Keywords**")
        cols[0].write(result.get("keywords", []))
        cols[1].write("**Synonyms / Related**")
        syn = result.get("synonyms", {})
        if syn:
            for k, v in syn.items():
                cols[1].write(f"- **{k}** → {v}")
        else:
            cols[1].write("No synonyms suggested (fallback extractor).")

        st.subheader("💬 Boolean Search String")
        st.code(result.get("boolean_query",""), language="text")
        st.button("Copy Boolean")  # streamlit copy button not built-in; user can copy from code block

        st.subheader("🌐 X-Ray Query Templates (copy-paste ready)")
        for site, q in result.get("xray_queries", {}).items():
            with st.expander(site):
                st.code(q, language="text")

        st.subheader("👥 Mock Candidate Matches")
        candidates = result.get("candidates", [])
        if candidates:
            for c in candidates:
                st.markdown(f"**{c['name']}** — {c['skills']} — {c['exp']} yrs — {c['location']}")
                st.progress(int(c['match']))
                cols2 = st.columns([1,1,1])
                if cols2[0].button(f"Shortlist {c['name']}", key=f"sl_{c['name']}"):
                    st.success(f"Shortlisted {c['name']}")
                if cols2[1].button(f"View {c['name']}", key=f"v_{c['name']}"):
                    st.info(f"Details: Skills: {c['skills']}, Experience: {c['exp']} yrs, Match: {c['match']}%")
                cols2[2].button(f"Export {c['name']}", key=f"e_{c['name']}")
        else:
            st.write("No candidates found (mock).")

        st.markdown("---")
        st.caption("This is a prototype. Replace mock candidate fetch with real search + parsing for production.")
