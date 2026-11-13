"""
Logic for External Assessment Module
"""
import numpy as np
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

def load_peresdachi_by_date_range(date_from, date_to) -> pd.DataFrame:
    """Загрузка записей из таблицы peresdachi с фильтром по дате добавления (created_at).
    
    Args:
        date_from: datetime.date — начало диапазона (включительно)
        date_to:   datetime.date — конец диапазона (включительно)
    
    Returns:
        pd.DataFrame с записями за указанный период
    """
    try:
        from datetime import timedelta
        supabase = get_supabase_client()

        # Преобразуем даты в ISO-строки для Supabase
        from_str = date_from.isoformat()
        # Добавляем 1 день, чтобы включить записи созданные в течение всего дня date_to
        to_str = (date_to + timedelta(days=1)).isoformat()

        all_data = []
        page_size = 1000
        offset = 0

        while True:
            response = (
                supabase.table(constants.DB_TABLE_PERESDACHI)
                .select("*")
                .gte("created_at", from_str)
                .lt("created_at", to_str)
                .range(offset, offset + page_size - 1)
                .execute()
            )
            if response.data:
                all_data.extend(response.data)
                if len(response.data) < page_size:
                    break
                offset += page_size
            else:
                break

        if all_data:
            return pd.DataFrame(all_data)
        return pd.DataFrame()
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке данных peresdachi по диапазону дат: {str(e)}")

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

def load_registration_data_from_supabase() -> pd.DataFrame:
    """Загрузка данных из таблицы registration_data"""
    try:
        all_data = fetch_all_from_supabase(constants.DB_TABLE_REGISTRATION_DATA)
        if all_data:
            df = pd.DataFrame(all_data)
            df = clean_email_column(df, constants.COL_EMAIL)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"Ошибка при загрузке данных из {constants.DB_TABLE_REGISTRATION_DATA}: {str(e)}")
        return pd.DataFrame()

