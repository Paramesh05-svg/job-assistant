from src.utils.logger import get_logger

logger = get_logger(__name__)

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
]

TARGET_LOCATIONS = [
    "india",
    "remote",
    "chennai",
    "bengaluru",
    "bangalore",
    "hyderabad",
    "coimbatore",
    "pune",
    "noida",
    "gurugram",
]

FRESHER_KEYWORDS = [
    "fresher",
    "freshers",
    "entry level",
    "graduate",
    "junior",
    "associate",
    "trainee",
    "intern",
    "0-1 year",
    "0 to 1 year",
    "0 year",
]

SENIORITY_BLOCKLIST = [
    "senior",
    "sr.",
    "staff",
    "principal",
    "lead",
    "manager",
    "director",
    "head",
    "architect",
    "vp",
    "vice president",
]


def is_valid_role(role):
    role = role.lower().strip()

    return any(
        target in role
        for target in TARGET_ROLES
    )


def is_valid_location(location):
    location = location.lower().strip()

    return any(
        target in location
        for target in TARGET_LOCATIONS
    )


def is_fresher_role(role):
    role = role.lower()

    # Reject senior positions
    if any(
        word in role
        for word in SENIORITY_BLOCKLIST
    ):
        return False

    # Prioritize fresher-friendly titles
    if any(
        keyword in role
        for keyword in FRESHER_KEYWORDS
    ):
        return True

    # Neutral titles like "Cloud Engineer"
    return True


def filter_jobs(jobs):
    priority_jobs = []
    regular_jobs = []

    for job in jobs:
        role = job.get("role", "")
        location = job.get("location", "")

        if not is_valid_role(role):
            continue

        if not is_valid_location(location):
            continue

        if not is_fresher_role(role):
            continue

        role_lower = role.lower()

        if any(
            keyword in role_lower
            for keyword in FRESHER_KEYWORDS
        ):
            priority_jobs.append(job)
        else:
            regular_jobs.append(job)

    filtered = priority_jobs + regular_jobs

    logger.info(
        f"Filtered {len(filtered)} from {len(jobs)} jobs "
        f"({len(priority_jobs)} fresher-priority jobs)"
    )

    return filtered
