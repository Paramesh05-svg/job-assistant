"""
resume_parser.py

Parses PDF resume and extracts:

- Candidate Skills
- Resume Text
- Candidate Profile

Compatible with:
resume/Parameshwari_New.pdf
"""

from pathlib import Path

import pdfplumber

from src.utils.logger import get_logger

logger = get_logger(__name__)

# ==================================================
# SKILL DATABASE
# ==================================================

TECHNICAL_SKILLS = [

    "AWS",
    "Terraform",
    "Docker",
    "Kubernetes",
    "Linux",
    "Python",
    "Jenkins",
    "GitLab",
    "Ansible",
    "Shell",
    "Shell Scripting",
    "CloudWatch",
    "Networking",
    "Git",
    "CI/CD",
    "DevOps",
    "EC2",
    "S3",
    "VPC",
    "IAM",
    "Route53",
    "RDS",
    "Load Balancer",
    "Auto Scaling",
    "CloudFormation",
    "EKS",
    "ECS",
    "Prometheus",
    "Grafana",
    "Nginx",
    "Apache",
    "MySQL",
    "PostgreSQL",
    "Linux Administration"
]


# ==================================================
# EXTRACT PDF TEXT
# ==================================================

def extract_text_from_pdf(pdf_path):

    try:

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():

            raise FileNotFoundError(
                f"Resume not found: {pdf_path}"
            )

        full_text = ""

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    full_text += page_text + "\n"

        logger.info(
            f"Resume loaded successfully: "
            f"{pdf_path}"
        )

        return full_text

    except Exception as error:

        logger.error(
            f"Resume parsing failed: {error}"
        )

        return ""


# ==================================================
# SKILL EXTRACTION
# ==================================================

def extract_skills(text):

    if not text:

        return []

    text = text.lower()

    matched_skills = []

    for skill in TECHNICAL_SKILLS:

        if skill.lower() in text:

            matched_skills.append(
                skill
            )

    return sorted(
        list(
            set(
                matched_skills
            )
        )
    )


# ==================================================
# PROFILE CREATION
# ==================================================

def parse_resume(pdf_path):

    text = extract_text_from_pdf(
        pdf_path
    )

    skills = extract_skills(
        text
    )

    profile = {

        "resume_path": str(
            pdf_path
        ),

        "skills": skills,

        "resume_text": text
    }

    logger.info(
        f"Skills extracted: "
        f"{len(skills)}"
    )

    return profile


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    profile = parse_resume(
        "resume/Parameshwari_New.pdf"
    )

    print("\nResume Parsed Successfully\n")

    print("Skills Found:\n")

    for skill in profile["skills"]:

        print(f"- {skill}")

    print(
        f"\nTotal Skills: "
        f"{len(profile['skills'])}"
    )
