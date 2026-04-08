from typing import List


def jaccard_similarity(a: List[str], b: List[str]) -> float:
    sa = {x.lower().strip() for x in a if x.strip()}
    sb = {x.lower().strip() for x in b if x.strip()}
    if not sa and not sb:
        return 0.0
    return len(sa.intersection(sb)) / max(len(sa.union(sb)), 1)


def compute_job_match_score(candidate_skills: List[str], job_skills: List[str], experience_years: float, min_exp: int) -> float:
    skill_component = jaccard_similarity(candidate_skills, job_skills) * 70
    exp_component = min(experience_years / max(min_exp, 1), 1.0) * 30 if min_exp > 0 else 30
    return round(skill_component + exp_component, 2)
