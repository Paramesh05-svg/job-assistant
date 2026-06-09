COMMON_SKILLS = [
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
    "Networking",
    "DevOps",
    "CI/CD",
    "Git",
    "EC2",
    "S3",
    "IAM",
    "VPC",
    "RDS",
    "Load Balancer",
    "Auto Scaling"
]


def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found_skills = []

    for skill in COMMON_SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return sorted(
        list(set(found_skills))
    )
