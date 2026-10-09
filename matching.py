"""
Talent-to-Project and Project-to-Talent Matching Engine for Odisha AI Nexus.
Employs normalized tokenization, skill overlap, and domain interest affinity
to compute transparent match percentages with human-readable explanations.
"""

import re
from typing import List, Dict, Any, Tuple


def _tokenize(text: str) -> set:
    """Extract lowercased alphanumeric tokens from text string."""
    if not text:
        return set()
    cleaned = re.sub(r"[,\(\)\/\-\+\.]", " ", text.lower())
    tokens = {token.strip() for token in cleaned.split() if len(token.strip()) > 1}
    return tokens


def mask_email(email: str) -> str:
    """Mask email address for privacy protection."""
    if not email or "@" not in email:
        return "Private / Confidential"
    parts = email.split("@")
    user, domain = parts[0], parts[1]
    if len(user) <= 2:
        masked_user = user[0] + "*"
    else:
        masked_user = user[0] + "*" * (len(user) - 2) + user[-1]
    return f"{masked_user}@{domain}"


def calculate_talent_project_match(talent: Dict[str, Any], project: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate match score and explainability breakdown between a talent profile and a project.
    """
    talent_skills = _tokenize(talent.get("technical_skills", ""))
    talent_interests = _tokenize(talent.get("areas_of_interest", ""))
    
    project_tech = _tokenize(project.get("tech_stack", ""))
    project_desc = _tokenize(project.get("description", "") + " " + project.get("title", ""))
    project_sector = _tokenize(project.get("sector", ""))

    # 1. Direct Skill Overlap
    # Compare talent skills with project tech stack and full description
    combined_project_text_skills = project_tech.union(project_desc)
    matched_skills = sorted(list(talent_skills.intersection(combined_project_text_skills)))
    
    if project_tech:
        skill_score = min(100.0, (len(matched_skills) / max(len(project_tech), 1)) * 100.0)
    else:
        skill_score = min(100.0, len(matched_skills) * 25.0)

    # 2. Sector & Domain Affinity
    domain_overlap = talent_interests.intersection(project_sector.union(project_desc))
    domain_score = 100.0 if domain_overlap else 40.0

    # 3. District / Proximity Synergy Bonus (bonus if same district)
    district_bonus = 0.0
    talent_district = talent.get("district", "").strip().lower()
    project_district = project.get("district", "").strip().lower()
    if talent_district and project_district and (talent_district in project_district or project_district in talent_district):
        district_bonus = 10.0

    # Composite Match Score (Weighted: 60% skills, 30% domain, 10% proximity)
    composite_score = (skill_score * 0.60) + (domain_score * 0.30) + district_bonus
    final_score = min(100.0, max(0.0, round(composite_score, 1)))

    # Explanation text
    reasons = []
    if matched_skills:
        reasons.append(f"Skill Alignment: Matches {len(matched_skills)} core technical competencies ({', '.join(matched_skills[:4])}).")
    else:
        reasons.append("Skill Alignment: Baseline algorithmic skills present; complementary learning required.")

    if domain_overlap:
        reasons.append(f"Domain Interest: Explicit passion for {project.get('sector', 'this domain')}.")
    
    if district_bonus > 0:
        reasons.append(f"Local Proximity: Both located in {talent.get('district')} for high-bandwidth collaboration.")

    return {
        "score": final_score,
        "matched_skills": matched_skills,
        "has_domain_overlap": bool(domain_overlap),
        "has_district_proximity": district_bonus > 0,
        "reasons": reasons,
    }


def find_top_projects_for_talent(
    talent: Dict[str, Any],
    projects: List[Dict[str, Any]],
    top_n: int = 5
) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """Return top matched projects for a given talent profile."""
    scored = []
    for project in projects:
        match_info = calculate_talent_project_match(talent, project)
        scored.append((project, match_info))
    
    scored.sort(key=lambda x: x[1]["score"], reverse=True)
    return scored[:top_n]


def find_top_talent_for_project(
    project: Dict[str, Any],
    talents: List[Dict[str, Any]],
    top_n: int = 5
) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """Return top matched talent candidates for a given project."""
    scored = []
    for talent in talents:
        match_info = calculate_talent_project_match(talent, project)
        scored.append((talent, match_info))
    
    scored.sort(key=lambda x: x[1]["score"], reverse=True)
    return scored[:top_n]
