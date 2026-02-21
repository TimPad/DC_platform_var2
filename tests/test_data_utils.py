import pandas as pd
from logic.data_utils import clean_email_column, clean_string_column, filter_valid_grades

def test_clean_email_column():
    df = pd.DataFrame({
        'email': [' TEST@Example.com ', 'nikulin@EDU.HSE.RU', 'none']
    })
    cleaned_df = clean_email_column(df, 'email')
    assert cleaned_df['email'].tolist() == ['test@example.com', 'nikulin@edu.hse.ru', 'none']

def test_clean_string_column():
    df = pd.DataFrame({
        'name': ['  Ivan  ', 'Petr\n', '  Sidorov  ']
    })
    cleaned_df = clean_string_column(df, 'name')
    assert cleaned_df['name'].tolist() == ['Ivan', 'Petr', 'Sidorov']

def test_filter_valid_grades():
    df = pd.DataFrame({
        'grade': ['5', 'NaN', '', ' 8 ', None]
    })
    filtered_df = filter_valid_grades(df, 'grade')
    # Should keep '5' and ' 8 '
    # Actually filter_valid_grades removes NaN, empty string, and "nan"
    assert filtered_df['grade'].tolist() == ['5', ' 8 ']
