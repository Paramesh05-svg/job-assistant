def calculate_match(candidate_skills, job_skills):

    candidate_skills = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    job_skills = {
        skill.lower().strip()
        for skill in job_skills
    }

    if not job_skills:
        return 0, []

    matched = candidate_skills.intersection(job_skills)

    # Percentage of job requirements matched
    score = round(
        (len(matched) / len(job_skills)) * 100
    )

    matched_skills = sorted(
        list(matched)
    )

    return score, matched_skills


if __name__ == "__main__":

    candidate = [
        "AWS",
        "Linux",
        "Terraform",
        "Python"
    ]

    job = [
        "AWS",
        "Linux",
        "Docker",
        "Terraform"
    ]

    score, matched = calculate_match(
        candidate,
        job
    )

    print(f"Score: {score}%")
    print(f"Matched: {matched}")
