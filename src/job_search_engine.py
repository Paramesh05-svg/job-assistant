import requests

def search_jobs(
keyword="Cloud Engineer",
limit=20
):

```
url = "https://remotive.com/api/remote-jobs"

try:

    response = requests.get(
        url,
        params={"search": keyword},
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get(
        "jobs",
        []
    )[:limit]:

        jobs.append(
            {
                "company": job.get(
                    "company_name",
                    ""
                ),
                "role": job.get(
                    "title",
                    ""
                ),
                "skills": [],
                "location": job.get(
                    "candidate_required_location",
                    "Remote"
                ),
                "platform": "Remotive",
                "link": job.get(
                    "url",
                    ""
                )
            }
        )

    return jobs

except Exception as e:

    print(
        f"Job search failed: {e}"
    )

    return []
```

if **name** == "**main**":

```
jobs = search_jobs(
    "AWS DevOps"
)

print(
    f"Found {len(jobs)} jobs"
)

for job in jobs[:5]:

    print(
        f"{job['company']} | {job['role']}"
    )
```
