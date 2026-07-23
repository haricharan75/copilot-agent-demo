import pytest

from student import Student


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


def test_update_age():
    student = Student(101, "Hari", 21)

    student.update_age(25)

    assert student.age == 25


def test_update_age_invalid():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(2)


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
