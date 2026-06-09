from src.job_sources.remotive_source import (
    fetch_jobs as remotive_jobs
)

from src.job_sources.greenhouse_source import (
    fetch_jobs as greenhouse_jobs
)

from src.job_sources.lever_source import (
    fetch_jobs as lever_jobs
)


def remove_duplicates(jobs):

    seen = set()

    unique = []

    for job in jobs:

        key = (

            job["company"].lower(),

            job["role"].lower()
        )

        if key not in seen:

            seen.add(key)

            unique.append(job)

    return unique


def fetch_all_jobs():

    jobs = []

    jobs.extend(
        remotive_jobs()
    )

    jobs.extend(
        greenhouse_jobs()
    )

    jobs.extend(
        lever_jobs()
    )

    return remove_duplicates(
        jobs
    )
