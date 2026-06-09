def calculate_match(
        candidate_skills,
        job_skills):

    matched = set(
        candidate_skills
    ).intersection(
        set(job_skills)
    )

    if len(job_skills) == 0:
        return 0, []

    score = int(
        len(matched)
        / len(job_skills)
        * 100
    )

    return score, list(matched)


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

    print(score)
    print(matched)
