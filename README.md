# Job Assistant V2

## Overview

Job Assistant V2 is a Python-based job discovery and ATS ranking platform designed for Cloud, DevOps, AWS, Linux, Platform Engineering, and Site Reliability Engineering roles.

The application automatically:

* Parses resume skills
* Searches multiple job sources
* Filters jobs by location and experience
* Calculates ATS match scores
* Stores jobs in SQLite
* Exports jobs to Excel
* Maintains approval status
* Opens approved jobs for manual review and application

The system is designed to help job seekers efficiently identify relevant opportunities without manually searching multiple job platforms every day.

---

## Features

### Resume Parsing

Extracts technical skills from a PDF resume.

Supported skills include:

* AWS
* Terraform
* Docker
* Kubernetes
* Linux
* Python
* Jenkins
* GitLab
* Ansible
* Shell Scripting
* Networking
* CloudWatch

---

### ATS Matching

Compares:

```text
Resume Skills
vs
Job Skills
```

and calculates an ATS compatibility score.

Example:

```text
Resume:
AWS, Terraform, Linux, Docker

Job:
AWS, Linux, Docker, Kubernetes

ATS Score:
75%
```

---

### Job Filtering

Filters jobs using:

#### Role Filters

* Cloud Engineer
* DevOps Engineer
* AWS Engineer
* Linux Administrator
* Platform Engineer
* Site Reliability Engineer
* Infrastructure Engineer
* Cloud Support Engineer

#### Location Filters

* Chennai
* Bengaluru
* Hyderabad
* Coimbatore
* Remote

#### Experience Filters

* 0 Years
* 1 Year
* 2 Years

---

### SQLite Storage

All discovered jobs are stored in:

```text
data/jobs.db
```

Benefits:

* Fast
* Lightweight
* No server required
* Portable

---

### Excel Export

Exports jobs into:

```text
data/jobs.xlsx
```

Columns:

* Company
* Role
* Location
* Platform
* ATS Score
* Job Link
* Status
* Date Found

---

### Approval Workflow

Every discovered job is initially marked as:

```text
PENDING
```

User options:

```text
Approve
Reject
Open Job Link
```

Approved jobs remain available for review and application.

---

### Logging

Application logs are written to:

```text
logs/app.log
```

Logs include:

* Job searches
* ATS calculations
* Errors
* Database operations
* Export operations

---

## Project Structure

```text
job-assistant/
│
├── config/
│   ├── keywords.yaml
│   └── settings.yaml
│
├── data/
│   ├── jobs.db
│   └── jobs.xlsx
│
├── logs/
│   └── app.log
│
├── resume/
│   └── resume.pdf
│
├── src/
│   │
│   ├── main.py
│   ├── ats_matcher.py
│   ├── resume_parser.py
│   ├── job_filter.py
│   │
│   ├── approval/
│   │   └── approval_manager.py
│   │
│   ├── storage/
│   │   ├── sqlite_store.py
│   │   └── excel_exporter.py
│   │
│   ├── job_sources/
│   │   ├── remotive_source.py
│   │   ├── greenhouse_source.py
│   │   └── lever_source.py
│   │
│   └── utils/
│       ├── config_loader.py
│       └── logger.py
│
├── run.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/Paramesh05-svg/job-assistant.git
cd job-assistant
```

Create virtual environment:

```bash
py -3.12 -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Update:

```text
config/keywords.yaml
```

Example:

```yaml
job_titles:
  - Cloud Engineer
  - DevOps Engineer
  - AWS Engineer

locations:
  - Chennai
  - Bengaluru
  - Hyderabad
  - Remote

experience:
  min: 0
  max: 2
```

---

## Running

Run application:

```bash
py -3.12 run.py
```

---

## Windows Startup Automation

Create:

```text
start_job_assistant.bat
```

Example:

```bat
@echo off

cd /d C:\Users\dell\job-assistant

py -3.12 run.py

pause
```

Add shortcut to:

```text
shell:startup
```

Windows will automatically launch the application after login.

---

## Future Enhancements

Planned improvements:

* Streamlit dashboard
* Email notifications
* Resume customization
* Cover letter generation
* AI-powered ATS analysis
* Duplicate job detection
* Scheduled job searches
* Job trend analytics

---

## Author

Parameshwari

Cloud Engineer | AWS | Linux | Terraform | DevOps

GitHub:
https://github.com/Paramesh05-svg
