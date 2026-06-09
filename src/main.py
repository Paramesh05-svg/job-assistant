from src.resume_parser import parse_resume
from src.job_filter import filter_jobs

from src.job_sources.remotive_source import (
    fetch_jobs
)

from src.ats_matcher import (
    calculate_match
)

from src.storage.sqlite_store import (
    initialize_database,
    insert_job
)

from src.storage.excel_exporter import (
    export_jobs_to_excel
)


def main():

    print(
        "\n===== JOB ASSISTANT STARTED =====\n"
    )

    initialize_database()

    profile = parse_resume(
        "resume/Parameshwari_New.pdf"
    )

    candidate_skills = profile.get(
        "skills",
        []
    )

    print(
        f"Resume Skills: {candidate_skills}\n"
    )

    jobs = fetch_jobs()

    print(
        f"Raw Jobs Fetched: {len(jobs)}"
    )

    jobs = filter_jobs(jobs)

    print(
        f"Relevant Jobs: {len(jobs)}\n"
    )

    for job in jobs:

        score, matched, missing = (
            calculate_match(
                candidate_skills,
                job.get(
                    "skills",
                    []
                )
            )
        )

        print("=" * 60)

        print(
            f"Company : {job['company']}"
        )

        print(
            f"Role    : {job['role']}"
        )

        print(
            f"Location: {job['location']}"
        )

        print(
            f"ATS     : {score}%"
        )

        print("=" * 60)

        insert_job({

            "company":
                job["company"],

            "role":
                job["role"],

            "location":
                job["location"],

            "platform":
                job["platform"],

            "job_link":
                job["job_link"],

            "ats_score":
                score,

            "matched_skills":
                matched
        })

    export_jobs_to_excel()

    print(
        "\n===== JOB ASSISTANT COMPLETED ====="
    )


if __name__ == "__main__":
    main()
