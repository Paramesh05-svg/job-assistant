import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"

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

    return list(set(found_skills))


def fetch_jobs(limit=100):

    jobs = []

    try:

        response = requests.get(
            REMOTIVE_API_URL,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        for job in data.get("jobs", []):

            description = job.get(
                "description",
                ""
            )

            jobs.append({

                "company":
                    job.get(
                        "company_name",
                        ""
                    ),

                "role":
                    job.get(
                        "title",
                        ""
                    ),

                "location":
                    job.get(
                        "candidate_required_location",
                        "Remote"
                    ),

                "platform":
                    "Remotive",

                "job_link":
                    job.get(
                        "url",
                        ""
                    ),

                "description":
                    description,

                "skills":
                    extract_skills(
                        description
                    )
            })

        logger.info(
            f"Fetched {len(jobs)} jobs from Remotive"
        )

        return jobs[:limit]

    except Exception as error:

        logger.error(
            f"Remotive fetch failed: {error}"
        )

        return []
