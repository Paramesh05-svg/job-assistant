import requests
import logging

# ---------------- LOGGING SETUP ----------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- SKILL DATABASE ----------------

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


# ---------------- SKILL EXTRACTION ----------------

def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    matched_skills = []

    for skill in COMMON_SKILLS:
        if skill.lower() in text:
            matched_skills.append(skill)

    return list(set(matched_skills))


# ---------------- REMOTIVE SEARCH ----------------

def search_jobs(keyword="Cloud Engineer", limit=20):

    url = "https://remotive.com/api/remote-jobs"

    try:

        logger.info(f"Searching jobs for keyword: {keyword}")

        response = requests.get(
            url,
            params={"search": keyword},
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get("jobs", []):

            description = job.get("description", "")

            jobs.append({
                "company": job.get("company_name", ""),
                "role": job.get("title", ""),
                "skills": extract_skills(description),
                "location": job.get(
                    "candidate_required_location",
                    "Remote"
                ),
                "platform": "Remotive",
                "link": job.get("url", "")
            })

            if len(jobs) >= limit:
                break

        logger.info(
            f"{len(jobs)} jobs fetched for keyword '{keyword}'"
        )

        return jobs

    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return []

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return []

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []


# ---------------- MULTI KEYWORD SEARCH ----------------

def search_multiple_keywords(keywords, limit_per_keyword=10):

    all_jobs = []

    for keyword in keywords:

        jobs = search_jobs(
            keyword=keyword,
            limit=limit_per_keyword
        )

        all_jobs.extend(jobs)

    return remove_duplicates(all_jobs)


# ---------------- REMOVE DUPLICATES ----------------

def remove_duplicates(jobs):

    seen = set()
    unique_jobs = []

    for job in jobs:

        key = (
            job["company"].lower(),
            job["role"].lower()
        )

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs


# ---------------- TEST ----------------

if __name__ == "__main__":

    test_keywords = [
        "cloud",
        "devops",
        "aws",
        "python"
    ]

    jobs = search_multiple_keywords(
        test_keywords,
        limit_per_keyword=5
    )

    print(f"\nFound {len(jobs)} jobs\n")

    for job in jobs[:10]:

        print(
            f"{job['company']} | "
            f"{job['role']} | "
            f"{job['skills']}"
        )
