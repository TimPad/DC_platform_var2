"""
Logic for External Assessment Module
"""
import pandas as pd
from typing import Tuple, List
from utils import get_supabase_client, fetch_all_from_supabase
from logic.data_utils import clean_email_column, clean_string_column, filter_valid_grades
import constants

def load_existing_peresdachi() -> pd.DataFrame:
    """Загрузка существующих записей из таблицы peresdachi"""
    try:
        all_data = fetch_all_from_supabase(constants.DB_TABLE_PERESDACHI)
        if all_data:
            return pd.DataFrame(all_data)
        return pd.DataFrame()
    except Exception as e:
        raise ValueError(f"Таблица peresdachi не найдена или пуста: {str(e)}")

def load_student_io_from_supabase() -> pd.DataFrame:
    """Загрузка данных из таблицы student_io"""
    try:
        select_query = f'"{constants.COL_EMAIL}", "{constants.COL_DISCIPLINE}", "{constants.COL_GRADE}"'
        all_data = fetch_all_from_supabase(constants.DB_TABLE_STUDENT_IO, select_query=select_query)
        
        if all_data:
            df = pd.DataFrame(all_data)
            df = clean_email_column(df, constants.COL_EMAIL)
            df = clean_string_column(df, constants.COL_DISCIPLINE)
            df = clean_string_column(df, constants.COL_GRADE)
            return df
        return pd.DataFrame()
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке данных из {constants.DB_TABLE_STUDENT_IO}: {str(e)}")

def save_to_supabase(df: pd.DataFrame) -> Tuple[bool, str]:
    """Сохранение данных в таблицу peresdachi в Supabase с использованием insert"""
    try:
        supabase = get_supabase_client()
        if df.empty:
            return False, "Нет данных для сохранения."

        cleaned_records = []
        for record in df.to_dict('records'):
            cleaned_record = {k: (v if pd.notna(v) else None) for k, v in record.items()}
            cleaned_records.append(cleaned_record)

        response = supabase.table(constants.DB_TABLE_PERESDACHI).insert(cleaned_records).execute()
        return True, "Данные успешно сохранены."
    except Exception as e:
        if "duplicate key value violates unique constraint" in str(e):
            return True, "Обнаружены дубликаты при сохранении. Они были проигнорированы. Остальные данные сохранены."
        return False, f"Ошибка при сохранении в Supabase: {str(e)}"

def get_new_records_from_dataframe(new_df: pd.DataFrame) -> pd.DataFrame:
    """Получить только новые записи, сравнивая с существующими в БД"""
    try:
        existing_df = load_existing_peresdachi()
        if existing_df.empty:
            return new_df
        
        merge_cols = [constants.COL_EMAIL, constants.COL_DISCIPLINE]
        if all(col in existing_df.columns for col in merge_cols) and all(col in new_df.columns for col in merge_cols):
            merged = new_df.merge(existing_df[merge_cols], on=merge_cols, how='left', indicator=True)
            return merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)
        return new_df
    except Exception as e:
        raise ValueError(f"Ошибка при определении новых записей: {str(e)}")

