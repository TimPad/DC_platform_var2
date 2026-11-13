import pandas as pd
import pytest

import constants
from logic.external_assessment import combine_grade_exports

EMAIL = constants.COL_EMAIL


def test_merges_courses_with_different_columns():
    group_1 = pd.DataFrame({
        "Фамилия": ["Иванов", "Петров"],
        EMAIL: ["ivanov@edu.hse.ru", "petrov@edu.hse.ru"],
        "Задание:Гуманитарный трек (Значение)": ["8,5", "-"],
        "Тест:Квиз (Значение)": [7, "-"],
    })
    english = pd.DataFrame({
        "Фамилия": ["Smith"],
        EMAIL: ["smith@edu.hse.ru"],
        "Задание:Humanities track (Значение)": [9],
        "Тест:Quiz for Hum track (Значение)": [6],
    })

    result = combine_grade_exports([group_1, english])

    assert result[EMAIL].tolist() == ["ivanov@edu.hse.ru", "petrov@edu.hse.ru", "smith@edu.hse.ru"]
    assert result["Задание:Гуманитарный трек (Значение)"].tolist()[0] == 8.5
    assert pd.isna(result["Задание:Гуманитарный трек (Значение)"].tolist()[1])
    assert result["Задание:Humanities track (Значение)"].tolist()[2] == 9


def test_student_in_two_courses_becomes_one_row_with_best_grades():
    course_a = pd.DataFrame({
        "Фамилия": ["Иванов"],
        EMAIL: [" Ivanov@edu.hse.ru "],
        "Задание:Трек (Значение)": [6],
        "Тест:Трек (Значение)": ["-"],
    })
    course_b = pd.DataFrame({
        "Фамилия": [None],
        EMAIL: ["ivanov@edu.hse.ru"],
        "Задание:Трек (Значение)": [9],
        "Тест:Трек (Значение)": [7],
    })

    result = combine_grade_exports([course_a, course_b])

    assert len(result) == 1
    row = result.iloc[0]
    assert row[EMAIL] == "ivanov@edu.hse.ru"
    assert row["Фамилия"] == "Иванов"
    assert row["Задание:Трек (Значение)"] == 9
    assert row["Тест:Трек (Значение)"] == 7


def test_drops_rows_without_email_and_empty_files():
    df = pd.DataFrame({EMAIL: ["a@edu.hse.ru", None, ""], "Тест:Т (Значение)": [1, 2, 3]})

    result = combine_grade_exports([df, pd.DataFrame()])

    assert result[EMAIL].tolist() == ["a@edu.hse.ru"]


def test_requires_email_column():
    with pytest.raises(ValueError):
        combine_grade_exports([pd.DataFrame({"Фамилия": ["Иванов"]})])
