def calculate_match(candidate_skills, job_skills):

    candidate_set = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    job_set = {
        skill.lower().strip()
        for skill in job_skills
    }

    if not job_set:
        return 0, []

    matched = candidate_set.intersection(job_set)

    score = round(
        (len(matched) / len(job_set)) * 100
    )

    return score, sorted(list(matched))
