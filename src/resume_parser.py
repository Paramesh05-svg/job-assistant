import pdfplumber
import json


KNOWN_SKILLS = [
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
    "CloudWatch",
    "Networking"
]


def parse_resume(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    detected_skills = []

    for skill in KNOWN_SKILLS:

        if skill.lower() in text.lower():
            detected_skills.append(skill)

    profile = {
        "skills": detected_skills
    }

    with open(
        "data/resume_profile.json",
        "w"
    ) as file:

        json.dump(profile, file, indent=4)

    return profile


if __name__ == "__main__":

    profile = parse_resume(
        "resume/Parameshwari_New.pdf"
    )

    print(profile)