def save_to_supabase(df: pd.DataFrame) -> Tuple[bool, str]:
    """Сохранение данных в таблицу peresdachi в Supabase с использованием insert"""
    # Список колонок, которые реально существуют в таблице peresdachi
    PERESDACHI_COLUMNS = {
        constants.COL_FIO,
        constants.COL_EMAIL,
        constants.COL_CAMPUS,
        constants.COL_FACULTY,
        constants.COL_PROGRAM,
        constants.COL_GROUP,
        constants.COL_COURSE,
        constants.COL_ID_DISCIPLINE,
        constants.COL_DISCIPLINE,
        constants.COL_PERIOD,
        constants.COL_GRADE,
        constants.COL_CANCEL,
    }
    try:
        supabase = get_supabase_client()
        if df.empty:
            return False, "Нет данных для сохранения."

        # Оставляем только колонки, присутствующие и в датафрейме, и в схеме таблицы
        cols_to_save = [c for c in df.columns if c in PERESDACHI_COLUMNS]
        df_to_save = df[cols_to_save]

        cleaned_records = []
        for record in df_to_save.to_dict('records'):
            cleaned_record = {k: (v if pd.notna(v) else None) for k, v in record.items()}
            cleaned_records.append(cleaned_record)

        supabase.table(constants.DB_TABLE_PERESDACHI).insert(cleaned_records).execute()
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
            # Нормализуем existing_df перед сравнением, чтобы совпадение работало
            # корректно (разный регистр, пробелы и т.п. не должны мешать)
            existing_normalized = existing_df[merge_cols].copy()
            existing_normalized = clean_email_column(existing_normalized, constants.COL_EMAIL)
            existing_normalized = clean_string_column(existing_normalized, constants.COL_DISCIPLINE)
            existing_normalized = existing_normalized.drop_duplicates(subset=merge_cols)
            merged = new_df.merge(existing_normalized, on=merge_cols, how='left', indicator=True)
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
    melted_df = clean_email_column(melted_df, constants.COL_EMAIL)
    
    registration_df = load_registration_data_from_supabase()
    
    students_cols = [constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS_OLD, constants.COL_FACULTY, constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE]
    avail_stu_cols = [col for col in students_cols if col in students_df.columns]
    students_subset = clean_email_column(students_df[avail_stu_cols].copy(), constants.COL_EMAIL)
    if constants.COL_CAMPUS_OLD in students_subset.columns:
        students_subset = students_subset.rename(columns={constants.COL_CAMPUS_OLD: constants.COL_CAMPUS})
    students_subset = students_subset.drop_duplicates(subset=[constants.COL_EMAIL])
        
    if not registration_df.empty:
        reg_cols = [
            constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS_OLD, constants.COL_CAMPUS, 
            constants.COL_FACULTY, constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE, 
            constants.COL_CANCEL, constants.COL_ID_DISCIPLINE, constants.COL_DISCIPLINE, constants.COL_PERIOD
        ]
        avail_reg_cols = [col for col in reg_cols if col in registration_df.columns]
        reg_subset = clean_email_column(registration_df[avail_reg_cols].copy(), constants.COL_EMAIL)
        if constants.COL_CAMPUS_OLD in reg_subset.columns and constants.COL_CAMPUS not in reg_subset.columns:
            reg_subset = reg_subset.rename(columns={constants.COL_CAMPUS_OLD: constants.COL_CAMPUS})
        merge_keys = [constants.COL_EMAIL]
        if constants.COL_DISCIPLINE in reg_subset.columns:
            merge_keys.append(constants.COL_DISCIPLINE)
            
        reg_subset = reg_subset.drop_duplicates(subset=merge_keys)
        
        result_df = melted_df.merge(reg_subset, on=merge_keys, how='left')

        result_df = result_df.merge(students_subset, on=constants.COL_EMAIL, how='left', suffixes=('', '_stu'))
        
        for col in [constants.COL_FIO, constants.COL_CAMPUS, constants.COL_FACULTY, constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE]:
            stu_col = col + '_stu'
            if col in result_df.columns and stu_col in result_df.columns:
                result_df[col] = result_df[col].fillna(result_df[stu_col])
            elif stu_col in result_df.columns:
                result_df[col] = result_df[stu_col]
                
        stu_cols_to_drop = [c for c in result_df.columns if c.endswith('_stu')]
        result_df = result_df.drop(columns=stu_cols_to_drop)
    else:
        result_df = melted_df.merge(students_subset, on=constants.COL_EMAIL, how='left')
    
    if constants.COL_CANCEL not in result_df.columns:
        result_df[constants.COL_CANCEL] = ''
    
    if constants.COL_ID_DISCIPLINE not in result_df.columns:
        result_df[constants.COL_ID_DISCIPLINE] = ''
    else:
        result_df[constants.COL_ID_DISCIPLINE] = result_df[constants.COL_ID_DISCIPLINE].fillna('')

    if constants.COL_PERIOD not in result_df.columns:
        result_df[constants.COL_PERIOD] = ''
    else:
        result_df[constants.COL_PERIOD] = result_df[constants.COL_PERIOD].fillna('')
    
    # Шаг 6: Переименование и структура
    output_columns = [
        constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS, constants.COL_FACULTY,
        constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE, constants.COL_ID_DISCIPLINE,
        constants.COL_DISCIPLINE, constants.COL_PERIOD, constants.COL_GRADE, constants.COL_CANCEL
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
    if constants.COL_EMAIL not in grades_df.columns:
        raise ValueError(f"Колонка '{constants.COL_EMAIL}' не найдена в файле.")

    # Pandas добавляет суффиксы .1, .2 и т. д. к повторяющимся заголовкам.
    def max_grade(prefix: str) -> pd.Series:
        columns = grades_df.filter(regex=rf"^\s*{prefix}:.*\(Значение\)(?:\.\d+)?\s*$")
        if columns.shape[1] == 0:
            raise ValueError(f"Не найдены колонки с оценками «{prefix}:… (Значение)».")

        numeric = columns.apply(
            lambda column: pd.to_numeric(
                column.astype("string").str.replace(",", ".", regex=False), errors="coerce"
            )
        )
        return numeric.replace([np.inf, -np.inf], np.nan).max(axis=1)

    project_max = max_grade("Задание")
    test_max = max_grade("Тест")
    incomplete_count = (project_max.notna() ^ test_max.notna()).sum()
    if incomplete_count:
        logs.append(f"Пропущено строк с оценкой только за одну часть: {incomplete_count}.")

    grades_df = grades_df.copy()
    grades_df[constants.COL_PROJECT_GRADE] = project_max
    grades_df[constants.COL_TEST_GRADE] = test_max
    grades_df[constants.COL_GRADE] = np.floor((project_max + test_max) / 2 + 0.5)
    grades_df[constants.COL_DISCIPLINE] = constants.DISCIPLINE_FINAL

    grades_df = grades_df.dropna(subset=[constants.COL_GRADE]).copy()
    grades_df[constants.COL_GRADE] = grades_df[constants.COL_GRADE].astype(int).astype(str)
    grades_df = clean_email_column(grades_df, constants.COL_EMAIL)
    
    registration_df = load_registration_data_from_supabase()
    
    students_cols = [constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS_OLD, constants.COL_FACULTY, constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE]
    available_cols = [col for col in students_cols if col in students_df.columns]
    students_subset = clean_email_column(students_df[available_cols].copy(), constants.COL_EMAIL)
    if constants.COL_CAMPUS_OLD in students_subset.columns:
        students_subset = students_subset.rename(columns={constants.COL_CAMPUS_OLD: constants.COL_CAMPUS})
    students_subset = students_subset.drop_duplicates(subset=[constants.COL_EMAIL])
    
    if not registration_df.empty:
        reg_cols = [
            constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS_OLD, constants.COL_CAMPUS, 
            constants.COL_FACULTY, constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE, 
            constants.COL_CANCEL, constants.COL_ID_DISCIPLINE, constants.COL_DISCIPLINE, constants.COL_PERIOD
        ]
        avail_reg_cols = [col for col in reg_cols if col in registration_df.columns]
        reg_subset = clean_email_column(registration_df[avail_reg_cols].copy(), constants.COL_EMAIL)
        if constants.COL_CAMPUS_OLD in reg_subset.columns and constants.COL_CAMPUS not in reg_subset.columns:
            reg_subset = reg_subset.rename(columns={constants.COL_CAMPUS_OLD: constants.COL_CAMPUS})
        merge_keys = [constants.COL_EMAIL]
        if constants.COL_DISCIPLINE in reg_subset.columns:
            merge_keys.append(constants.COL_DISCIPLINE)
            
        reg_subset = reg_subset.drop_duplicates(subset=merge_keys)
        
        result_df = grades_df.merge(reg_subset, on=merge_keys, how='left')

        result_df = result_df.merge(students_subset, on=constants.COL_EMAIL, how='left', suffixes=('', '_stu'))
        
        for col in [constants.COL_FIO, constants.COL_CAMPUS, constants.COL_FACULTY, constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE]:
            stu_col = col + '_stu'
            if col in result_df.columns and stu_col in result_df.columns:
                result_df[col] = result_df[col].fillna(result_df[stu_col])
            elif stu_col in result_df.columns:
                result_df[col] = result_df[stu_col]
                
        stu_cols_to_drop = [c for c in result_df.columns if c.endswith('_stu')]
        result_df = result_df.drop(columns=stu_cols_to_drop)
    else:
        result_df = grades_df.merge(students_subset, on=constants.COL_EMAIL, how='left')
        
    if constants.COL_CANCEL not in result_df.columns:
        result_df[constants.COL_CANCEL] = ''
        
    if constants.COL_ID_DISCIPLINE not in result_df.columns:
        result_df[constants.COL_ID_DISCIPLINE] = ''
    else:
        result_df[constants.COL_ID_DISCIPLINE] = result_df[constants.COL_ID_DISCIPLINE].fillna('')

    if constants.COL_PERIOD not in result_df.columns:
        result_df[constants.COL_PERIOD] = ''
    else:
        result_df[constants.COL_PERIOD] = result_df[constants.COL_PERIOD].fillna('')
    
    output_columns = [
        constants.COL_FIO, constants.COL_EMAIL, constants.COL_CAMPUS, constants.COL_FACULTY,
        constants.COL_PROGRAM, constants.COL_GROUP, constants.COL_COURSE,
        constants.COL_DISCIPLINE, constants.COL_GRADE, constants.COL_PROJECT_GRADE,
        constants.COL_TEST_GRADE, constants.COL_ID_DISCIPLINE, constants.COL_PERIOD, constants.COL_CANCEL
    ]
    
    final_columns = [col for col in output_columns if col in result_df.columns]
    result_df = result_df[final_columns]
    
    return result_df, logs

def deduplicate_and_split(result_df: pd.DataFrame, conflict_cols: List[str] = None):
    """
    Дедупликация результата и разделение на полный набор и только новые записи.

    Returns:
        dict с ключами: result_df, display_new_records, total_count, new_count, duplicates_removed
    """
    if conflict_cols is None:
        conflict_cols = [constants.COL_EMAIL, constants.COL_DISCIPLINE]

    total_count_uncleaned = len(result_df)

    result_df_cleaned = result_df.drop_duplicates(subset=conflict_cols, keep='first')
    duplicates_removed = total_count_uncleaned - len(result_df_cleaned)

    if duplicates_removed > 0:
        result_df = result_df_cleaned

    display_new_records = get_new_records_from_dataframe(result_df)
    display_new_records = display_new_records.drop_duplicates(subset=conflict_cols, keep='first')

    return {
        'result_df': result_df,
        'display_new_records': display_new_records,
        'total_count': len(result_df),
        'new_count': len(display_new_records),
        'duplicates_removed': duplicates_removed,
    }


def update_final_grades(df: pd.DataFrame) -> Tuple[bool, int, str]:
    """Сохраняет максимумы за проект и тест и рассчитанную итоговую оценку."""
    try:
        if df.empty:
            return True, 0, "Данные отсутствуют"

        required_columns = [
            constants.COL_EMAIL, constants.COL_PROJECT_GRADE,
            constants.COL_TEST_GRADE, constants.COL_GRADE,
        ]
        missing_columns = [column for column in required_columns if column not in df.columns]
        if missing_columns:
            return False, 0, f"Нет необходимых колонок: {', '.join(missing_columns)}"

        work_df = clean_email_column(df.dropna(subset=required_columns).copy(), constants.COL_EMAIL)
        work_df = work_df[work_df[constants.COL_EMAIL].ne("")].drop_duplicates(subset=[constants.COL_EMAIL])
        if work_df.empty:
            return True, 0, "Нет оценок для обновления"

        supabase = get_supabase_client()
        emails = work_df[constants.COL_EMAIL].tolist()
        existing_emails = set()
        chunk_size = 200
        for start in range(0, len(emails), chunk_size):
            response = (
                supabase.table(constants.DB_TABLE_FINAL_GRADES)
                .select(f'"{constants.COL_EMAIL}"')
                .in_(constants.COL_EMAIL, emails[start:start + chunk_size])
                .execute()
            )
            existing_emails.update(record[constants.COL_EMAIL] for record in response.data)

        updates = []
        inserts = []
        for _, row in work_df.iterrows():
            email = row[constants.COL_EMAIL]
            payload = {
                constants.COL_EMAIL: email,
                constants.COL_PROJECT_GRADE: float(row[constants.COL_PROJECT_GRADE]),
                constants.COL_TEST_GRADE: float(row[constants.COL_TEST_GRADE]),
                constants.COL_FINAL_GRADE: int(row[constants.COL_GRADE]),
            }
            if email in existing_emails:
                updates.append(payload)
            else:
                fio = row.get(constants.COL_FIO, "")
                fio = fio if isinstance(fio, str) else ""
                names = fio.split()
                payload[constants.COL_FIO] = fio
                payload["Фамилия"] = names[0] if names else ""
                payload["Имя"] = names[1] if len(names) > 1 else ""
                inserts.append(payload)

        for records in (updates, inserts):
            for start in range(0, len(records), chunk_size):
                batch = records[start:start + chunk_size]
                supabase.table(constants.DB_TABLE_FINAL_GRADES).upsert(
                    batch, on_conflict=constants.COL_EMAIL
                ).execute()

        return True, len(work_df), "Успешно обновлено"
            
    except Exception as e:
        return False, 0, f"Критическая ошибка при обновлении final_grades: {str(e)}"
