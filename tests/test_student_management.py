import pytest
import pandas as pd
import io
from logic.student_management import load_student_list_file

class MockUploadedFile:
    def __init__(self, name, content):
        self.name = name
        self.content = content
    def getvalue(self):
        return self.content

def test_load_student_list_file_xlsx(mocker):
    # Mocking pd.read_excel because we don't want to create a real binary xlsx
    mock_df = pd.DataFrame({
        'фио': ['Ivanov'],
        'корпоративная почта': ['ivanov@edu.hse.ru'],
        'кампус': ['Москва']
    })
    mocker.patch('pandas.read_excel', return_value=mock_df)
    
    mock_file = MockUploadedFile("students.xlsx", b"dummy content")
    result_df = load_student_list_file(mock_file)
    
    assert not result_df.empty
    assert 'ФИО' in result_df.columns
    assert 'Корпоративная почта' in result_df.columns
    assert result_df.iloc[0]['ФИО'] == 'Ivanov'
    assert result_df.iloc[0]['Корпоративная почта'] == 'ivanov@edu.hse.ru'

def test_load_student_list_file_csv_utf8():
    csv_content = "фио,email,кампус\nIvanov,ivanov@edu.hse.ru,Москва".encode('utf-8')
    mock_file = MockUploadedFile("students.csv", csv_content)
    
    result_df = load_student_list_file(mock_file)
    
    assert not result_df.empty
    assert result_df.iloc[0]['ФИО'] == 'Ivanov'
    assert result_df.iloc[0]['Корпоративная почта'] == 'ivanov@edu.hse.ru'

def test_load_student_list_file_unsupported_format():
    mock_file = MockUploadedFile("test.txt", b"some text")
    with pytest.raises(ValueError, match="Неподдерживаемый формат файла"):
        load_student_list_file(mock_file)


def test_students_are_cached_inside_streamlit(mocker):
    """st.cache_data работает только внутри запущенного Streamlit, поэтому проверяем через AppTest."""
    from streamlit.testing.v1 import AppTest
    from logic import student_management

    fetch = mocker.patch.object(
        student_management,
        "fetch_all_from_supabase",
        return_value=[{"корпоративная_почта": "ivanov@edu.hse.ru", "фио": "Иванов"}],
    )

    def script():
        import streamlit as st
        from logic.student_management import load_students_from_supabase

        load_students_from_supabase.clear()
        calls = st.session_state["calls"] = {}

        first = load_students_from_supabase()
        first.drop(columns=["ФИО"], inplace=True)  # правка копии не должна портить кэш
        second = load_students_from_supabase()
        calls["second_has_fio"] = "ФИО" in second.columns

        load_students_from_supabase(filters={"курс": ["Курс 3", "Курс 4"]})
        load_students_from_supabase(filters={"курс": ["Курс 3", "Курс 4"]})

        load_students_from_supabase.clear()
        load_students_from_supabase()

    app = AppTest.from_function(script).run()

    assert not app.exception
    assert app.session_state["calls"]["second_has_fio"]
    # без фильтра, с фильтром и ещё раз без фильтра после сброса кэша
    assert fetch.call_count == 3
    student_management.load_students_from_supabase.clear()
