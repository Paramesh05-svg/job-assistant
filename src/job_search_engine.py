import requests
import logging

# ---------------- LOGGING SETUP ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------- JOB SEARCH ENGINE ----------------

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

        for job in data.get("jobs", [])[:limit]:

            jobs.append({
                "company": job.get("company_name", ""),
                "role": job.get("title", ""),
                "skills": [],
                "location": job.get("candidate_required_location", "Remote"),
                "platform": "Remotive",
                "link": job.get("url", "")
            })

        logger.info(f"Total jobs fetched: {len(jobs)}")

        return jobs

    except Exception as e:
        logger.error(f"Job search failed: {e}")
        return []


# ---------------- TEST RUN ----------------

if __name__ == "__main__":

    jobs = search_jobs("AWS DevOps")

    print(f"\nFound {len(jobs)} jobs\n")

    for job in jobs[:5]:
        print(f"{job['company']} | {job['role']}")
