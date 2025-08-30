Recruitment AI Agent 🚀
📌 Overview

This project is an AI-powered recruitment assistant that automates the candidate shortlisting process for recruiters.
It uses Groq’s LLM API for intelligence, LangGraph to manage multi-agent workflows, and a scheduler to run automatically every hour.

Instead of recruiters manually going through resumes, the AI agent fetches, processes, and filters candidates based on the job description (JD) and sends the recruiter an update.

⚙️ Features

🤖 Multi-Agent Workflow using LangGraph:

JD Parsing Agent → Extracts key requirements from the job description.

Resume Screening Agent → Compares resumes with the parsed JD.

Matching Agent → Scores candidates based on relevance.

Notifier Agent → Sends shortlisted candidates to the recruiter.

🔄 Automated Scheduling → Runs every hour.

⚡ LLM-Powered Matching → Uses Groq API for fast and accurate resume–JD matching.

📬 Recruiter Notification → Recruiter receives results via email/Slack/console log.

🛠️ Tech Stack

Groq API → LLM inference (fast processing of text).

LangGraph → Multi-agent workflow orchestration.

Python → Core development.

Scheduler → Cron/schedule library for automation.

📂 Project Pipeline

Input: Recruiter provides a Job Description (JD).

Resume Fetching: (Can be extended) – Currently resumes are fed locally (PDF/JSON), later can be fetched via LinkedIn, Naukri, Indeed, etc.

JD Parsing Agent: Extracts key requirements (skills, experience, role).

Resume Screening Agent: Reads resumes and extracts candidate data.

Matching Agent: Compares resume data with JD and assigns a match score.

Notifier Agent: Sends top matches to recruiter.

Scheduler: Repeats process every hour automatically.
