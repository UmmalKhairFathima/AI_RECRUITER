import io
import re
from typing import Dict, List


DEFAULT_SKILLS = {
    "python", "java", "javascript", "typescript", "react", "react native", "android",
    "kotlin", "fastapi", "django", "flask", "sql", "mongodb", "firebase", "aws",
    "docker", "kubernetes", "machine learning", "nlp", "bert", "gemini", "whisper",
    "git", "rest api", "pandas", "numpy", "node", "express"
}

EDU_KEYWORDS = ["b.tech", "bachelor", "master", "m.tech", "phd", "b.sc", "m.sc", "mba"]


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    try:
        import fitz
    except Exception:
        return ""

    text_parts: List[str] = []
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        text_parts.append(page.get_text("text"))
    return "\n".join(text_parts)


def extract_text_from_docx_bytes(docx_bytes: bytes) -> str:
    try:
        from docx import Document
    except Exception:
        return ""

    try:
        document = Document(io.BytesIO(docx_bytes))
        return "\n".join([p.text for p in document.paragraphs if p.text])
    except Exception:
        return ""


def extract_text_from_resume_file(file_bytes: bytes, filename: str = "") -> str:
    lower_name = (filename or "").lower()
    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf_bytes(file_bytes)
    if lower_name.endswith(".docx"):
        return extract_text_from_docx_bytes(file_bytes)

    # For txt/csv/md/json and unknown text-like files.
    return file_bytes.decode("utf-8", errors="ignore")


def parse_resume(resume_text: str, required_skills: List[str]) -> Dict:
    text = resume_text.lower()
    extracted_skills = sorted([s for s in DEFAULT_SKILLS if s in text])
    education = [k for k in EDU_KEYWORDS if k in text]

    years = re.findall(r"(\d+)\+?\s+years", text)
    experience_years = float(max([int(y) for y in years], default=0))

    required_set = {s.strip().lower() for s in required_skills if s.strip()}
    if not required_set:
        required_set = set(extracted_skills)

    overlap = required_set.intersection(extracted_skills)
    score = round((len(overlap) / max(len(required_set), 1)) * 100, 2)
    missing = sorted(list(required_set - set(extracted_skills)))

    suggestions = []
    if missing:
        suggestions.append(f"Add project evidence for: {', '.join(missing[:6])}.")
    if experience_years < 2:
        suggestions.append("Highlight internships/freelance work with measurable outcomes.")
    if not education:
        suggestions.append("Add education details with degree, college, and graduation year.")

    return {
        "extracted_skills": extracted_skills,
        "education": education,
        "experience_years": experience_years,
        "skill_match_score": score,
        "missing_skills": missing,
        "suggestions": suggestions,
    }
