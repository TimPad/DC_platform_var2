"""
Logic for Student Management
Handling student list loading, parsing, and updating in Supabase.
"""
import pandas as pd
from typing import Tuple
import time
from io import StringIO
from utils import get_supabase_client, fetch_all_from_supabase
from constants import STUDENT_REQUIRED_COLUMNS, STUDENT_DB_TO_DF_MAPPING

def load_student_list_file(uploaded_file) -> pd.DataFrame:
    """
    Загрузка списка студентов из файла Excel или CSV.
    Парсит файл, находит нужные колонки и нормализует данные.
    """
    try:
        file_name = uploaded_file.name.lower()
        if file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        elif file_name.endswith('.csv'):
            content = uploaded_file.getvalue()
            try:
                # Попытка 1: UTF-16 + Tab (часто бывает в выгрузках)
                df = pd.read_csv(StringIO(content.decode('utf-16')), sep='\t')
            except (UnicodeDecodeError, pd.errors.ParserError):
                try:
                    # Попытка 2: UTF-8
                    df = pd.read_csv(StringIO(content.decode('utf-8')))
                except UnicodeDecodeError:
                    # Попытка 3: CP1251 (Windows)
                    df = pd.read_csv(StringIO(content.decode('cp1251')))
        else:
            raise ValueError("Неподдерживаемый формат файла")

        # Поиск колонок по вариациям названий (из constants.py)
        found_columns = {}
        df_columns_lower = [str(col).lower().strip() for col in df.columns]
        
        for target_col, possible_names in STUDENT_REQUIRED_COLUMNS.items():
            for col_idx, col_name in enumerate(df_columns_lower):
                if any(possible_name in col_name for possible_name in possible_names):
                    found_columns[target_col] = df.columns[col_idx]
                    break

        # Формирование результирующего DataFrame
        result_df = pd.DataFrame()
        for target_col, source_col in found_columns.items():
            if source_col in df.columns:
                result_df[target_col] = df[source_col]

        # Специфичная логика парсинга "Данные о пользователе" (если есть)
        if 'Данные о пользователе' in df.columns:
            user_data = df['Данные о пользователе'].astype(str)
            parsed_data = user_data.str.split(';', expand=True)
            if len(parsed_data.columns) >= 4:
                result_df['Факультет'] = parsed_data[0]
                result_df['Образовательная программа'] = parsed_data[1] 
                result_df['Курс'] = parsed_data[2]
                result_df['Группа'] = parsed_data[3]

        # Заполнение недостающих колонок
        for required_col in STUDENT_REQUIRED_COLUMNS.keys():
            if required_col not in result_df.columns:
                if required_col == 'ФИО':
                    result_df[required_col] = None
                else:
                    result_df[required_col] = ''

        # Фильтрация и очистка email
        if 'Корпоративная почта' in result_df.columns:
            result_df = result_df[result_df['Корпоративная почта'].astype(str).str.contains('@edu.hse.ru', na=False)]
            result_df['Корпоративная почта'] = pd.Series(result_df['Корпоративная почта']).astype(str).str.lower().str.strip()
            
        return result_df
        
    except Exception as e:
        raise ValueError(f"Ошибка загрузки списка студентов: {e}")

def upload_students_to_supabase(supabase, student_data: pd.DataFrame) -> bool:
    """
    Загрузка данных студентов в таблицу students с использованием оптимизированного UPSERT.
    """
    try:
        records_for_upsert = []
        processed_emails = set()
        
        # Инвертируем маппинг для сохранения в БД (DF Name -> DB Name)
        # STUDENT_DB_TO_DF_MAPPING: 'db_col' -> 'Df Col'
        # Нам нужно обратное, но у нас в коде keys это db_col.
        # Подготовим маппинг для value из row.
        
        for _, row in student_data.iterrows():
            email = str(row.get('Корпоративная почта', '')).strip().lower()
            if not email or '@edu.hse.ru' not in email:
                continue
            if email in processed_emails:
                continue
            processed_emails.add(email)
                
            student_record = {
                'корпоративная_почта': email,
                'фио': str(row.get('ФИО', 'Неизвестно')).strip() or 'Неизвестно',
                'филиал_кампус': str(row.get('Филиал (кампус)', '')) if pd.notna(row.get('Филиал (кампус)')) and str(row.get('Филиал (кампус)', '')).strip() else None,
                'факультет': str(row.get('Факультет', '')) if pd.notna(row.get('Факультет')) and str(row.get('Факультет', '')).strip() else None,
                'образовательная_программа': str(row.get('Образовательная программа', '')) if pd.notna(row.get('Образовательная программа')) and str(row.get('Образовательная программа', '')).strip() else None,
                'версия_образовательной_программы': str(row.get('Версия образовательной программы', '')) if pd.notna(row.get('Версия образовательной программы')) and str(row.get('Версия образовательной программы', '')).strip() else None,
                'группа': str(row.get('Группа', '')) if pd.notna(row.get('Группа')) and str(row.get('Группа', '')).strip() else None,
                'курс': str(row.get('Курс', '')) if pd.notna(row.get('Курс')) and str(row.get('Курс', '')).strip() else None,
                'уровень_образования': str(row.get('Уровень образования', '')) if pd.notna(row.get('Уровень образования')) and str(row.get('Уровень образования', '')).strip() else None,
            }
            records_for_upsert.append(student_record)
        
        if not records_for_upsert:
            return False, "Нет записей для обработки"
        
        # Batch processing
        batch_size = 200
        total_processed = 0
        
        for i in range(0, len(records_for_upsert), batch_size):
            batch = records_for_upsert[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = ((len(records_for_upsert) - 1) // batch_size) + 1
            
            try:
                result = supabase.table('students').upsert(
                    batch,
                    on_conflict='корпоративная_почта',
                    ignore_duplicates=False,
                    returning='minimal'
                ).execute()
                total_processed += len(batch)
            except Exception as e:
                error_str = str(e)
                if any(pat in error_str.lower() for pat in ["connection", "timeout", "ssl", "eof"]):
                    time.sleep(2)
                    try:
                        result = supabase.table('students').upsert(batch, on_conflict='корпоративная_почта').execute()
                        total_processed += len(batch)
                    except Exception as retry_error:
                        return False, f"Батч {batch_num} не удался после повтора: {retry_error}"
                else:
                    return False, f"Ошибка в батче {batch_num}: {e}"
        
        return True, f"UPSERT завершён! Обработано {total_processed} записей"
    except Exception as e:
        return False, f"Критическая ошибка UPSERT студентов: {e}"

def load_students_from_supabase(filters: dict = None) -> pd.DataFrame:
    """
    Загрузка списка студентов из Supabase с кэшированием (TTL 300с).
    Поддерживает фильтрацию (например, {'курс': 'Курс 4'}).
    """
    try:
        # Используем fetch_all_from_supabase из utils для пагинации
        all_data = fetch_all_from_supabase('students', filters=filters)
        
        if all_data:
            df = pd.DataFrame(all_data)
            
            # Переименование колонок используя константу
            existing_columns = {k: v for k, v in STUDENT_DB_TO_DF_MAPPING.items() if k in df.columns}
            df = df.rename(columns=existing_columns)
            
            return df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        raise ValueError(f"Не удалось загрузить данные студентов: {str(e)}")
