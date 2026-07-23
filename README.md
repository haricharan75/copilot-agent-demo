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

## Run

```bash
python app.py
```

## Run Tests

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