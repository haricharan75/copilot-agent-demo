class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.courses = []
        self.marks = {}

    def update_name(self, new_name):
        if not new_name.strip():
            raise ValueError("Name cannot be empty.")
        self.name = new_name

    def update_age(self, new_age):
        if new_age < 5 or new_age > 100:
            raise ValueError("Invalid age.")
        self.age = new_age

    def enroll_course(self, course_name):
        if course_name not in self.courses:
            self.courses.append(course_name)

    def remove_course(self, course_name):
        if course_name in self.courses:
            self.courses.remove(course_name)

    def add_mark(self, subject, mark):
        if mark < 0 or mark > 100:
            raise ValueError("Marks should be between 0 and 100.")
        self.marks[subject] = mark

    def remove_mark(self, subject):
        if subject in self.marks:
            del self.marks[subject]

    def calculate_average(self):
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def get_grade(self):
        average = self.calculate_average()

        if average >= 90:
            return "A+"
        if average >= 80:
            return "A"
        if average >= 70:
            return "B"
        if average >= 60:
            return "C"
        if average >= 50:
            return "D"
        return "F"

    def is_passed(self):
        return self.calculate_average() >= 50

    def display(self):
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

    def __str__(self):
        return (
            f"Student("
            f"id={self.student_id}, "
            f"name={self.name}, "
            f"age={self.age}, "
            f"grade={self.get_grade()})"
        )
