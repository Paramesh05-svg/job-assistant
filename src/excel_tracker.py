import os
import pandas as pd

EXCEL_FILE = "data/applied_jobs.xlsx"

COLUMNS = [
    "S.No",
    "Company Name",
    "Role",
    "Location",
    "Platform",
    "Job Link",
    "ATS Match",
    "Date Found",
    "Approval Status",
    "Applied",
    "Date Applied",
    "Status",
    "Notes"
]


def initialize_tracker():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_excel(EXCEL_FILE, index=False)


def add_job(job_data):

    df = pd.read_excel(EXCEL_FILE)

    job_data["S.No"] = len(df) + 1

    df = pd.concat(
        [df, pd.DataFrame([job_data])],
        ignore_index=True
    )

    df.to_excel(EXCEL_FILE, index=False)


if __name__ == "__main__":
    initialize_tracker()
    print("Excel tracker initialized")
