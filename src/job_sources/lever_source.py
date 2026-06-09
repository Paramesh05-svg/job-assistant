import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)

LEVER_COMPANIES = [

    "digitalocean",
    "crowdstrike",
    "sourcegraph",
    "scaleai",
    "asana"
]


def fetch_jobs():

    jobs = []

    for company in LEVER_COMPANIES:

        try:

            url = (
                f"https://api.lever.co/v0/postings/"
                f"{company}"
            )

            response = requests.get(
                url,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            for job in data:

                jobs.append({

                    "company": company.title(),

                    "role": job.get(
                        "text",
                        ""
                    ),

                    "location":
                        job.get(
                            "categories",
                            {}
                        ).get(
                            "location",
                            ""
                        ),

                    "platform":
                        "Lever",

                    "job_link":
                        job.get(
                            "hostedUrl",
                            ""
                        ),

                    "description": "",

                    "skills": []
                })

        except Exception as error:

            logger.error(
                f"Lever error "
                f"{company}: {error}"
            )

    logger.info(
        f"Lever fetched "
        f"{len(jobs)} jobs"
    )

    return jobs
