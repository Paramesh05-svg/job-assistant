"""
excel_exporter.py

Exports jobs from SQLite database
to Excel workbook.
"""

from pathlib import Path

import pandas as pd

from src.storage.sqlite_store import get_connection
from src.utils.logger import get_logger

logger = get_logger(__name__)

# ==================================================
# EXPORT LOCATION
# ==================================================

DATA_DIR = Path("data")

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXCEL_FILE = DATA_DIR / "jobs.xlsx"


# ==================================================
# EXPORT JOBS
# ==================================================

def export_jobs_to_excel():

    try:

        conn = get_connection()

        query = """
        SELECT

            id,
            company,
            role,
            location,
            platform,
            job_link,
            ats_score,
            matched_skills,
            status,
            date_found,
            date_reviewed

        FROM jobs

        ORDER BY ats_score DESC
        """

        df = pd.read_sql_query(
            query,
            conn
        )

        conn.close()

        if df.empty:

            logger.warning(
                "No jobs found in database."
            )

            return False

        df.to_excel(
            EXCEL_FILE,
            index=False,
            engine="openpyxl"
        )

        logger.info(
            f"Excel exported successfully: "
            f"{EXCEL_FILE}"
        )

        print(
            f"\nExcel exported successfully:\n"
            f"{EXCEL_FILE}\n"
        )

        return True

    except Exception as error:

        logger.error(
            f"Excel export failed: {error}"
        )

        return False


# ==================================================
# EXPORT ONLY APPROVED JOBS
# ==================================================

def export_approved_jobs():

    try:

        conn = get_connection()

        query = """
        SELECT

            id,
            company,
            role,
            location,
            platform,
            job_link,
            ats_score,
            matched_skills,
            status,
            date_found,
            date_reviewed

        FROM jobs

        WHERE status='APPROVED'

        ORDER BY ats_score DESC
        """

        df = pd.read_sql_query(
            query,
            conn
        )

        conn.close()

        if df.empty:

            logger.warning(
                "No approved jobs found."
            )

            return False

        approved_file = (
            DATA_DIR /
            "approved_jobs.xlsx"
        )

        df.to_excel(
            approved_file,
            index=False,
            engine="openpyxl"
        )

        logger.info(
            f"Approved jobs exported: "
            f"{approved_file}"
        )

        print(
            f"\nApproved jobs exported:\n"
            f"{approved_file}\n"
        )

        return True

    except Exception as error:

        logger.error(
            f"Approved export failed: {error}"
        )

        return False


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    export_jobs_to_excel()
