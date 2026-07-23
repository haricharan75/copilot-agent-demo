import pytest

from database import StudentDatabase


@pytest.fixture
def database():
    return StudentDatabase()


def test_add_student(database):
    student = database.add_student(101, "Hari", 21)

    assert student.student_id == 101
    assert database.count_students() == 1


def test_duplicate_student(database):
    database.add_student(101, "Hari", 21)

    with pytest.raises(ValueError):
        database.add_student(101, "Charan", 22)


def test_find_student_by_id(database):
    database.add_student(101, "Hari", 21)

    student = database.find_student_by_id(101)

    assert student.name == "Hari"


def test_find_student_by_invalid_id(database):
    assert database.find_student_by_id(999) is None


def test_find_student_by_name(database):
    database.add_student(101, "Hari", 21)

    students = database.find_student_by_name("Hari")

    assert len(students) == 1
    assert students[0].student_id == 101


def test_update_student_name(database):
    database.add_student(101, "Hari", 21)

    result = database.update_student_name(101, "Charan")

    assert result is True
    assert database.find_student_by_id(101).name == "Charan"


def test_update_student_age(database):
    database.add_student(101, "Hari", 21)

    result = database.update_student_age(101, 25)

    assert result is True
    assert database.find_student_by_id(101).age == 25


def test_delete_student(database):
    database.add_student(101, "Hari", 21)

    result = database.delete_student(101)

    assert result is True
    assert database.count_students() == 0


def test_delete_invalid_student(database):
    assert database.delete_student(999) is False


def test_count_students(database):
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)

    assert database.count_students() == 2


def test_clear_database(database):
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)

    database.clear_database()

    assert database.count_students() == 0


def test_add_marks(database):
    database.add_student(101, "Hari", 21)

    result = database.add_marks(101, "Python", 95)

    assert result is True
    assert database.find_student_by_id(101).marks["Python"] == 95


def test_enroll_student(database):
    database.add_student(101, "Hari", 21)

    result = database.enroll_student(101, "Python")

    assert result is True
    assert "Python" in database.find_student_by_id(101).courses


def test_get_passed_students(database):
    student = database.add_student(101, "Hari", 21)

    student.add_mark("Python", 80)

    passed = database.get_passed_students()

    assert len(passed) == 1


def test_get_failed_students(database):
    student = database.add_student(101, "Hari", 21)

    student.add_mark("Python", 20)

    failed = database.get_failed_students()

    assert len(failed) == 1


def test_sort_by_name(database):
    database.add_student(102, "Zara", 20)
    database.add_student(101, "Hari", 21)

    database.sort_by_name()

    students = database.get_all_students()

    assert students[0].name == "Hari"


def test_sort_by_average(database):
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 70)
    second.add_mark("Python", 95)

    database.sort_by_average()

    students = database.get_all_students()

    assert students[0].name == "Charan"


def test_get_top_student(database):
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 75)
    second.add_mark("Python", 95)

    top = database.get_top_student()

    assert top.name == "Charan"


def test_empty_top_student(database):
    assert database.get_top_student() is None
