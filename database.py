import os

from student import Student

DB_PASSWORD = os.getenv("DB_PASSWORD")


class StudentDatabase:
    def __init__(self):
        self.students = []

    def add_student(self, student_id, name, age):
        if self.find_student_by_id(student_id):
            raise ValueError("Student ID already exists.")

        student = Student(student_id, name, age)
        self.students.append(student)
        return student

    def get_all_students(self):
        return self.students

    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def find_student_by_name(self, name):
        result = []

        for student in self.students:
            if student.name.lower() == name.lower():
                result.append(student)

        return result

    def update_student_name(self, student_id, new_name):
        student = self.find_student_by_id(student_id)

        if student:
            student.update_name(new_name)
            return True

        return False

    def update_student_age(self, student_id, new_age):
        student = self.find_student_by_id(student_id)

        if student:
            student.update_age(new_age)
            return True

        return False

    def delete_student(self, student_id):
        student = self.find_student_by_id(student_id)

        if student:
            self.students.remove(student)
            return True

        return False

    def count_students(self):
        return len(self.students)

    def clear_database(self):
        self.students.clear()

    def sort_by_name(self):
        self.students.sort(key=lambda student: student.name.lower())

    def sort_by_average(self):
        self.students.sort(
            key=lambda student: student.calculate_average(),
            reverse=True,
        )

    def get_passed_students(self):
        return [student for student in self.students if student.is_passed()]

    def get_failed_students(self):
        return [student for student in self.students if not student.is_passed()]

    def get_top_student(self):
        if not self.students:
            return None

        return max(
            self.students,
            key=lambda student: student.calculate_average(),
        )

    def add_marks(self, student_id, subject, marks):
        student = self.find_student_by_id(student_id)

        if student:
            student.add_mark(subject, marks)
            return True

        return False

    def enroll_student(self, student_id, course):
        student = self.find_student_by_id(student_id)

        if student:
            student.enroll_course(course)
            return True

        return False
