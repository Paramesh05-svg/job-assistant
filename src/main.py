import yaml
from datetime import datetime

from src.resume_parser import parse_resume
from src.job_search_engine import search_jobs
from src.ats_matcher import calculate_match
from src.excel_tracker import initialize_tracker, add_job


def load_keywords():
    with open("config/keywords.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    print("\n===== JOB ASSISTANT STARTED =====\n")

    # Initialize tracker
    initialize_tracker()

    # Load keywords
    config = load_keywords()
    job_titles = config.get("job_titles", [])

    # Parse resume
    profile = parse_resume("resume/Parameshwari_New.pdf")

    candidate_skills = profile.get("skills", [])

    print("Resume Parsed Successfully")
    print(f"Skills Found: {candidate_skills}\n")

    all_jobs = []

    # Search jobs for each keyword
    for title in job_titles:
        jobs = search_jobs(keyword=title, limit=10)
        if jobs:
            all_jobs.extend(jobs)

    if not all_jobs:
        print("No jobs found.")
        return

    print(f"Found {len(all_jobs)} jobs.\n")

    # Process each job
    for job in all_jobs:

        job_skills = job.get("skills", [])

        score, matched = calculate_match(candidate_skills, job_skills)

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