def process_external_assessment(grades_df: pd.DataFrame, students_df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Обработка пересдач внешней оценки"""
    logs = []
    
    # Шаг 1: Очистка данных
    grades_df = grades_df.astype(str)
    for col in grades_df.columns:
        grades_df[col] = grades_df[col].str.replace('-', '', regex=False).str.strip()
    
    # Шаг 2: Переименование колонок
    column_mapping = {
        constants.TEST_COL_INPUT: constants.DISCIPLINE_INPUT,
        constants.TEST_COL_MID: constants.DISCIPLINE_MID,
        constants.TEST_COL_FINAL: constants.DISCIPLINE_FINAL
    }
    grades_df = grades_df.rename(columns=column_mapping)
    
    # Шаг 3: Melt
    value_columns = [constants.DISCIPLINE_INPUT, constants.DISCIPLINE_MID, constants.DISCIPLINE_FINAL]
    id_cols = [constants.COL_EMAIL]
    
    if constants.COL_EMAIL not in grades_df.columns:
        raise ValueError(f"Колонка '{constants.COL_EMAIL}' не найдена в файле оценок")
    
    melted_df = pd.melt(grades_df, id_vars=id_cols, value_vars=value_columns, var_name=constants.COL_DISCIPLINE, value_name=constants.COL_GRADE)
    
    # Шаг 4: Присоединение данных студентов
    students_cols = [constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS_OLD, constants.COL_FACULTY, constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE]
    missing_cols = [col for col in students_cols if col not in students_df.columns]
    
    if missing_cols:
        logs.append(f"Отсутствуют колонки в файле студентов: {missing_cols}")
        available_cols = [col for col in students_cols if col in students_df.columns]
    else:
        available_cols = students_cols
    
    students_subset = students_df[available_cols].copy()
    melted_df = clean_email_column(melted_df, constants.COL_EMAIL)
    students_subset = clean_email_column(students_subset, constants.COL_EMAIL)
    
    result_df = melted_df.merge(students_subset, on=constants.COL_EMAIL, how='left')
    
    # Шаг 5: Добавление пустых колонок
    result_df[constants.COL_ID_DISCIPLINE] = ''
    result_df[constants.COL_PERIOD] = ''
    
    # Шаг 6: Переименование и структура
    if constants.COL_CAMPUS_OLD in result_df.columns:
        result_df = result_df.rename(columns={constants.COL_CAMPUS_OLD: constants.COL_CAMPUS})
        
    output_columns = [
        constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS, constants.COL_FACULTY,
        constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE, constants.COL_ID_DISCIPLINE,
        constants.COL_DISCIPLINE, constants.COL_PERIOD, constants.COL_GRADE
    ]
    final_columns = [col for col in output_columns if col in result_df.columns]
    result_df = result_df[final_columns]
    
    # Валидация оценок
    result_df = filter_valid_grades(result_df, constants.COL_GRADE)
    
    # Шаг 7: Проверка student_io
    logs.append(f"Проверка существующих оценок в {constants.DB_TABLE_STUDENT_IO}...")
    try:
        student_io_df = load_student_io_from_supabase()
        if not student_io_df.empty:
            result_df = clean_email_column(result_df, constants.COL_EMAIL)
            result_df = clean_string_column(result_df, constants.COL_DISCIPLINE)
            
            merged_with_io = result_df.merge(
                student_io_df[[constants.COL_EMAIL, constants.COL_DISCIPLINE, constants.COL_GRADE]], 
                on=[constants.COL_EMAIL, constants.COL_DISCIPLINE], 
                how='left', suffixes=('_from_file', '_from_io')
            )
            merged_with_io[constants.COL_GRADE] = merged_with_io[constants.COL_GRADE + '_from_io'].where(
                pd.notna(merged_with_io[constants.COL_GRADE + '_from_io']), merged_with_io[constants.COL_GRADE + '_from_file']
            )
            result_df = merged_with_io.drop(columns=[constants.COL_GRADE + '_from_file', constants.COL_GRADE + '_from_io'])
            result_df = filter_valid_grades(result_df, constants.COL_GRADE)
            logs.append(f"Проверка завершена. Найдено {len(student_io_df)} записей в {constants.DB_TABLE_STUDENT_IO}.")
        else:
            logs.append(f"Таблица {constants.DB_TABLE_STUDENT_IO} пуста, используются оценки из файла.")
    except Exception as e:
        logs.append(f"Ошибка при проверке {constants.DB_TABLE_STUDENT_IO}: {e}")

    # Шаг 8: Проверка peresdachi
    logs.append(f"Проверка существующих оценок в {constants.DB_TABLE_PERESDACHI}...")
    try:
        existing_peresdachi_df = load_existing_peresdachi()
        if not existing_peresdachi_df.empty:
            existing_peresdachi_df = clean_email_column(existing_peresdachi_df, constants.COL_EMAIL)
            existing_peresdachi_df = clean_string_column(existing_peresdachi_df, constants.COL_DISCIPLINE)
            
            merged_with_peresdachi = result_df.merge(
                existing_peresdachi_df[[constants.COL_EMAIL, constants.COL_DISCIPLINE, constants.COL_GRADE]], 
                on=[constants.COL_EMAIL, constants.COL_DISCIPLINE], 
                how='left', suffixes=('_current', '_peresdachi')
            )
            merged_with_peresdachi[constants.COL_GRADE] = merged_with_peresdachi[constants.COL_GRADE + '_peresdachi'].where(
                pd.notna(merged_with_peresdachi[constants.COL_GRADE + '_peresdachi']), merged_with_peresdachi[constants.COL_GRADE + '_current']
            )
            result_df = merged_with_peresdachi.drop(columns=[constants.COL_GRADE + '_current', constants.COL_GRADE + '_peresdachi'])
            result_df = filter_valid_grades(result_df, constants.COL_GRADE)
            logs.append(f"Проверка {constants.DB_TABLE_PERESDACHI} завершена. Найдено {len(existing_peresdachi_df)} записей.")
        else:
            logs.append(f"Таблица {constants.DB_TABLE_PERESDACHI} пуста, используются текущие оценки.")
    except Exception as e:
        logs.append(f"Ошибка при проверке {constants.DB_TABLE_PERESDACHI}: {e}")

    return result_df, logs

def process_project_assessment(grades_df: pd.DataFrame, students_df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Обработка внешнего измерения (Проекты)"""
    logs = []
    
    existing_project_columns = [col for col in constants.PROJECT_COLUMNS if col in grades_df.columns]
    if not existing_project_columns:
        raise ValueError("Не найдены колонки с оценками за проект (Задание:...).")

    def clean_numeric(series):
        return pd.to_numeric(series.astype(str).replace('-', float('nan')), errors='coerce')

    project_data = grades_df[existing_project_columns].apply(clean_numeric)
    grades_df[constants.COL_GRADE] = project_data.max(axis=1)
    grades_df[constants.COL_DISCIPLINE] = constants.DISCIPLINE_FINAL
    
    if constants.COL_EMAIL not in grades_df.columns:
        raise ValueError(f"Колонка '{constants.COL_EMAIL}' не найдена в файле.")
    
    grades_df = clean_email_column(grades_df, constants.COL_EMAIL)
    
    students_cols = [constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS_OLD, constants.COL_FACULTY, constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE]
    available_cols = [col for col in students_cols if col in students_df.columns]
    students_subset = clean_email_column(students_df[available_cols].copy(), constants.COL_EMAIL)
    
    result_df = grades_df.merge(students_subset, on=constants.COL_EMAIL, how='left')
    result_df[constants.COL_ID_DISCIPLINE] = ''
    result_df[constants.COL_PERIOD] = ''
    
    if constants.COL_CAMPUS_OLD in result_df.columns:
        result_df = result_df.rename(columns={constants.COL_CAMPUS_OLD: constants.COL_CAMPUS})
        
    output_columns = [
        constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS, constants.COL_FACULTY,
        constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE,
        constants.COL_DISCIPLINE, constants.COL_GRADE, constants.COL_ID_DISCIPLINE, constants.COL_PERIOD
    ]
    
    final_columns = [col for col in output_columns if col in result_df.columns]
    result_df = result_df[final_columns]
    
    result_df = filter_valid_grades(result_df, constants.COL_GRADE)
    result_df = result_df[pd.to_numeric(result_df[constants.COL_GRADE], errors='coerce') > 0]
    result_df[constants.COL_GRADE] = result_df[constants.COL_GRADE].astype(str)
    
    # Шаг 1: student_io
    logs.append(f"Проверка {constants.DB_TABLE_STUDENT_IO}...")
    try:
        student_io_df = load_student_io_from_supabase()
        if not student_io_df.empty:
            result_df = clean_email_column(result_df, constants.COL_EMAIL)
            merged_with_io = result_df.merge(
                student_io_df[[constants.COL_EMAIL, constants.COL_DISCIPLINE, constants.COL_GRADE]],
                on=[constants.COL_EMAIL, constants.COL_DISCIPLINE], how='left', suffixes=('_from_file', '_from_io')
            )
            merged_with_io[constants.COL_GRADE] = merged_with_io[constants.COL_GRADE + '_from_io'].where(
                pd.notna(merged_with_io[constants.COL_GRADE + '_from_io']), merged_with_io[constants.COL_GRADE + '_from_file']
            )
            result_df = merged_with_io.drop(columns=[constants.COL_GRADE + '_from_file', constants.COL_GRADE + '_from_io'])
            result_df = filter_valid_grades(result_df, constants.COL_GRADE)
            logs.append(f"Проверка {constants.DB_TABLE_STUDENT_IO} завершена.")
    except Exception as e:
        logs.append(f"Ошибка проверки {constants.DB_TABLE_STUDENT_IO}: {e}")
    
    # Шаг 2: peresdachi
    logs.append(f"Проверка {constants.DB_TABLE_PERESDACHI}...")
    try:
        existing_peresdachi_df = load_existing_peresdachi()
        if not existing_peresdachi_df.empty:
            existing_peresdachi_df = clean_email_column(existing_peresdachi_df, constants.COL_EMAIL)
            merged_with_peresdachi = result_df.merge(
                existing_peresdachi_df[[constants.COL_EMAIL, constants.COL_DISCIPLINE, constants.COL_GRADE]],
                on=[constants.COL_EMAIL, constants.COL_DISCIPLINE], how='left', suffixes=('_current', '_peresdachi')
            )
            merged_with_peresdachi[constants.COL_GRADE] = merged_with_peresdachi[constants.COL_GRADE + '_peresdachi'].where(
                pd.notna(merged_with_peresdachi[constants.COL_GRADE + '_peresdachi']), merged_with_peresdachi[constants.COL_GRADE + '_current']
            )
            result_df = merged_with_peresdachi.drop(columns=[constants.COL_GRADE + '_current', constants.COL_GRADE + '_peresdachi'])
            result_df = filter_valid_grades(result_df, constants.COL_GRADE)
            logs.append(f"Проверка {constants.DB_TABLE_PERESDACHI} завершена.")
    except Exception as e:
        logs.append(f"Ошибка проверки {constants.DB_TABLE_PERESDACHI}: {e}")

    return result_df, logs

def update_final_grades(df: pd.DataFrame) -> Tuple[bool, int, str]:
    """Обновление таблицы final_grades в Supabase на основе новых оценок за проекты."""
    try:
        supabase = get_supabase_client()
        if df.empty:
            return True, 0, "Данные отсутствуют"
            
        if constants.COL_EMAIL not in df.columns or constants.COL_GRADE not in df.columns:
            return False, 0, f"Нет необходимых колонок '{constants.COL_EMAIL}' или '{constants.COL_GRADE}'"
            
        work_df = clean_email_column(df.copy(), constants.COL_EMAIL)
        unique_emails = work_df[constants.COL_EMAIL].unique().tolist()
        
        if not unique_emails:
            return True, 0, "Нет уникальных email"

        existing_records_map = {}
        chunk_size = 200
        for i in range(0, len(unique_emails), chunk_size):
            chunk_emails = unique_emails[i:i + chunk_size]
            try:
                response = supabase.table(constants.DB_TABLE_FINAL_GRADES).select('*').in_(constants.COL_EMAIL, chunk_emails).execute()
                for rec in response.data:
                    email = rec.get(constants.COL_EMAIL, '').lower().strip()
                    if email:
                        existing_records_map[email] = rec
            except Exception:
                pass

        payloads = []
        processed_count = 0
        
        for _, row in work_df.iterrows():
            email = row.get(constants.COL_EMAIL)
            new_project_grade = row.get(constants.COL_GRADE)
            fio = row.get(constants.COL_FIO, '')
            
            if not email or pd.isna(new_project_grade):
                continue
            try:
                new_project_grade = float(new_project_grade)
            except:
                continue
                
            record = existing_records_map.get(email, {})
            old_test_grade = record.get('Оценка за тест')
            old_final_grade = record.get('Итоговая оценка')
            
            def to_float(val):
                return float(val) if val is not None and str(val).strip() else 0.0
            
            val_test, val_old_final = to_float(old_test_grade), to_float(old_final_grade)
            
            current_project = new_project_grade 
            new_final = max(val_test, current_project, val_old_final)
            
            payload = {constants.COL_EMAIL: email}
            if not record:
                payload[constants.COL_FIO] = fio
                if isinstance(fio, str):
                    parts = fio.split()
                    if len(parts) >= 1: payload['Фамилия'] = parts[0]
                    if len(parts) >= 2: payload['Имя'] = parts[1]
            
            payload['Оценка за проект'] = current_project
            payload['Итоговая оценка'] = new_final
            
            payloads.append(payload)
            processed_count += 1

        if not payloads:
            return True, 0, "Нет полезной нагрузки"
            
        for i in range(0, len(payloads), chunk_size):
            batch = payloads[i:i + chunk_size]
            supabase.table(constants.DB_TABLE_FINAL_GRADES).upsert(batch, on_conflict=constants.COL_EMAIL).execute()
            
        return True, processed_count, "Успешно обновлено"
            
    except Exception as e:
        return False, 0, f"Критическая ошибка при обновлении final_grades: {str(e)}"
