import streamlit as st
import PyPDF2
import re
import pandas as pd

st.set_page_config(page_title="Offline Resume Analyzer", page_icon="📄")
st.title("📄 Offline Resume Analyzer")
st.markdown("Upload your resume (PDF), and get basic feedback — no internet or API required!")

tech_df = pd.read_csv("/home/hazar/Downloads/tech_skill.csv")
soft_df = pd.read_csv("/home/hazar/Downloads/soft_skills.csv")

TECH_SKILLS = tech_df['tech_skill'].str.lower().tolist()
SOFT_SKILLS = soft_df['soft_skill'].str.lower().tolist()
REQUIRED_SECTIONS = ["experience", "education", "skills", "projects", "contact", "certifications"]

def find_skills(skills_list, text):
    found = []
    for skill in skills_list:
        if re.search(rf'\b{re.escape(skill)}\b', text, re.I):
            found.append(skill)
    return found

def match_percentage(resume_skills, jd_skills):
    if not jd_skills:
        return 100, set(), set()
    matched = set(resume_skills).intersection(set(jd_skills))
    percent = len(matched) / len(jd_skills) * 100
    return round(percent, 1), matched, set(jd_skills) - matched

uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    resume_text = ""
    for page in pdf_reader.pages:
        try:
            resume_text += page.extract_text() or ""
        except Exception:
            continue

    if not resume_text.strip():
        st.warning("⚠️ No text extracted from PDF. Try another file.")
    else:
        resume_text_lower = resume_text.lower()

        st.subheader("📄 Extracted Resume Text")
        st.text_area("Resume Preview", resume_text[:2000], height=300)

        st.subheader("🧠 Automated Feedback")

        st.markdown("### 📌 Section Check:")
        for section in REQUIRED_SECTIONS:
            if section in resume_text_lower:
                st.success(f"✅ Found section: {section.title()}")
            else:
                st.warning(f"❌ Missing section: {section.title()}")

        soft_matches = find_skills(SOFT_SKILLS, resume_text_lower)
        tech_matches = find_skills(TECH_SKILLS, resume_text_lower)

        st.markdown(f"### 😊 Soft Skills Found ({len(soft_matches)}): {', '.join(soft_matches) if soft_matches else 'None'}")
        st.markdown(f"### 💻 Technical Skills Found ({len(tech_matches)}): {', '.join(tech_matches) if tech_matches else 'None'}")

        words = re.findall(r"\w+", resume_text)
        word_count = len(words)
        st.markdown(f"### 🔢 Word Count: {word_count} words")

        st.markdown("### 📝 Suggestions:")
        if word_count < 300:
            st.info("📌 Consider adding more detail to your resume.")
        if "github" not in resume_text_lower and "portfolio" not in resume_text_lower:
            st.info("🔗 Include a link to your GitHub or portfolio if applicable.")
        if len(tech_matches) < 3:
            st.info("💻 Try to showcase more technical skills relevant to your field.")


        st.markdown("---")
        st.header("📋 Job Description Matching")

        jd_file = st.file_uploader("Upload Job Description (txt or pdf)", type=["txt", "pdf"], key="jd_file")
        job_description = ""

        if jd_file:
            if jd_file.type == "application/pdf":
                jd_reader = PyPDF2.PdfReader(jd_file)
                jd_text = ""
                for page in jd_reader.pages:
                    jd_text += page.extract_text() or ""
                job_description = jd_text
            else:
                job_description = jd_file.read().decode('utf-8')
        else:
            job_description = st.text_area("Or paste the Job Description here:")

        if job_description.strip():
            jd_lower = job_description.lower()

            jd_tech_skills = [skill for skill in TECH_SKILLS if re.search(rf'\b{re.escape(skill)}\b', jd_lower, re.I)]
            jd_soft_skills = [skill for skill in SOFT_SKILLS if re.search(rf'\b{re.escape(skill)}\b', jd_lower, re.I)]

            tech_match_percent, matched_tech, missing_tech = match_percentage(tech_matches, jd_tech_skills)
            soft_match_percent, matched_soft, missing_soft = match_percentage(soft_matches, jd_soft_skills)

            st.markdown(f"### 📊 Technical Skills Match: {tech_match_percent}%")
            if missing_tech:
                st.markdown(f"**Missing Technical Skills:** {', '.join(missing_tech)}")

            st.markdown(f"### 📊 Soft Skills Match: {soft_match_percent}%")
            if missing_soft:
                st.markdown(f"**Missing Soft Skills:** {', '.join(missing_soft)}")

            overall_match = round((tech_match_percent + soft_match_percent) / 2, 1)
            st.markdown(f"### 🎯 Overall Skills Match Score: {overall_match}%")
