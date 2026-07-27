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


def test_add_student_returns_the_stored_instance(database):
    student = database.add_student(101, "Hari", 21)

    assert database.find_student_by_id(101) is student


def test_add_student_with_invalid_id_is_not_stored(database):
    with pytest.raises(ValueError):
        database.add_student(-1, "Hari", 21)

    assert database.count_students() == 0


def test_add_student_with_invalid_age_is_not_stored(database):
    with pytest.raises(ValueError):
        database.add_student(101, "Hari", 200)

    assert database.count_students() == 0


def test_add_student_with_missing_name_is_not_stored(database):
    with pytest.raises(ValueError):
        database.add_student(101, "", 21)

    assert database.count_students() == 0


def test_duplicate_student_does_not_overwrite_existing_record(database):
    database.add_student(101, "Hari", 21)

    with pytest.raises(ValueError):
        database.add_student(101, "Charan", 22)

    assert database.count_students() == 1
    assert database.find_student_by_id(101).name == "Hari"


def test_get_all_students_on_empty_database(database):
    assert database.get_all_students() == []


def test_get_all_students_preserves_insertion_order(database):
    database.add_student(102, "Zara", 20)
    database.add_student(101, "Hari", 21)

    names = [student.name for student in database.get_all_students()]

    assert names == ["Zara", "Hari"]


def test_count_students_on_empty_database(database):
    assert database.count_students() == 0


def test_clear_empty_database_is_a_no_op(database):
    database.clear_database()

    assert database.count_students() == 0


@pytest.mark.parametrize("search_term", ["hari", "HARI", "HaRi"])
def test_find_student_by_name_is_case_insensitive(database, search_term):
    database.add_student(101, "Hari", 21)

    students = database.find_student_by_name(search_term)

    assert len(students) == 1
    assert students[0].student_id == 101


def test_find_student_by_name_with_no_match(database):
    database.add_student(101, "Hari", 21)

    assert database.find_student_by_name("Charan") == []


def test_find_student_by_name_on_empty_database(database):
    assert database.find_student_by_name("Hari") == []


def test_find_student_by_name_returns_all_matches(database):
    database.add_student(101, "Hari", 21)
    database.add_student(102, "hari", 22)
    database.add_student(103, "Charan", 23)

    students = database.find_student_by_name("Hari")

    assert [student.student_id for student in students] == [101, 102]


def test_update_name_for_missing_student(database):
    assert database.update_student_name(999, "Charan") is False


def test_update_name_with_invalid_value_leaves_record_unchanged(database):
    database.add_student(101, "Hari", 21)

    with pytest.raises(ValueError):
        database.update_student_name(101, "")

    assert database.find_student_by_id(101).name == "Hari"


def test_update_age_for_missing_student(database):
    assert database.update_student_age(999, 25) is False


def test_update_age_with_invalid_value_leaves_record_unchanged(database):
    database.add_student(101, "Hari", 21)

    with pytest.raises(ValueError):
        database.update_student_age(101, 200)

    assert database.find_student_by_id(101).age == 21


def test_add_marks_for_missing_student(database):
    assert database.add_marks(999, "Python", 90) is False


def test_add_marks_with_invalid_value_records_nothing(database):
    database.add_student(101, "Hari", 21)

    with pytest.raises(ValueError):
        database.add_marks(101, "Python", 150)

    assert database.find_student_by_id(101).marks == {}


def test_add_marks_overwrites_existing_subject(database):
    database.add_student(101, "Hari", 21)

    database.add_marks(101, "Python", 60)
    result = database.add_marks(101, "Python", 85)

    assert result is True
    assert database.find_student_by_id(101).marks == {"Python": 85}


def test_enroll_student_for_missing_student(database):
    assert database.enroll_student(999, "Python") is False


def test_enroll_student_twice_does_not_duplicate_course(database):
    database.add_student(101, "Hari", 21)

    database.enroll_student(101, "Python")
    result = database.enroll_student(101, "Python")

    assert result is True
    assert database.find_student_by_id(101).courses == ["Python"]


def test_delete_student_only_removes_the_target(database):
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)

    database.delete_student(101)

    assert database.count_students() == 1
    assert database.find_student_by_id(101) is None
    assert database.find_student_by_id(102) is not None


def test_delete_student_twice_returns_false_the_second_time(database):
    database.add_student(101, "Hari", 21)

    assert database.delete_student(101) is True
    assert database.delete_student(101) is False


def test_passed_and_failed_students_on_empty_database(database):
    assert database.get_passed_students() == []
    assert database.get_failed_students() == []


def test_student_without_marks_counts_as_failed(database):
    database.add_student(101, "Hari", 21)

    assert database.get_passed_students() == []
    assert len(database.get_failed_students()) == 1


def test_student_on_the_pass_boundary_counts_as_passed(database):
    student = database.add_student(101, "Hari", 21)

    student.add_mark("Python", 50)

    assert len(database.get_passed_students()) == 1
    assert database.get_failed_students() == []


def test_passed_and_failed_students_partition_the_database(database):
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)
    third = database.add_student(103, "Zara", 23)

    first.add_mark("Python", 80)
    second.add_mark("Python", 20)
    third.add_mark("Python", 95)

    passed = [student.student_id for student in database.get_passed_students()]
    failed = [student.student_id for student in database.get_failed_students()]

    assert passed == [101, 103]
    assert failed == [102]


def test_sort_by_name_ignores_case(database):
    database.add_student(101, "Banana", 21)
    database.add_student(102, "apple", 22)

    database.sort_by_name()

    names = [student.name for student in database.get_all_students()]

    assert names == ["apple", "Banana"]


def test_sort_by_name_on_empty_database(database):
    database.sort_by_name()

    assert database.get_all_students() == []


def test_sort_by_average_places_students_without_marks_last(database):
    first = database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)
    third = database.add_student(103, "Zara", 23)

    first.add_mark("Python", 60)
    third.add_mark("Python", 95)

    database.sort_by_average()

    names = [student.name for student in database.get_all_students()]

    assert names == ["Zara", "Hari", "Charan"]


def test_sort_by_average_on_empty_database(database):
    database.sort_by_average()

    assert database.get_all_students() == []


def test_get_top_student_with_a_tie_returns_the_first_added(database):
    first = database.add_student(101, "Hari", 21)
    second = database.add_student(102, "Charan", 22)

    first.add_mark("Python", 90)
    second.add_mark("Python", 90)

    assert database.get_top_student().student_id == 101


def test_get_top_student_when_nobody_has_marks(database):
    database.add_student(101, "Hari", 21)
    database.add_student(102, "Charan", 22)

    assert database.get_top_student().student_id == 101


def test_get_top_student_after_clearing_the_database(database):
    student = database.add_student(101, "Hari", 21)

    student.add_mark("Python", 90)
    database.clear_database()

    assert database.get_top_student() is None
