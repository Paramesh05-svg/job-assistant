from src.parsers.skill_extractor import extract_skills
from src.utils.logger import get_logger

import requests

logger = get_logger(__name__)

GREENHOUSE_BOARDS = [
    "hashicorp",
    "datadog",
    "cloudflare",
    "newrelic",
    "elastic",
    "stripe",
    "mongodb",
]


def fetch_jobs():
    jobs = []

    for board in GREENHOUSE_BOARDS:
        try:
            url = (
                f"https://boards-api.greenhouse.io/v1/boards/"
                f"{board}/jobs"
            )

            response = requests.get(
                url,
                timeout=20,
            )

            response.raise_for_status()

            data = response.json()

            for job in data.get("jobs", []):
                content = job.get(
                    "content",
                    ""
                )

                jobs.append(
                    {
                        "company": board.title(),
                        "role": job.get(
                            "title",
                            ""
                        ),
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

        except Exception as error:
            logger.error(
                f"Greenhouse error "
                f"{board}: {error}"
            )

    logger.info(
        f"Greenhouse fetched "
        f"{len(jobs)} jobs"
    )

    return jobs
