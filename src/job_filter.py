"""
job_filter.py

Filters jobs based on:

1. Role
2. Location
3. Experience

Used before ATS scoring and database insertion.
"""

import re

from src.utils.logger import get_logger

logger = get_logger(__name__)

# ==================================================
# TARGET ROLES
# ==================================================

TARGET_ROLES = [

    "cloud engineer",
    "devops engineer",
    "aws engineer",
    "aws devops engineer",
    "cloud support engineer",
    "linux administrator",
    "linux engineer",
    "site reliability engineer",
    "sre",
    "platform engineer",
    "infrastructure engineer",
    "systems engineer"
]

# ==================================================
# TARGET LOCATIONS
# ==================================================

TARGET_LOCATIONS = [

    "chennai",
    "bengaluru",
    "bangalore",
    "hyderabad",
    "coimbatore",
    "remote"
]

# ==================================================
# EXPERIENCE LIMIT
# ==================================================

MIN_EXPERIENCE = 0
MAX_EXPERIENCE = 2


# ==================================================
# ROLE FILTER
# ==================================================

def role_matches(role):

    role = str(role).lower()

    for target_role in TARGET_ROLES:

        if target_role in role:
            return True

    return False


# ==================================================
# LOCATION FILTER
# ==================================================

def location_matches(location):

    location = str(location).lower()

    for target_location in TARGET_LOCATIONS:

        if target_location in location:
            return True

    return False


# ==================================================
# EXPERIENCE EXTRACTION
# ==================================================

def extract_experience(job_text):
    """
    Extract years of experience from
    job description.

    Examples:

    0 years
    1 year
    2 years
    3+ years
    5 years experience
    """

    try:

        matches = re.findall(
            r'(\d+)\+?\s*(?:year|years)',
            str(job_text).lower()
        )

        if matches:

            years = max(
                int(value)
                for value in matches
            )

            return years

        return 0

    except Exception as error:

        logger.error(
            f"Experience extraction failed: {error}"
        )

        return 0


# ==================================================
# EXPERIENCE FILTER
# ==================================================

def experience_matches(job_text):

    years = extract_experience(
        job_text
    )

    return (
        MIN_EXPERIENCE
        <= years
        <= MAX_EXPERIENCE
    )


# ==================================================
# MAIN FILTER
# ==================================================

def is_relevant_job(job):

    try:

        role = job.get(
            "role",
            ""
        )

        location = job.get(
            "location",
            ""
        )

        description = job.get(
            "description",
            ""
        )

        if not role_matches(role):

            logger.info(
                f"Rejected Role: {role}"
            )

            return False

        if not location_matches(location):

            logger.info(
                f"Rejected Location: {location}"
            )

            return False

        if not experience_matches(description):

            logger.info(
                "Rejected Experience"
            )

            return False

        return True

    except Exception as error:

        logger.error(
            f"Job filtering failed: {error}"
        )

        return False


# ==================================================
# BULK FILTER
# ==================================================

def filter_jobs(jobs):

    filtered_jobs = []

    for job in jobs:

        if is_relevant_job(job):

            filtered_jobs.append(job)

    logger.info(
        f"Filtered {len(filtered_jobs)} "
        f"out of {len(jobs)} jobs"
    )

    return filtered_jobs


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    sample_jobs = [

        {
            "role": "Cloud Engineer",
            "location": "Chennai",
            "description": "Looking for AWS Engineer with 1 year experience"
        },

        {
            "role": "Java Developer",
            "location": "Mumbai",
            "description": "4 years experience required"
        },

        {
            "role": "DevOps Engineer",
            "location": "Remote",
            "description": "0-2 years experience"
        }
    ]

    result = filter_jobs(
        sample_jobs
    )

    print(
        f"\nRelevant Jobs: {len(result)}\n"
    )

    for job in result:

        print(
            f"{job['role']} | "
            f"{job['location']}"
        )
