import csv

CSV_HEADERS = (
    "Student ID",
    "Name",
    "Age",
    "Subject",
    "Mark",
    "Average",
    "Grade",
    "Passed",
)


class Student:
    """Represents a single student and their academic record.

    Attributes:
        student_id (int): Unique, positive identifier for the student.
        name (str): The student's full name.
        age (int): The student's age in years (5-100 inclusive).
        courses (list[str]): Names of courses the student is enrolled in.
        marks (dict[str, int | float]): Mapping of subject name to mark
            (0-100 inclusive).
    """

    GRADE_THRESHOLDS = (
        (90, "A+"),
        (80, "A"),
        (70, "B"),
        (60, "C"),
        (50, "D"),
    )

    def __init__(self, student_id, name, age):
        """Initializes a Student with an id, name, and age.

        Args:
            student_id (int): Unique, positive identifier for the student.
            name (str): The student's full name. Cannot be empty or blank.
            age (int): The student's age. Must be between 5 and 100 inclusive.

        Raises:
            ValueError: If `student_id` is not a positive integer, `name` is
                not a non-empty string, or `age` is not an integer between
                5 and 100 inclusive.
        """
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")
        self.student_id = student_id
        self.courses = []
        self.marks = {}
        self.update_name(name)
        self.update_age(age)

    def update_name(self, new_name):
        """Updates the student's name.

        Args:
            new_name (str): The new name to assign. Cannot be empty or
                consist only of whitespace.

        Raises:
            ValueError: If `new_name` is not a string, or is empty/blank.
        """
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("Name cannot be empty.")
        self.name = new_name

    def update_age(self, new_age):
        """Updates the student's age.

        Args:
            new_age (int): The new age to assign. Must be between 5 and 100
                inclusive.

        Raises:
            ValueError: If `new_age` is not an integer, or is outside the
                5-100 range.
        """
        if not isinstance(new_age, int) or new_age < 5 or new_age > 100:
            raise ValueError("Invalid age.")
        self.age = new_age

    def enroll_course(self, course_name):
        """Enrolls the student in a course, if not already enrolled.

        Args:
            course_name (str): Name of the course to enroll in.
        """
        if course_name not in self.courses:
            self.courses.append(course_name)

    def remove_course(self, course_name):
        """Removes the student from a course, if currently enrolled.

        Args:
            course_name (str): Name of the course to remove.
        """
        if course_name in self.courses:
            self.courses.remove(course_name)

    def add_mark(self, subject, mark):
        """Records or updates the student's mark for a subject.

        Args:
            subject (str): Name of the subject the mark belongs to.
            mark (int | float): The mark to record. Must be between 0 and
                100 inclusive.

        Raises:
            ValueError: If `mark` is not a number, or is outside the 0-100
                range.
        """
        if not isinstance(mark, (int, float)) or mark < 0 or mark > 100:
            raise ValueError("Marks should be between 0 and 100.")
        self.marks[subject] = mark

    def remove_mark(self, subject):
        """Removes a recorded mark for a subject, if one exists.

        Args:
            subject (str): Name of the subject whose mark should be removed.
        """
        if subject in self.marks:
            del self.marks[subject]

    def calculate_average(self):
        """Calculates the student's average mark across all subjects.

        Returns:
            int | float: The average of all recorded marks, or 0 if no
            marks have been recorded.
        """
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def get_grade(self):
        """Determines the student's letter grade from their average mark.

        Returns:
            str: One of "A+", "A", "B", "C", "D", or "F", based on where
            the average mark falls against `GRADE_THRESHOLDS`.
        """
        average = self.calculate_average()
        for threshold, grade in self.GRADE_THRESHOLDS:
            if average >= threshold:
                return grade
        return "F"

    def is_passed(self):
        """Determines whether the student has passed.

        Returns:
            bool: True if the average mark is at least 50, False otherwise.
        """
        return self.calculate_average() >= 50

    def display(self):
        """Builds a summary of the student's record.

        Returns:
            dict: A mapping with keys "Student ID", "Name", "Age",
            "Courses", "Marks", "Average", "Grade", and "Passed",
            summarizing the student's current state.
        """
        return {
            "Student ID": self.student_id,
            "Name": self.name,
            "Age": self.age,
            "Courses": self.courses,
            "Marks": self.marks,
            "Average": round(self.calculate_average(), 2),
            "Grade": self.get_grade(),
            "Passed": self.is_passed(),
        }

    def get_grade_rows(self):
        """Builds the CSV rows describing this student's grades.

        Produces one row per recorded subject, ordered by subject name so
        that exports are stable regardless of the order marks were added.
        A student with no recorded marks still yields a single row, with
        empty "Subject" and "Mark" values, so they are not silently
        omitted from an export.

        Returns:
            list[list]: Rows aligned with `CSV_HEADERS`.
        """
        average = round(self.calculate_average(), 2)
        grade = self.get_grade()
        passed = self.is_passed()

        if not self.marks:
            return [
                [
                    self.student_id,
                    self.name,
                    self.age,
                    "",
                    "",
                    average,
                    grade,
                    passed,
                ]
            ]

        return [
            [
                self.student_id,
                self.name,
                self.age,
                subject,
                self.marks[subject],
                average,
                grade,
                passed,
            ]
            for subject in sorted(self.marks)
        ]

    def export_grades_to_csv(self, file_path):
        """Writes this student's grades to a CSV file.

        The file is created (or overwritten) with a header row followed by
        the rows from `get_grade_rows`.

        Args:
            file_path (str): Path of the CSV file to write. Cannot be empty
                or consist only of whitespace.

        Returns:
            str: The `file_path` that was written.

        Raises:
            ValueError: If `file_path` is not a non-empty string.
            OSError: If the file cannot be opened for writing.
        """
        return _write_csv(file_path, self.get_grade_rows())

    def __str__(self):
        """Builds a concise, human-readable representation of the student.

        Returns:
            str: A string of the form
            "Student(id=..., name=..., age=..., grade=...)".
        """
        return (
            f"Student("
            f"id={self.student_id}, "
            f"name={self.name}, "
            f"age={self.age}, "
            f"grade={self.get_grade()})"
        )


def _write_csv(file_path, rows):
    """Writes a header row and `rows` to a CSV file.

    Args:
        file_path (str): Path of the CSV file to write. Cannot be empty or
            consist only of whitespace.
        rows (list[list]): Rows aligned with `CSV_HEADERS`.

    Returns:
        str: The `file_path` that was written.

    Raises:
        ValueError: If `file_path` is not a non-empty string.
        OSError: If the file cannot be opened for writing.
    """
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError("File path cannot be empty.")

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(CSV_HEADERS)
        writer.writerows(rows)

    return file_path


def export_students_to_csv(students, file_path):
    """Writes the grades of several students to a single CSV file.

    Args:
        students (iterable[Student]): Students whose grades to export.
        file_path (str): Path of the CSV file to write. Cannot be empty or
            consist only of whitespace.

    Returns:
        str: The `file_path` that was written.

    Raises:
        ValueError: If `file_path` is not a non-empty string.
        OSError: If the file cannot be opened for writing.
    """
    rows = []

    for student in students:
        rows.extend(student.get_grade_rows())

    return _write_csv(file_path, rows)
