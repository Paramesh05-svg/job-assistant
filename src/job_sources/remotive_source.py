"""
remotive_source.py

Fetch Cloud / DevOps related jobs from Remotive API.

Returns standardized job objects for use throughout
Job Assistant V2.
"""

import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)

# ==================================================
# CONFIG
# ==================================================

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"

REQUEST_TIMEOUT = 20


# ==================================================
# SKILL EXTRACTION
# ==================================================

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
    "Git"
]


def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    matched_skills = []

    for skill in COMMON_SKILLS:

        if skill.lower() in text:

            matched_skills.append(skill)

    return sorted(
        list(
            set(matched_skills)
        )
    )


# ==================================================
# JOB FETCHER
# ==================================================

def fetch_jobs(
    keyword="Cloud Engineer",
    limit=50
):

    jobs = []

    try:

        logger.info(
            f"Searching Remotive for: {keyword}"
        )

        response = requests.get(
            REMOTIVE_API_URL,
            params={
                "search": keyword
            },
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        for job in data.get(
            "jobs",
            []
        )[:limit]:

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
            f"Fetched {len(jobs)} jobs "
            f"for keyword '{keyword}'"
        )

        return jobs

    except Exception as error:

        logger.error(
            f"Remotive fetch failed: {error}"
        )

        return []


# ==================================================
# MULTI KEYWORD SEARCH
# ==================================================

def fetch_multiple_keywords(
    keywords,
    limit_per_keyword=20
):

    all_jobs = []

    for keyword in keywords:

        jobs = fetch_jobs(
            keyword=keyword,
            limit=limit_per_keyword
        )

        all_jobs.extend(
            jobs
        )

    return remove_duplicates(
        all_jobs
    )


# ==================================================
# DUPLICATE REMOVAL
# ==================================================

def remove_duplicates(jobs):

    unique_jobs = []

    seen = set()

    for job in jobs:

        key = (

            job["company"].lower(),

            job["role"].lower()
        )

        if key not in seen:

            seen.add(key)

            unique_jobs.append(job)

    return unique_jobs


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    test_keywords = [

        "Cloud Engineer",

        "DevOps Engineer",

        "AWS Engineer"
    ]

    jobs = fetch_multiple_keywords(
        test_keywords,
        limit_per_keyword=10
    )

    print(
        f"\nTotal Jobs Found: "
        f"{len(jobs)}\n"
    )

    for job in jobs[:10]:

        print(
            f"{job['company']} | "
            f"{job['role']} | "
            f"{job['location']}"
        )
