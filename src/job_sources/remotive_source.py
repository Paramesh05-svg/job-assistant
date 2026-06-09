import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)

REMOTIVE_API = "https://remotive.com/api/remote-jobs"


def fetch_jobs(limit=100):

    try:

        response = requests.get(
            REMOTIVE_API,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get("jobs", []):

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
                        ""
                    ),

                "platform":
                    "Remotive",

                "job_link":
                    job.get(
                        "url",
                        ""
                    ),

                "description":
                    job.get(
                        "description",
                        ""
                    ),

                "skills": []
            })

        logger.info(
            f"Fetched {len(jobs)} jobs from Remotive"
        )

        return jobs[:limit]

    except Exception as error:

        logger.error(
            f"Remotive error: {error}"
        )

        return []
