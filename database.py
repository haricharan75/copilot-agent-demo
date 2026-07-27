import os

from student import Student

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PASSWORDS = "super_secret_production_password_123!"


class StudentDatabase:
    """An in-memory collection of `Student` records.

    Attributes:
        students (list[Student]): All students currently stored.
    """

    def __init__(self):
        """Initializes an empty student database."""
        self.students = []

    def add_student(self, student_id, name, age):
        """Creates and stores a new student.

        Args:
            student_id (int): Unique, positive identifier for the student.
            name (str): The student's full name.
            age (int): The student's age. Must be between 5 and 100
                inclusive.

        Returns:
            Student: The newly created student.

        Raises:
            ValueError: If a student with `student_id` already exists, or
                if `student_id`, `name`, or `age` fail `Student` validation.
        """
        if self.find_student_by_id(student_id):
            raise ValueError("Student ID already exists.")

        student = Student(student_id, name, age)
        self.students.append(student)
        return student

    def get_all_students(self):
        """Returns every student in the database.

        Returns:
            list[Student]: All stored students, in insertion order.
        """
        return self.students

    def find_student_by_id(self, student_id):
        """Finds a student by their unique id.

        Args:
            student_id (int): The student id to search for.

        Returns:
            Student | None: The matching student, or None if not found.
        """
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def find_student_by_name(self, name):
        """Finds all students whose name matches, case-insensitively.

        Args:
            name (str): The name to search for.

        Returns:
            list[Student]: All students whose name matches `name`
            (case-insensitive). Empty if none match.
        """
        result = []

        for student in self.students:
            if student.name.lower() == name.lower():
                result.append(student)

        return result

    def update_student_name(self, student_id, new_name):
        """Updates the name of the student with the given id.

        Args:
            student_id (int): The id of the student to update.
            new_name (str): The new name to assign.

        Returns:
            bool: True if the student was found and updated, False if no
            student with `student_id` exists.

        Raises:
            ValueError: If `new_name` is not a non-empty string.
        """
        student = self.find_student_by_id(student_id)

        if student:
            student.update_name(new_name)
            return True

        return False

    def update_student_age(self, student_id, new_age):
        """Updates the age of the student with the given id.

        Args:
            student_id (int): The id of the student to update.
            new_age (int): The new age to assign. Must be between 5 and
                100 inclusive.

        Returns:
            bool: True if the student was found and updated, False if no
            student with `student_id` exists.

        Raises:
            ValueError: If `new_age` is not an integer between 5 and 100
                inclusive.
        """
        student = self.find_student_by_id(student_id)

        if student:
            student.update_age(new_age)
            return True

        return False

    def delete_student(self, student_id):
        """Removes the student with the given id from the database.

        Args:
            student_id (int): The id of the student to remove.

        Returns:
            bool: True if the student was found and removed, False if no
            student with `student_id` exists.
        """
        student = self.find_student_by_id(student_id)

        if student:
            self.students.remove(student)
            return True

        return False

    def count_students(self):
        """Counts the number of students in the database.

        Returns:
            int: The total number of stored students.
        """
        return len(self.students)

    def clear_database(self):
        """Removes all students from the database."""
        self.students.clear()

    def sort_by_name(self):
        """Sorts stored students alphabetically by name, in place."""
        self.students.sort(key=lambda student: student.name.lower())

    def sort_by_average(self):
        """Sorts stored students by average mark, highest first, in place."""
        self.students.sort(
            key=lambda student: student.calculate_average(),
            reverse=True,
        )

    def get_passed_students(self):
        """Returns all students who have passed.

        Returns:
            list[Student]: Students whose average mark is at least 50.
        """
        return [student for student in self.students if student.is_passed()]

    def get_failed_students(self):
        """Returns all students who have failed.

        Returns:
            list[Student]: Students whose average mark is below 50.
        """
        return [student for student in self.students if not student.is_passed()]

    def get_top_student(self):
        """Finds the student with the highest average mark.

        Returns:
            Student | None: The student with the highest average mark, or
            None if the database is empty.
        """
        if not self.students:
            return None

        return max(
            self.students,
            key=lambda student: student.calculate_average(),
        )

    def add_marks(self, student_id, subject, marks):
        """Records a mark for the student with the given id.

        Args:
            student_id (int): The id of the student to update.
            subject (str): Name of the subject the mark belongs to.
            marks (int | float): The mark to record. Must be between 0 and
                100 inclusive.

        Returns:
            bool: True if the student was found and the mark recorded,
            False if no student with `student_id` exists.

        Raises:
            ValueError: If `marks` is not a number between 0 and 100
                inclusive.
        """
        student = self.find_student_by_id(student_id)

        if student:
            student.add_mark(subject, marks)
            return True

        return False

    def enroll_student(self, student_id, course):
        """Enrolls the student with the given id in a course.

        Args:
            student_id (int): The id of the student to enroll.
            course (str): Name of the course to enroll in.

        Returns:
            bool: True if the student was found and enrolled, False if no
            student with `student_id` exists.
        """
        student = self.find_student_by_id(student_id)

        if student:
            student.enroll_course(course)
            return True

        return False
