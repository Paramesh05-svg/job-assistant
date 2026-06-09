from src.job_sources.remotive_source import (
    fetch_jobs as remotive_jobs
)

from src.job_sources.greenhouse_source import (
    fetch_jobs as greenhouse_jobs
)


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


def fetch_all_jobs():

    jobs = []

    jobs.extend(
        remotive_jobs()
    )

    jobs.extend(
        greenhouse_jobs()
    )

    return remove_duplicates(
        jobs
    )
