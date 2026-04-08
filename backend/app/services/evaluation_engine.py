from typing import Dict, List


def evaluate_candidate(skill_match_score: float, job_match_score: float, interview_score: float) -> Dict:
    final = round((skill_match_score * 0.35) + (job_match_score * 0.25) + (interview_score * 0.40), 2)

    strengths: List[str] = []
    weaknesses: List[str] = []

    if skill_match_score >= 70:
        strengths.append("Strong resume-to-role skill alignment")
    else:
        weaknesses.append("Skill coverage gaps compared to role requirements")

    if interview_score >= 70:
        strengths.append("Good communication and technical articulation")
    else:
        weaknesses.append("Interview responses need more depth and structure")

    if job_match_score >= 65:
        strengths.append("Relevant experience profile")
    else:
        weaknesses.append("Experience weightage lower than target role")

    recommendation = "Hire" if final >= 75 else ("Hold" if final >= 55 else "Reject")

    return {
        "final_score": final,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendation": recommendation,
    }
