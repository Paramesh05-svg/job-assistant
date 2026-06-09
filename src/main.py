from src.resume_parser import parse_resume

from src.ats_matcher import (
    calculate_match,
    is_eligible
)

from src.job_filter import filter_jobs

from src.job_sources.aggregator import (
    fetch_all_jobs
)

from src.storage.sqlite_store import (
    initialize_database,
    insert_job,
    count_jobs
)

from src.storage.excel_exporter import (
    export_jobs_to_excel
)

from src.utils.logger import get_logger

logger = get_logger(__name__)


# ==================================================
# CONFIG
# ==================================================

RESUME_PATH = "resume/Parameshwari_New.pdf"

MINIMUM_ATS_SCORE = 0


# ==================================================
# MAIN
# ==================================================

def main():

    print("\n===== JOB ASSISTANT STARTED =====\n")

    logger.info(
        "Job Assistant Started"
    )

    # ------------------------------------------
    # Database
    # ------------------------------------------

    initialize_database()

    # ------------------------------------------
    # Resume Parsing
    # ------------------------------------------

    profile = parse_resume(
        RESUME_PATH
    )

    candidate_skills = profile.get(
        "skills",
        []
    )

    print("Resume Parsed Successfully")

    print(
        f"Skills Found: {candidate_skills}\n"
    )

    # ------------------------------------------
    # Fetch Jobs
    # ------------------------------------------

    print(
        "Fetching jobs from all sources...\n"
    )

    jobs = fetch_all_jobs()

    print(
        f"Raw Jobs Retrieved: "
        f"{len(jobs)}"
    )

    # ------------------------------------------
    # Filter Jobs
    # ------------------------------------------

    jobs = filter_jobs(
        jobs
    )

    print(
        f"Relevant Jobs Found: "
        f"{len(jobs)}\n"
    )

    if not jobs:

        print(
            "No relevant jobs found."
        )

        return

    saved_count = 0

    # ------------------------------------------
    # ATS Matching
    # ------------------------------------------

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

  #      if not is_eligible(
#         score,
   #         MINIMUM_ATS_SCORE
    #    ):
     #       continue

        print("=" * 70)

        print(
            f"Company : "
            f"{job['company']}"
        )

        print(
            f"Role    : "
            f"{job['role']}"
        )

        print(
            f"Location: "
            f"{job['location']}"
        )

        print(
            f"Platform: "
            f"{job['platform']}"
        )

        print(
            f"ATS     : "
            f"{score}%"
        )

        print(
            f"Matched : "
            f"{matched}"
        )

        print(
            f"Missing : "
            f"{missing}"
        )

        print("=" * 70)

        success = insert_job({

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

        if success:
            saved_count += 1

    # ------------------------------------------
    # Export Excel
    # ------------------------------------------

    export_jobs_to_excel()

    # ------------------------------------------
    # Summary
    # ------------------------------------------

    print("\n===== SUMMARY =====\n")

    print(
        f"Jobs Saved : "
        f"{saved_count}"
    )

    print(
        f"Database Records : "
        f"{count_jobs()}"
    )

    print(
        "\nExcel Exported:"
        "\ndata/jobs.xlsx"
    )

    print(
        "\n===== JOB ASSISTANT COMPLETED =====\n"
    )

    logger.info(
        "Job Assistant Completed"
    )


# ==================================================
# ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()
