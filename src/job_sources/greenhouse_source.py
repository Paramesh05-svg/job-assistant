from src.parsers.skill_extractor import extract_skills
from src.utils.logger import get_logger

import requests

logger = get_logger(__name__)

GREENHOUSE_BOARDS = [
    "datadog",
    "cloudflare",
    "newrelic",
    "elastic",
    "stripe",
    "mongodb"
]

TARGET_KEYWORDS = [
    "cloud",
    "devops",
    "aws",
    "linux",
    "site reliability",
    "sre",
    "platform",
    "infrastructure",
    "systems engineer"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}


def is_relevant_role(role):

    role = role.lower()

    return any(
        keyword in role
        for keyword in TARGET_KEYWORDS
    )


def fetch_jobs():

    jobs = []

    for board in GREENHOUSE_BOARDS:

        try:

            url = (
                "https://boards-api.greenhouse.io/v1/boards/"
                f"{board}/jobs"
            )

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            board_jobs = 0

            for job in data.get("jobs", []):

                role = job.get(
                    "title",
                    ""
                )

                if not is_relevant_role(role):
                    continue

                content = job.get(
                    "content",
                    ""
                )

                jobs.append(
                    {
                        "company": board.title(),

                        "role": role,

                        "location": job.get(
                            "location",
                            {}
                        ).get(
                            "name",
                            ""
                        ),

                        "platform": "Greenhouse",

                        "job_link": job.get(
                            "absolute_url",
                            ""
                        ),

                        "description": content,

                        "skills": extract_skills(
                            content
                        ),
                    }
                )

                board_jobs += 1

            logger.info(
                f"{board}: {board_jobs} relevant jobs"
            )

        except Exception as error:

            logger.error(
                f"Greenhouse error "
                f"{board}: {error}"
            )

    logger.info(
        f"Greenhouse fetched "
        f"{len(jobs)} relevant jobs"
    )

    return jobs


if __name__ == "__main__":

    jobs = fetch_jobs()

    print(
        f"\nTotal Greenhouse Jobs: "
        f"{len(jobs)}\n"
    )

    for job in jobs[:10]:

        print(
            f"{job['company']} | "
            f"{job['role']} | "
            f"{job['location']}"
        )
