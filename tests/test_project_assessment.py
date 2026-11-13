from unittest.mock import Mock

import pandas as pd
import pytest

import constants
from logic import external_assessment


@pytest.fixture
def without_database(mocker):
    for name in (
        "load_registration_data_from_supabase",
        "load_student_io_from_supabase",
        "load_existing_peresdachi",
    ):
        mocker.patch.object(external_assessment, name, return_value=pd.DataFrame())


def test_project_results_use_independent_maxima(without_database):
    emails = ["first@example.com", "second@example.com", "third@example.com"]
    grades = pd.DataFrame({
        constants.COL_EMAIL: emails,
        "Задание:Трек 1 (Значение)": ["8,5", 9, 0],
        "Задание:Трек 2 (Значение)": [9, "-", "-"],
        "Тест:Трек 1 (Значение)": [7, "-", 6],
        "Тест:Трек 2 (Значение)": ["-", "-", "-"],
        "Тест:Трек 2 (Значение).1": [8, "-", "-"],
        "Тест:Трек 3 (Значение)": [6, "-", "-"],
        "Задание:Трек 2 (Отзыв)": [10, 10, 10],
        "Итоговая оценка за курс (Значение)": [10, 10, 10],
    })

    results, _ = external_assessment.process_project_assessment(
        grades, pd.DataFrame({constants.COL_EMAIL: emails})
    )

    assert results[constants.COL_EMAIL].tolist() == [emails[0], emails[2]]
    assert results[constants.COL_GRADE].tolist() == ["9", "3"]
    assert results["Оценка за проект"].tolist() == [9, 0]
    assert results["Оценка за тест"].tolist() == [8, 6]


def test_project_results_require_test_columns(without_database):
    grades = pd.DataFrame({
        constants.COL_EMAIL: ["student@example.com"],
        constants.PROJECT_COL_GENERAL: [8],
    })

    with pytest.raises(ValueError, match="Тест:"):
        external_assessment.process_project_assessment(
            grades, grades[[constants.COL_EMAIL]]
        )


def test_final_grades_save_components_and_calculated_result(mocker):
    email = "student@example.com"
    supabase = mocker.patch.object(
        external_assessment, "get_supabase_client", return_value=Mock()
    ).return_value
    table = supabase.table.return_value
    table.select.return_value.in_.return_value.execute.return_value.data = [{
        constants.COL_EMAIL: email,
        "Оценка за тест": 10,
        "Итоговая оценка": 10,
    }]
    results = pd.DataFrame([{
        constants.COL_EMAIL: email,
        constants.COL_GRADE: "9",
        "Оценка за проект": 9,
        "Оценка за тест": 8,
    }])

    success, count, message = external_assessment.update_final_grades(results)

    assert success, message
    assert count == 1
    table.upsert.assert_called_once_with([{
        constants.COL_EMAIL: email,
        "Оценка за проект": 9,
        "Оценка за тест": 8,
        "Итоговая оценка": 9,
    }], on_conflict=constants.COL_EMAIL)
