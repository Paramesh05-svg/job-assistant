from datetime import datetime

from src.resume_parser import parse_resume
from src.utils.config_loader import load_keywords
from src.job_search_engine import search_jobs
from src.ats_matcher import calculate_match
from src.excel_tracker import initialize_tracker, add_job


def main():
    print("\n===== JOB ASSISTANT STARTED =====\n")

    # Initialize Excel tracker
    initialize_tracker()

    # Load keywords from YAML
    config = load_keywords()

    job_titles = config.get("job_titles", [])

    if not job_titles:
        print("No job titles found in keywords.yaml")
        return

    # Parse resume
    profile = parse_resume("resume/Parameshwari_New.pdf")

    candidate_skills = profile.get("skills", [])

    print("Resume Parsed Successfully")
    print(f"Skills Found: {candidate_skills}\n")

    all_jobs = []

    # Search jobs
    for title in job_titles:
        print(f"Searching jobs for: {title}")

        jobs = search_jobs(
            keyword=title,
            limit=10
        )

        if jobs:
            all_jobs.extend(jobs)

    if not all_jobs:
        print("No jobs found.")
        return

    print(f"\nFound {len(all_jobs)} jobs.\n")

    # Process jobs
    for job in all_jobs:

        job_skills = job.get("skills", [])

        score, matched = calculate_match(
            candidate_skills,
            job_skills
        )

        print(f"Company : {job['company']}")
        print(f"Role    : {job['role']}")
        print(f"ATS Match : {score}%")
        print(f"Matched Skills : {matched}")
        print("-" * 50)

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

    print("\nJob data saved successfully.")
    print("\n===== JOB ASSISTANT COMPLETED =====")


if __name__ == "__main__":
    main()
