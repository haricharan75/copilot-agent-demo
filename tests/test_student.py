import csv

import pytest

from student import CSV_HEADERS, Student, export_students_to_csv


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as csv_file:
        return list(csv.reader(csv_file))


def test_student_creation():
    student = Student(101, "Hari", 21)

    assert student.student_id == 101
    assert student.name == "Hari"
    assert student.age == 21
    assert student.courses == []
    assert student.marks == {}


def test_update_name():
    student = Student(101, "Hari", 21)

    student.update_name("Charan")

    assert student.name == "Charan"


def test_update_name_invalid():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_name("")


def test_update_name_whitespace_only():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_name("   ")


def test_update_name_none():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_name(None)


def test_update_age():
    student = Student(101, "Hari", 21)

    student.update_age(25)

    assert student.age == 25


def test_update_age_invalid():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(2)


def test_update_age_too_high():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(150)


def test_update_age_boundary_values():
    student = Student(101, "Hari", 21)

    student.update_age(5)
    assert student.age == 5

    student.update_age(100)
    assert student.age == 100


def test_update_age_non_integer():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age("twenty")


def test_student_creation_invalid_id_negative():
    with pytest.raises(ValueError):
        Student(-1, "Hari", 21)


def test_student_creation_invalid_id_zero():
    with pytest.raises(ValueError):
        Student(0, "Hari", 21)


def test_student_creation_invalid_id_non_integer():
    with pytest.raises(ValueError):
        Student("abc", "Hari", 21)


def test_student_creation_missing_name():
    with pytest.raises(ValueError):
        Student(101, "", 21)


def test_student_creation_missing_age():
    with pytest.raises(ValueError):
        Student(101, "Hari", None)


def test_student_creation_invalid_age():
    with pytest.raises(ValueError):
        Student(101, "Hari", 200)


def test_enroll_course():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")

    assert "Python" in student.courses


def test_remove_course():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.remove_course("Python")

    assert "Python" not in student.courses


def test_add_marks():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 95)

    assert student.marks["Python"] == 95


def test_remove_marks():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)
    student.remove_mark("Python")

    assert "Python" not in student.marks


def test_invalid_marks():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.add_mark("Python", 120)


def test_invalid_marks_negative():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.add_mark("Python", -5)


def test_invalid_marks_non_numeric():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.add_mark("Python", "ninety")


def test_remove_marks_nonexistent_subject():
    student = Student(101, "Hari", 21)

    student.remove_mark("Python")

    assert "Python" not in student.marks


def test_remove_course_nonexistent_course():
    student = Student(101, "Hari", 21)

    student.remove_course("Python")

    assert "Python" not in student.courses


def test_enroll_course_duplicate():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.enroll_course("Python")

    assert student.courses.count("Python") == 1


def test_average():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)
    student.add_mark("Java", 90)

    assert student.calculate_average() == 85


def test_grade():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)
    student.add_mark("Java", 90)

    assert student.get_grade() == "A+"


def test_average_with_no_marks():
    student = Student(101, "Hari", 21)

    assert student.calculate_average() == 0


@pytest.mark.parametrize(
    "mark, expected_grade",
    [
        (95, "A+"),
        (85, "A"),
        (75, "B"),
        (65, "C"),
        (55, "D"),
        (40, "F"),
    ],
)
def test_grade_boundaries(mark, expected_grade):
    student = Student(101, "Hari", 21)

    student.add_mark("Python", mark)

    assert student.get_grade() == expected_grade


def test_passed():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)

    assert student.is_passed() is True


def test_failed():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 20)

    assert student.is_passed() is False


def test_display():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)

    data = student.display()

    assert data["Student ID"] == 101
    assert data["Name"] == "Hari"
    assert data["Grade"] == "A+"


def test_string_method():
    student = Student(101, "Hari", 21)

    text = str(student)

    assert "Hari" in text
    assert "101" in text


def test_get_grade_rows():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)
    student.add_mark("Java", 90)

    rows = student.get_grade_rows()

    assert rows == [
        [101, "Hari", 21, "Java", 90, 85.0, "A", True],
        [101, "Hari", 21, "Python", 80, 85.0, "A", True],
    ]


def test_get_grade_rows_sorted_by_subject():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)
    student.add_mark("Java", 90)
    student.add_mark("C", 70)

    subjects = [row[3] for row in student.get_grade_rows()]

    assert subjects == ["C", "Java", "Python"]


def test_get_grade_rows_with_no_marks():
    student = Student(101, "Hari", 21)

    rows = student.get_grade_rows()

    assert rows == [[101, "Hari", 21, "", "", 0, "F", False]]


def test_export_grades_to_csv(tmp_path):
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)
    student.add_mark("Java", 90)

    path = tmp_path / "grades.csv"
    student.export_grades_to_csv(str(path))

    assert read_csv(path) == [
        list(CSV_HEADERS),
        ["101", "Hari", "21", "Java", "90", "85.0", "A", "True"],
        ["101", "Hari", "21", "Python", "80", "85.0", "A", "True"],
    ]


def test_export_grades_to_csv_returns_path(tmp_path):
    student = Student(101, "Hari", 21)

    path = tmp_path / "grades.csv"

    assert student.export_grades_to_csv(str(path)) == str(path)


def test_export_grades_to_csv_with_no_marks(tmp_path):
    student = Student(101, "Hari", 21)

    path = tmp_path / "grades.csv"
    student.export_grades_to_csv(str(path))

    rows = read_csv(path)

    assert rows[0] == list(CSV_HEADERS)
    assert rows[1] == ["101", "Hari", "21", "", "", "0", "F", "False"]


def test_export_grades_to_csv_overwrites_existing_file(tmp_path):
    student = Student(101, "Hari", 21)
    student.add_mark("Python", 80)

    path = tmp_path / "grades.csv"
    path.write_text("stale content\n", encoding="utf-8")

    student.export_grades_to_csv(str(path))

    rows = read_csv(path)

    assert rows[0] == list(CSV_HEADERS)
    assert len(rows) == 2


def test_export_grades_to_csv_escapes_commas_in_name(tmp_path):
    student = Student(101, "Hari, Charan", 21)
    student.add_mark("Python", 80)

    path = tmp_path / "grades.csv"
    student.export_grades_to_csv(str(path))

    assert read_csv(path)[1][1] == "Hari, Charan"


@pytest.mark.parametrize("bad_path", ["", "   ", None, 123])
def test_export_grades_to_csv_invalid_path(bad_path):
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.export_grades_to_csv(bad_path)


def test_export_grades_to_csv_missing_directory(tmp_path):
    student = Student(101, "Hari", 21)

    path = tmp_path / "missing" / "grades.csv"

    with pytest.raises(OSError):
        student.export_grades_to_csv(str(path))


def test_export_students_to_csv(tmp_path):
    first = Student(101, "Hari", 21)
    first.add_mark("Python", 80)

    second = Student(102, "Charan", 22)
    second.add_mark("Java", 40)

    path = tmp_path / "grades.csv"
    export_students_to_csv([first, second], str(path))

    assert read_csv(path) == [
        list(CSV_HEADERS),
        ["101", "Hari", "21", "Python", "80", "80.0", "A", "True"],
        ["102", "Charan", "22", "Java", "40", "40.0", "F", "False"],
    ]


def test_export_students_to_csv_empty_list(tmp_path):
    path = tmp_path / "grades.csv"

    export_students_to_csv([], str(path))

    assert read_csv(path) == [list(CSV_HEADERS)]


def test_export_students_to_csv_invalid_path():
    with pytest.raises(ValueError):
        export_students_to_csv([Student(101, "Hari", 21)], "")
