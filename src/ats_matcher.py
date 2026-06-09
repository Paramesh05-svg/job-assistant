"""
ats_matcher.py

ATS scoring engine for Job Assistant V2

Features:
- Case-insensitive matching
- Skill normalization
- Percentage scoring
- Matched skills tracking
- Missing skills tracking
"""

from src.utils.logger import get_logger

logger = get_logger(__name__)

# ==================================================
# SKILL ALIASES
# ==================================================

SKILL_ALIASES = {
    "amazon web services": "aws",
    "shell scripting": "shell",
    "bash": "shell",
    "gitlab ci": "gitlab",
    "jenkins ci": "jenkins",
    "k8s": "kubernetes",
    "terraform iaac": "terraform"
}


# ==================================================
# NORMALIZE SKILLS
# ==================================================

def normalize_skills(skills):

    normalized = set()

    for skill in skills:

        skill = str(skill).strip().lower()

        if skill in SKILL_ALIASES:
            skill = SKILL_ALIASES[skill]

        normalized.add(skill)

    return normalized


# ==================================================
# CALCULATE ATS MATCH
# ==================================================

def calculate_match(
    candidate_skills,
    job_skills
):
    """
    Returns:

    (
        ats_score,
        matched_skills,
        missing_skills
    )
    """

    try:

        candidate_set = normalize_skills(
            candidate_skills
        )

        job_set = normalize_skills(
            job_skills
        )

        if not job_set:

            return (
                0,
                [],
                []
            )

        matched = sorted(
            list(
                candidate_set.intersection(
                    job_set
                )
            )
        )

        missing = sorted(
            list(
                job_set.difference(
                    candidate_set
                )
            )
        )

        score = round(
            (
                len(matched)
                / len(job_set)
            )
            * 100
        )

        logger.info(
            f"ATS Score={score}% | "
            f"Matched={len(matched)} | "
            f"Missing={len(missing)}"
        )

        return (
            score,
            matched,
            missing
        )

    except Exception as error:

        logger.error(
            f"ATS calculation failed: {error}"
        )

        return (
            0,
            [],
            []
        )


# ==================================================
# JOB ELIGIBILITY
# ==================================================

def is_eligible(
    ats_score,
    minimum_score=30
):

    return ats_score >= minimum_score


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    candidate = [
        "AWS",
        "Linux",
        "Terraform",
        "Docker",
        "Python",
        "Jenkins"
    ]

    job = [
        "AWS",
        "Linux",
        "Docker",
        "Kubernetes",
        "Terraform",
        "GitLab"
    ]

    score, matched, missing = calculate_match(
        candidate,
        job
    )

    print("\nATS SCORE")
    print(score)

    print("\nMATCHED")
    print(matched)

    print("\nMISSING")
    print(missing)

    print("\nELIGIBLE")
    print(
        is_eligible(
            score,
            minimum_score=30
        )
    )
