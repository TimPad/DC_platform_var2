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
