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
    "infrastructure engineer"
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
    "gurugram"
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


def filter_jobs(jobs):

    filtered = []

    for job in jobs:

        role = job.get("role", "")
        location = job.get("location", "")

        if not is_valid_role(role):
            continue

        if not is_valid_location(location):
            continue

        filtered.append(job)

    logger.info(
        f"Filtered {len(filtered)} from {len(jobs)} jobs"
    )

    return filtered
