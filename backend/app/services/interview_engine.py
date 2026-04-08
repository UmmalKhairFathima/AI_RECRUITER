from typing import List


def generate_questions(job_title: str, round_type: str) -> List[str]:
    base = [
        f"Tell me about a project where you used skills relevant to {job_title}.",
        "How do you prioritize tasks when deadlines are tight?",
        "Explain a difficult bug you solved and your debugging process.",
        "How do you ensure clean, maintainable code in team projects?",
        "What are your growth goals for the next 12 months?",
    ]

    if round_type.lower() == "hr":
        return [
            "Tell me about yourself in 90 seconds.",
            "Why are you interested in this role?",
            "Describe a conflict at work and how you resolved it.",
            "What motivates you beyond salary?",
            "Do you have any questions for us?",
        ]
    return base


def score_answer(answer: str, expected_keywords: List[str]) -> float:
    answer_l = answer.lower().strip()
    if not answer_l:
        return 0.0

    wc = len(answer_l.split())
    length_score = min(wc / 80, 1.0) * 50
    keyword_hits = sum(1 for kw in expected_keywords if kw.lower() in answer_l)
    keyword_score = min(keyword_hits / max(len(expected_keywords), 1), 1.0) * 50

    return round(length_score + keyword_score, 2)
