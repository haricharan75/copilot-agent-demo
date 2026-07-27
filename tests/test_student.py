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


def test_student_creation_invalid_id_float():
    with pytest.raises(ValueError):
        Student(101.0, "Hari", 21)


def test_student_creation_invalid_id_none():
    with pytest.raises(ValueError):
        Student(None, "Hari", 21)


def test_student_creation_age_boundary_values():
    youngest = Student(101, "Hari", 5)
    oldest = Student(102, "Charan", 100)

    assert youngest.age == 5
    assert oldest.age == 100


def test_student_creation_age_just_outside_boundaries():
    with pytest.raises(ValueError):
        Student(101, "Hari", 4)

    with pytest.raises(ValueError):
        Student(102, "Charan", 101)


def test_student_creation_age_float_rejected():
    with pytest.raises(ValueError):
        Student(101, "Hari", 21.0)


def test_student_creation_non_string_name():
    with pytest.raises(ValueError):
        Student(101, 12345, 21)


def test_students_do_not_share_courses_or_marks():
    first = Student(101, "Hari", 21)
    second = Student(102, "Charan", 22)

    first.enroll_course("Python")
    first.add_mark("Python", 90)

    assert second.courses == []
    assert second.marks == {}


def test_update_name_preserves_surrounding_whitespace():
    student = Student(101, "Hari", 21)

    student.update_name("  Charan  ")

    assert student.name == "  Charan  "


def test_update_name_non_string_rejected():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_name(12345)


def test_update_name_failure_leaves_name_unchanged():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_name("")

    assert student.name == "Hari"


def test_update_age_just_outside_boundaries():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(4)

    with pytest.raises(ValueError):
        student.update_age(101)


def test_update_age_float_rejected():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(25.0)


def test_update_age_none_rejected():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(None)


def test_update_age_failure_leaves_age_unchanged():
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.update_age(150)

    assert student.age == 21


def test_enroll_multiple_courses_preserves_order():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.enroll_course("Java")
    student.enroll_course("Go")

    assert student.courses == ["Python", "Java", "Go"]


def test_remove_course_leaves_other_courses_intact():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.enroll_course("Java")
    student.enroll_course("Go")

    student.remove_course("Java")

    assert student.courses == ["Python", "Go"]


def test_remove_course_from_empty_list_is_a_no_op():
    student = Student(101, "Hari", 21)

    student.remove_course("Python")

    assert student.courses == []


def test_remove_course_twice_is_a_no_op():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.remove_course("Python")
    student.remove_course("Python")

    assert student.courses == []


@pytest.mark.parametrize("mark", [0, 100, 0.0, 100.0, 49.5])
def test_add_mark_accepts_valid_boundary_values(mark):
    student = Student(101, "Hari", 21)

    student.add_mark("Python", mark)

    assert student.marks["Python"] == mark


@pytest.mark.parametrize("mark", [-0.1, 100.1, -1, 101, None, "90", [90]])
def test_add_mark_rejects_invalid_values(mark):
    student = Student(101, "Hari", 21)

    with pytest.raises(ValueError):
        student.add_mark("Python", mark)


def test_add_mark_failure_leaves_marks_unchanged():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 80)

    with pytest.raises(ValueError):
        student.add_mark("Java", 120)

    assert student.marks == {"Python": 80}


def test_add_mark_overwrites_existing_subject():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 50)
    student.add_mark("Python", 80)

    assert student.marks == {"Python": 80}


def test_remove_mark_leaves_other_marks_intact():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)
    student.add_mark("Java", 80)

    student.remove_mark("Python")

    assert student.marks == {"Java": 80}


def test_remove_mark_twice_is_a_no_op():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)
    student.remove_mark("Python")
    student.remove_mark("Python")

    assert student.marks == {}


def test_average_with_single_mark():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 70)

    assert student.calculate_average() == 70


def test_average_with_float_marks():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 50.5)
    student.add_mark("Java", 60.5)

    assert student.calculate_average() == 55.5


def test_average_is_not_rounded():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 50)
    student.add_mark("Java", 51)
    student.add_mark("Go", 51)

    assert student.calculate_average() == pytest.approx(50.6666666, abs=1e-6)


def test_average_uses_zero_marks_in_the_calculation():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 100)
    student.add_mark("Java", 0)

    assert student.calculate_average() == 50


@pytest.mark.parametrize(
    "mark, expected_grade",
    [
        (100, "A+"),
        (90, "A+"),
        (89.9, "A"),
        (80, "A"),
        (79.9, "B"),
        (70, "B"),
        (69.9, "C"),
        (60, "C"),
        (59.9, "D"),
        (50, "D"),
        (49.9, "F"),
        (0, "F"),
    ],
)
def test_grade_exact_threshold_boundaries(mark, expected_grade):
    student = Student(101, "Hari", 21)

    student.add_mark("Python", mark)

    assert student.get_grade() == expected_grade


def test_grade_with_no_marks_is_failing():
    student = Student(101, "Hari", 21)

    assert student.get_grade() == "F"


def test_passed_at_exact_pass_mark():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 40)
    student.add_mark("Java", 60)

    assert student.calculate_average() == 50
    assert student.is_passed() is True


def test_passed_just_below_pass_mark():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 49.9)

    assert student.is_passed() is False


def test_passed_with_no_marks_is_false():
    student = Student(101, "Hari", 21)

    assert student.is_passed() is False


def test_display_contains_all_expected_keys():
    student = Student(101, "Hari", 21)

    data = student.display()

    assert set(data) == {
        "Student ID",
        "Name",
        "Age",
        "Courses",
        "Marks",
        "Average",
        "Grade",
        "Passed",
    }


def test_display_reports_courses_and_marks():
    student = Student(101, "Hari", 21)

    student.enroll_course("Python")
    student.add_mark("Python", 90)

    data = student.display()

    assert data["Age"] == 21
    assert data["Courses"] == ["Python"]
    assert data["Marks"] == {"Python": 90}
    assert data["Passed"] is True


def test_display_rounds_the_average_to_two_decimals():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 50)
    student.add_mark("Java", 51)
    student.add_mark("Go", 51)

    data = student.display()

    assert data["Average"] == 50.67


def test_display_with_no_marks():
    student = Student(101, "Hari", 21)

    data = student.display()

    assert data["Courses"] == []
    assert data["Marks"] == {}
    assert data["Average"] == 0
    assert data["Grade"] == "F"
    assert data["Passed"] is False


def test_string_method_full_format():
    student = Student(101, "Hari", 21)

    student.add_mark("Python", 90)

    assert str(student) == "Student(id=101, name=Hari, age=21, grade=A+)"


def test_string_method_with_no_marks_shows_failing_grade():
    student = Student(101, "Hari", 21)

    assert str(student) == "Student(id=101, name=Hari, age=21, grade=F)"
