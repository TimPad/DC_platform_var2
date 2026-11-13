import pandas as pd
import pytest

import constants
from logic import external_assessment

EMAIL, DISCIPLINE, GRADE = constants.COL_EMAIL, constants.COL_DISCIPLINE, constants.COL_GRADE


def test_load_existing_peresdachi_requests_only_given_columns(mocker):
    fetch = mocker.patch.object(external_assessment, "fetch_all_from_supabase", return_value=[])

    external_assessment.load_existing_peresdachi(columns=[EMAIL, DISCIPLINE])

    fetch.assert_called_once_with(
        constants.DB_TABLE_PERESDACHI,
        select_query=f'"{EMAIL}", "{DISCIPLINE}"',
        order_by=[f'"{EMAIL}"', f'"{DISCIPLINE}"'],
    )


def test_load_existing_peresdachi_loads_all_columns_by_default(mocker):
    fetch = mocker.patch.object(
        external_assessment, "fetch_all_from_supabase", return_value=[{EMAIL: "a@edu.hse.ru", "ФИО": "А"}]
    )

    result = external_assessment.load_existing_peresdachi()

    fetch.assert_called_once_with(constants.DB_TABLE_PERESDACHI, order_by="id")
    assert result.columns.tolist() == [EMAIL, "ФИО"]


def test_new_records_use_passed_peresdachi_without_loading(mocker):
    load = mocker.patch.object(external_assessment, "load_existing_peresdachi")
    new_df = pd.DataFrame({
        EMAIL: ["old@edu.hse.ru", "new@edu.hse.ru"],
        DISCIPLINE: [constants.DISCIPLINE_FINAL, constants.DISCIPLINE_FINAL],
        GRADE: ["8", "9"],
    })
    existing = pd.DataFrame({EMAIL: [" OLD@edu.hse.ru "], DISCIPLINE: [constants.DISCIPLINE_FINAL], GRADE: ["7"]})

    result = external_assessment.get_new_records_from_dataframe(new_df, existing_df=existing)

    load.assert_not_called()
    assert result[EMAIL].tolist() == ["new@edu.hse.ru"]
    assert existing[EMAIL].tolist() == [" OLD@edu.hse.ru "]  # переданная таблица не меняется


def test_new_records_load_only_key_columns_when_nothing_passed(mocker):
    load = mocker.patch.object(external_assessment, "load_existing_peresdachi", return_value=pd.DataFrame())
    new_df = pd.DataFrame({EMAIL: ["new@edu.hse.ru"], DISCIPLINE: [constants.DISCIPLINE_FINAL], GRADE: ["9"]})

    result = external_assessment.deduplicate_and_split(new_df)

    load.assert_called_once_with(columns=[EMAIL, DISCIPLINE])
    assert result["new_count"] == 1


@pytest.fixture
def tests_tab_inputs(mocker):
    mocker.patch.object(external_assessment, "load_registration_data_from_supabase", return_value=pd.DataFrame())
    mocker.patch.object(external_assessment, "load_student_io_from_supabase", return_value=pd.DataFrame())
    grades = pd.DataFrame({
        EMAIL: ["first@edu.hse.ru", "second@edu.hse.ru"],
        constants.TEST_COL_INPUT: ["5", "-"],
        constants.TEST_COL_MID: ["-", "-"],
        constants.TEST_COL_FINAL: ["6", "7"],
    })
    students = pd.DataFrame({EMAIL: ["first@edu.hse.ru", "second@edu.hse.ru"], constants.COL_FIO: ["Первый", "Второй"]})
    return grades, students


def test_tests_tab_gives_same_result_with_passed_and_loaded_peresdachi(mocker, tests_tab_inputs):
    grades, students = tests_tab_inputs
    existing = pd.DataFrame({
        EMAIL: ["FIRST@edu.hse.ru"],
        DISCIPLINE: [constants.DISCIPLINE_FINAL],
        GRADE: ["9"],
    })
    load = mocker.patch.object(external_assessment, "load_existing_peresdachi", return_value=existing.copy())

    loaded_result, _ = external_assessment.process_external_assessment(grades.copy(), students)
    load.assert_called_once_with(columns=external_assessment.PERESDACHI_COMPARE_COLUMNS)

    load.reset_mock()
    passed_result, _ = external_assessment.process_external_assessment(
        grades.copy(), students, existing_peresdachi_df=existing
    )
    load.assert_not_called()

    pd.testing.assert_frame_equal(
        loaded_result.reset_index(drop=True), passed_result.reset_index(drop=True)
    )
    # оценка из peresdachi важнее оценки из файла
    final_first = passed_result[
        (passed_result[EMAIL] == "first@edu.hse.ru") & (passed_result[DISCIPLINE] == constants.DISCIPLINE_FINAL)
    ]
    assert final_first[GRADE].tolist() == ["9"]
    assert existing[EMAIL].tolist() == ["FIRST@edu.hse.ru"]  # переданная таблица не меняется

    # один и тот же набор peresdachi годится и для поиска новых записей
    split = external_assessment.deduplicate_and_split(passed_result, existing_df=existing)
    load.assert_not_called()
    assert split["total_count"] == 3
    assert split["new_count"] == 2
