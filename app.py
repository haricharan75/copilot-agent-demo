from database import StudentDatabase


def display_student(student):
    data = student.display()

    print("\n----------------------------")
    print(f"Student ID : {data['Student ID']}")
    print(f"Name       : {data['Name']}")
    print(f"Age        : {data['Age']}")
    print(f"Courses    : {', '.join(data['Courses']) if data['Courses'] else 'None'}")
    print(f"Marks      : {data['Marks']}")
    print(f"Average    : {data['Average']}")
    print(f"Grade      : {data['Grade']}")
    print(f"Passed     : {data['Passed']}")
    print("----------------------------")


def menu():
    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student by ID")
    print("4. Search Student by Name")
    print("5. Update Student Name")
    print("6. Update Student Age")
    print("7. Delete Student")
    print("8. Add Marks")
    print("9. Enroll Course")
    print("10. Show Top Student")
    print("11. Show Passed Students")
    print("12. Show Failed Students")
    print("13. Sort Students by Name")
    print("14. Sort Students by Average")
    print("15. Count Students")
    print("16. Clear Database")
    print("17. Exit")


def main():
    database = StudentDatabase()

    while True:
        menu()

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                student_id = int(input("Student ID: "))
                name = input("Name: ")
                age = int(input("Age: "))

                database.add_student(student_id, name, age)
                print("Student added successfully.")

            elif choice == "2":
                students = database.get_all_students()

                if not students:
                    print("No students found.")
                else:
                    for student in students:
                        display_student(student)

            elif choice == "3":
                student_id = int(input("Enter Student ID: "))

                student = database.find_student_by_id(student_id)

                if student:
                    display_student(student)
                else:
                    print("Student not found.")

            elif choice == "4":
                name = input("Enter Student Name: ")

                students = database.find_student_by_name(name)

                if students:
                    for student in students:
                        display_student(student)
                else:
                    print("Student not found.")

            elif choice == "5":
                student_id = int(input("Student ID: "))
                new_name = input("New Name: ")

                if database.update_student_name(student_id, new_name):
                    print("Student updated.")
                else:
                    print("Student not found.")

            elif choice == "6":
                student_id = int(input("Student ID: "))
                new_age = int(input("New Age: "))

                if database.update_student_age(student_id, new_age):
                    print("Age updated.")
                else:
                    print("Student not found.")

            elif choice == "7":
                student_id = int(input("Student ID: "))

                if database.delete_student(student_id):
                    print("Student deleted.")
                else:
                    print("Student not found.")

            elif choice == "8":
                student_id = int(input("Student ID: "))
                subject = input("Subject: ")
                marks = float(input("Marks: "))

                if database.add_marks(student_id, subject, marks):
                    print("Marks added.")
                else:
                    print("Student not found.")

            elif choice == "9":
                student_id = int(input("Student ID: "))
                course = input("Course Name: ")

                if database.enroll_student(student_id, course):
                    print("Course enrolled.")
                else:
                    print("Student not found.")

            elif choice == "10":
                student = database.get_top_student()

                if student:
                    display_student(student)
                else:
                    print("No students available.")

            elif choice == "11":
                students = database.get_passed_students()

                if students:
                    for student in students:
                        display_student(student)
                else:
                    print("No passed students.")

            elif choice == "12":
                students = database.get_failed_students()

                if students:
                    for student in students:
                        display_student(student)
                else:
                    print("No failed students.")

            elif choice == "13":
                database.sort_by_name()
                print("Students sorted by name.")

            elif choice == "14":
                database.sort_by_average()
                print("Students sorted by average.")

            elif choice == "15":
                print(f"Total Students: {database.count_students()}")

            elif choice == "16":
                database.clear_database()
                print("Database cleared.")

            elif choice == "17":
                print("Exiting...")
                break

            else:
                print("Invalid choice.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
