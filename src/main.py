from datetime import datetime

from src.resume_parser import parse_resume
from src.utils.config_loader import load_keywords
from src.job_search_engine import search_multiple_keywords
from src.ats_matcher import calculate_match
from src.excel_tracker import initialize_tracker, add_job


def main():

    print("\n===== JOB ASSISTANT STARTED =====\n")

    # Initialize tracker
    initialize_tracker()

    # Load keywords
    config = load_keywords()

    job_titles = [
        "cloud",
        "devops",
        "aws",
        "linux",
        "platform engineer",
        "site reliability"
     ]

    if not job_titles:
        print("No job titles found in keywords.yaml")
        return

    print("Keywords Loaded:")
    for title in job_titles:
        print(f"  - {title}")

    print()

    # Parse resume
    profile = parse_resume(
        "resume/Parameshwari_New.pdf"
    )

    candidate_skills = profile.get(
        "skills",
        []
    )

    print("Resume Parsed Successfully")
    print(f"Skills Found: {candidate_skills}\n")

    # Search jobs from all keywords
    all_jobs = search_multiple_keywords(
        keywords=job_titles,
        limit_per_keyword=10
    )

    if not all_jobs:
        print("No jobs found.")
        return

    print(f"\nFound {len(all_jobs)} jobs.\n")

    jobs_saved = 0

    # Process jobs
    for job in all_jobs:

        job_skills = job.get(
            "skills",
            []
        )

        score, matched = calculate_match(
            candidate_skills,
            job_skills
        )

        print("=" * 70)
        print(f"Company       : {job['company']}")
        print(f"Role          : {job['role']}")
        print(f"Location      : {job.get('location', '')}")
        print(f"Platform      : {job.get('platform', '')}")
        print(f"ATS Match     : {score}%")
        print(f"Matched Skills: {matched}")
        print("=" * 70)

        add_job({
            "Company Name": job["company"],
            "Role": job["role"],
            "Location": job.get("location", ""),
            "Platform": job.get("platform", ""),
            "Job Link": job.get("link", ""),
            "ATS Match": score,
            "Date Found": datetime.now().strftime("%Y-%m-%d"),
            "Approval Status": "Pending",
            "Applied": "No",
            "Date Applied": "",
            "Status": "New",
            "Notes": ""
        })

        jobs_saved += 1

    print(f"\n{jobs_saved} jobs saved successfully.")
    print("\n===== JOB ASSISTANT COMPLETED =====")


if __name__ == "__main__":
    main()
