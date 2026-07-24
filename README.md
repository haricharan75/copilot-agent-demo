# Student Management System

A Python-based Student Management System developed for learning DevSecOps practices.

## Features

- Add Student
- Update Student
- Delete Student
- Search Student
- Enroll Courses
- Add Marks
- Calculate Average
- Grade Calculation
- Pass/Fail Status
- Sort Students
- View Top Student

## Technologies

- Python
- Pytest
- Black
- Pylint
- Bandit
- GitHub Actions

## Setup

Create and activate a virtual environment, then install dependencies from
`requirements.txt`.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in real values before running the app:

```bash
cp .env.example .env
```

## Run

```bash
python app.py
```

## Run Tests

With the virtual environment activated, run the test suite with pytest:

```bash
pytest -v
```

## Run Coverage

```bash
pytest --cov=.
```

## Format Code

```bash
black .
```

## Run Pylint

```bash
pylint student.py database.py app.py
```

## Run Bandit

```bash
bandit -r .
```