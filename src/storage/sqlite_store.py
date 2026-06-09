"""
sqlite_store.py

SQLite database manager for Job Assistant V2

Features:
- Create database automatically
- Create jobs table automatically
- Insert jobs
- Prevent duplicates
- Update approval status
- Fetch jobs
- Fetch pending jobs
- Delete jobs
"""

import sqlite3
from pathlib import Path
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger(__name__)

# ==================================================
# DATABASE CONFIGURATION
# ==================================================

DATA_DIR = Path("data")

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_FILE = DATA_DIR / "jobs.db"


# ==================================================
# CONNECTION
# ==================================================

def get_connection():

    return sqlite3.connect(
        DATABASE_FILE
    )


# ==================================================
# CREATE TABLE
# ==================================================

def initialize_database():

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            company TEXT NOT NULL,

            role TEXT NOT NULL,

            location TEXT,

            platform TEXT,

            job_link TEXT,

            ats_score INTEGER,

            matched_skills TEXT,

            status TEXT DEFAULT 'PENDING',

            date_found TEXT,

            date_reviewed TEXT
        )
        """)

        conn.commit()

        conn.close()

        logger.info(
            "Database initialized successfully"
        )

    except Exception as error:

        logger.error(
            f"Database initialization failed: {error}"
        )

        raise


# ==================================================
# DUPLICATE CHECK
# ==================================================

def job_exists(
    company,
    role
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM jobs
        WHERE LOWER(company)=LOWER(?)
        AND LOWER(role)=LOWER(?)
        """,
        (
            company,
            role
        )
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# ==================================================
# INSERT JOB
# ==================================================

def insert_job(job):

    try:

        if job_exists(
            job["company"],
            job["role"]
        ):

            logger.info(
                f"Duplicate skipped: "
                f"{job['company']} - {job['role']}"
            )

            return False

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO jobs (

                company,
                role,
                location,
                platform,
                job_link,
                ats_score,
                matched_skills,
                status,
                date_found

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job["company"],
                job["role"],
                job["location"],
                job["platform"],
                job["job_link"],
                job["ats_score"],
                ", ".join(
                    job["matched_skills"]
                ),
                "PENDING",
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        conn.commit()

        conn.close()

        logger.info(
            f"Saved job: "
            f"{job['company']} - {job['role']}"
        )

        return True

    except Exception as error:

        logger.error(
            f"Failed to insert job: {error}"
        )

        return False


# ==================================================
# GET ALL JOBS
# ==================================================

def get_all_jobs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# GET PENDING JOBS
# ==================================================

def get_pending_jobs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE status='PENDING'
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# UPDATE STATUS
# ==================================================

def update_status(
    job_id,
    status
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE jobs

        SET
            status=?,
            date_reviewed=?

        WHERE id=?
        """,
        (
            status,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            job_id
        )
    )

    conn.commit()

    conn.close()

    logger.info(
        f"Job {job_id} updated "
        f"to {status}"
    )


# ==================================================
# DELETE JOB
# ==================================================

def delete_job(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM jobs
        WHERE id=?
        """,
        (job_id,)
    )

    conn.commit()

    conn.close()

    logger.info(
        f"Deleted job {job_id}"
    )


# ==================================================
# COUNT JOBS
# ==================================================

def count_jobs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM jobs
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    initialize_database()

    print(
        f"Database created: "
        f"{DATABASE_FILE}"
    )

    print(
        f"Total Jobs: "
        f"{count_jobs()}"
    )
