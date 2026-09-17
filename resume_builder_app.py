import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "https://ai-resume-builder-umwu.onrender.com/generate"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0e0e10;
    color: #e8e6df;
}
section[data-testid="stSidebar"] {
    background: #18181b;
    border-right: 1px solid #2a2a2e;
    padding-top: 2rem;
}
section[data-testid="stSidebar"] * { color: #e8e6df !important; }
h1, h2, h3 { font-family: 'DM Serif Display', serif !important; letter-spacing: -0.02em; }
h1 { font-size: 2.6rem !important; color: #f5c842 !important; }
h2 { font-size: 1.5rem !important; color: #f5c842 !important; margin-top: 0.4rem !important; }
h3 { font-size: 1.15rem !important; color: #c9c4bb !important; }
input, textarea, select {
    background-color: #1e1e22 !important;
    border: 1px solid #35353b !important;
    border-radius: 6px !important;
    color: #e8e6df !important;
    font-family: 'DM Sans', sans-serif !important;
}
input:focus, textarea:focus { border-color: #f5c842 !important; box-shadow: 0 0 0 2px rgba(245,200,66,0.15) !important; }
label { color: #9e9b93 !important; font-size: 0.82rem !important; font-weight: 500 !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; }
.stButton > button {
    background: #f5c842 !important;
    color: #0e0e10 !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s;
    letter-spacing: 0.02em;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stDownloadButton > button {
    background: #1e1e22 !important;
    color: #f5c842 !important;
    border: 1px solid #f5c842 !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stDownloadButton > button:hover { background: #f5c842 !important; color: #0e0e10 !important; }
.section-card {
    background: #18181b;
    border: 1px solid #2a2a2e;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.4rem;
}
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 0.5rem; }
.chip {
    background: rgba(245,200,66,0.12);
    border: 1px solid rgba(245,200,66,0.35);
    color: #f5c842;
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.82rem;
    font-weight: 500;
    font-family: 'DM Sans', sans-serif;
}
.result-box {
    background: #1e1e22;
    border-left: 3px solid #f5c842;
    border-radius: 0 8px 8px 0;
    padding: 1.1rem 1.3rem;
    font-size: 0.96rem;
    line-height: 1.7;
    color: #d4d0c8;
    white-space: pre-wrap;
    margin-bottom: 1rem;
}
hr { border-color: #2a2a2e !important; }
.step-badge {
    display: inline-block;
    background: #f5c842;
    color: #0e0e10;
    border-radius: 4px;
    padding: 1px 8px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.6rem;
}
div[data-testid="stSpinner"] { color: #f5c842 !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📄 AI Resume Builder")
    st.markdown("---")
    st.markdown("""
**How it works**

1. Fill in your details across each section  
2. Click **Generate Resume**  
3. Download your polished PDF or DOCX  
""")
    st.markdown("---")
    page = st.radio("Navigate to", ["✏️ Build Resume", "⚙️ Settings"], label_visibility="collapsed")
    st.markdown("---")
    st.caption("Powered by AI · v1.0")


# ── Settings ───────────────────────────────────────────────────────────────
if page == "⚙️ Settings":
    st.markdown("# ⚙️ Settings")
    st.markdown("Configure connection to the backend.")
    BACKEND_URL = st.text_input("Backend URL", value=BACKEND_URL)
    st.info("Update this URL to match your running Flask backend.")
    st.stop()


# ── Main ───────────────────────────────────────────────────────────────────
st.markdown("# AI Resume Builder")
st.markdown("### Fill in the sections below and let AI craft your resume.")
st.markdown("---")

# Step 1 — Personal Info
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="step-badge">Step 1</div>', unsafe_allow_html=True)
st.markdown("## Personal Information")
col1, col2 = st.columns(2)
with col1:
    full_name = st.text_input("Full Name", placeholder="Jane Doe")
    email     = st.text_input("Email", placeholder="jane@email.com")
with col2:
    phone    = st.text_input("Phone", placeholder="+1 555 000 0000")
    linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/janedoe")
target_role = st.text_input("🎯 Job Title / Target Role", placeholder="e.g. Senior Product Manager")
st.markdown('</div>', unsafe_allow_html=True)

# Step 2 — Education
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="step-badge">Step 2</div>', unsafe_allow_html=True)
st.markdown("## Education")
col1, col2, col3 = st.columns([2, 2, 1])
with col1: degree      = st.text_input("Degree", placeholder="B.Sc. Computer Science")
with col2: institution = st.text_input("Institution", placeholder="MIT")
with col3: grad_year   = st.text_input("Year", placeholder="2021")
st.markdown('</div>', unsafe_allow_html=True)

# Step 3 — Experience
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="step-badge">Step 3</div>', unsafe_allow_html=True)
st.markdown("## Work Experience")
if "experiences" not in st.session_state:
    st.session_state.experiences = [{"company": "", "role": "", "duration": "", "description": ""}]
for i, exp in enumerate(st.session_state.experiences):
    with st.expander(f"Experience #{i+1} — {exp['company'] or 'New Entry'}", expanded=(i == 0)):
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1: st.session_state.experiences[i]["company"]  = st.text_input("Company",  value=exp["company"],  key=f"co_{i}", placeholder="Acme Corp")
        with c2: st.session_state.experiences[i]["role"]     = st.text_input("Role",     value=exp["role"],     key=f"ro_{i}", placeholder="Software Engineer")
        with c3: st.session_state.experiences[i]["duration"] = st.text_input("Duration", value=exp["duration"], key=f"du_{i}", placeholder="2020–2023")
        st.session_state.experiences[i]["description"] = st.text_area("Description", value=exp["description"], key=f"de_{i}", placeholder="Describe your responsibilities…", height=100)
col_add, col_remove = st.columns([1, 5])
with col_add:
    if st.button("＋ Add Role"):
        st.session_state.experiences.append({"company": "", "role": "", "duration": "", "description": ""})
        st.rerun()
with col_remove:
    if len(st.session_state.experiences) > 1 and st.button("− Remove Last"):
        st.session_state.experiences.pop()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Step 4 — Skills
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="step-badge">Step 4</div>', unsafe_allow_html=True)
st.markdown("## Skills")
skills_input = st.text_input("Skills (comma-separated)", placeholder="Python, React, SQL…")
st.markdown('</div>', unsafe_allow_html=True)

# Step 5 — Projects
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="step-badge">Step 5</div>', unsafe_allow_html=True)
st.markdown("## Projects")
if "projects" not in st.session_state:
    st.session_state.projects = [{"title": "", "description": ""}]
for i, proj in enumerate(st.session_state.projects):
    with st.expander(f"Project #{i+1} — {proj['title'] or 'New Project'}", expanded=(i == 0)):
        st.session_state.projects[i]["title"]       = st.text_input("Title",       value=proj["title"],       key=f"pt_{i}", placeholder="Portfolio Website")
        st.session_state.projects[i]["description"] = st.text_area("Description", value=proj["description"], key=f"pd_{i}", placeholder="Briefly describe the project…", height=80)
col_p1, col_p2 = st.columns([1, 5])
with col_p1:
    if st.button("＋ Add Project"):
        st.session_state.projects.append({"title": "", "description": ""})
        st.rerun()
with col_p2:
    if len(st.session_state.projects) > 1 and st.button("− Remove Last Project"):
        st.session_state.projects.pop()
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Step 6 — Certifications
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="step-badge">Step 6 · Optional</div>', unsafe_allow_html=True)
st.markdown("## Certifications")
certifications = st.text_area("List certifications (one per line)", placeholder="AWS Certified Solutions Architect\nGoogle Data Analytics Certificate", height=90)
st.markdown('</div>', unsafe_allow_html=True)


# ── Optional NLP job matching ───────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🎯 Job Description Matching")
job_description = st.text_area(
    "Paste the job description (optional)",
    placeholder="Paste the job description here to get an NLP-based resume match and missing-skill analysis…",
    height=140,
    help="Uses TF-IDF and cosine similarity to compare your resume content with the job description."
)

# ── Generate ───────────────────────────────────────────────────────────────
st.markdown("---")
col_btn, col_tip = st.columns([1, 3])
with col_btn:
    generate = st.button("✨ Generate Resume", use_container_width=True)
with col_tip:
    st.caption("Processing usually takes 10–20 seconds.")

if generate:
    payload = {
        "personal": {
            "full_name":   full_name,
            "email":       email,
            "phone":       phone,
            "linkedin":    linkedin,
            "target_role": target_role,
        },
        "education": {
            "degree":      degree,
            "institution": institution,
            "year":        grad_year,
        },
        "experience":     st.session_state.experiences,
        "skills":         [s.strip() for s in skills_input.split(",") if s.strip()],
        "projects":       st.session_state.projects,
        "certifications": [c.strip() for c in certifications.splitlines() if c.strip()],
        "job_description": job_description,
    }

    required = [full_name, email, target_role, degree, institution]
    if not all(required):
        st.error("⚠️ Please fill in at least: Full Name, Email, Target Role, Degree, and Institution.")
        st.stop()

    with st.spinner("🤖 AI is crafting your resume…"):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Could not connect to backend at `{BACKEND_URL}`. Is the server running?")
            st.stop()
        except requests.exceptions.Timeout:
            st.error("⏱️ The backend took too long to respond. Try again.")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()

    st.markdown("---")
    st.markdown("# ✅ Resume Generated!")

    suggested = result.get("suggested_skills", [])
    if suggested:
        st.markdown("## 💡 Suggested Skills to Add")
        chips_html = '<div class="chip-row">' + "".join(f'<span class="chip">{s}</span>' for s in suggested) + '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("")

    job_match = result.get("job_match", {})
    if job_description and job_match.get("match_score") is not None:
        st.markdown("## 🎯 NLP Job Match")
        st.metric("Resume ↔ Job Description Match", f"{job_match['match_score']}%")

        matched = job_match.get("matched_skills", [])
        missing = job_match.get("missing_skills", [])
        if matched:
            st.markdown("**Matched skills:** " + ", ".join(matched))
        if missing:
            st.markdown("**Skills found in the job description but not detected in your resume:** " + ", ".join(missing))

    summary = result.get("resume_summary", "")
    if summary:
        st.markdown("## 📝 AI-Generated Summary")
        st.markdown(f'<div class="result-box">{summary}</div>', unsafe_allow_html=True)

    st.markdown("## 📥 Download Your Resume")
    dl1, dl2, dl3 = st.columns(3)

    with dl1:
        pdf_b64 = result.get("download_pdf", "")
        if pdf_b64:
            st.download_button(
                label="⬇️ Download PDF",
                data=base64.b64decode(pdf_b64),
                file_name=f"{full_name.replace(' ', '_')}_Resume.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Standard PDF generated with ReportLab",
            )
        else:
            st.info("PDF not available.")

    with dl2:
        docx_b64 = result.get("download_docx", "")
        if docx_b64:
            st.download_button(
                label="⬇️ Download DOCX",
                data=base64.b64decode(docx_b64),
                file_name=f"{full_name.replace(' ', '_')}_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                help="Editable Word document",
            )
        else:
            st.info("DOCX not available.")

    with dl3:
        latex_b64 = result.get("download_latex_pdf", "")
        if latex_b64:
            st.download_button(
                label="⬇️ Download LaTeX PDF",
                data=base64.b64decode(latex_b64),
                file_name=f"{full_name.replace(' ', '_')}_Resume_LaTeX.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Polished PDF compiled from LaTeX",
            )
        else:
            st.info("LaTeX PDF not available.")

    with st.expander("🔍 Raw API Response (debug)"):
        st.json(result)
