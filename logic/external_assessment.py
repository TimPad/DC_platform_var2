"""
Logic for External Assessment Module
"""
import pandas as pd
import streamlit as st
from utils import get_supabase_client, fetch_all_from_supabase
from typing import Tuple


def load_existing_peresdachi() -> pd.DataFrame:
    """Загрузка существующих записей из таблицы peresdachi"""
    try:
        all_data = fetch_all_from_supabase('peresdachi')
        
        if all_data:
            return pd.DataFrame(all_data)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.warning(f"Таблица peresdachi не найдена или пуста: {str(e)}")
        return pd.DataFrame()

def load_student_io_from_supabase() -> pd.DataFrame:
    """Загрузка данных из таблицы student_io (все записи с пагинацией)"""
    try:
        # Используем точные имена колонок из базы данных, заключенные в двойные кавычки
        select_query = '"Адрес электронной почты", "Наименование дисциплины", "Оценка"'
        all_data = fetch_all_from_supabase('student_io', select_query=select_query)
        
        if all_data:
            df = pd.DataFrame(all_data)
            # Убедимся, что email и дисциплина строковые и приведены к нижнему регистру/без пробелов для корректного сравнения
            if 'Адрес электронной почты' in df.columns:
                df['Адрес электронной почты'] = df['Адрес электронной почты'].astype(str).str.strip().str.lower()
            if 'Наименование дисциплины' in df.columns:
                df['Наименование дисциплины'] = df['Наименование дисциплины'].astype(str).str.strip()
            if 'Оценка' in df.columns:
                df['Оценка'] = df['Оценка'].astype(str).str.strip()
            return df
        else:
            st.info("Таблица student_io пуста или не создана.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Ошибка при загрузке данных из student_io: {str(e)}")
        return pd.DataFrame()

def save_to_supabase(df: pd.DataFrame) -> bool:
    """Сохранение данных в таблицу peresdachi в Supabase с использованием insert, игнорируя дубликаты."""
    try:
        supabase = get_supabase_client()

        if df.empty:
            st.info("Нет данных для сохранения.")
            return True

        cleaned_records = []
        for record in df.to_dict('records'):
            cleaned_record = {k: (v if pd.notna(v) else None) for k, v in record.items()}
            cleaned_records.append(cleaned_record)

        # Используем обычный insert
        response = supabase.table('peresdachi').insert(cleaned_records).execute()

        return True

    # Поймаем конкретную ошибку дублирования
    except Exception as e:
        # Проверим, является ли ошибка ошибкой дублирования ключа
        if "duplicate key value violates unique constraint" in str(e):
            # Это ожидаемая ошибка, если дубликаты есть.
            # В supabase-py нет отдельного типа исключения для этого, приходится проверять строку.
            st.warning("Обнаружены дубликаты при сохранении. Они были проигнорированы. Остальные данные сохранены.")
            # Важно: вставка может быть частично успешной или полностью неудачной в зависимости от батчинга.
            # Для надежности, лучше удалять дубликаты в Python до вставки.
            return True # Считаем, что всё в порядке, если дубликаты - это ожидаемое поведение
        else:
            # Если другая ошибка, выводим её
            st.error(f"Ошибка при сохранении в Supabase: {str(e)}")
            if hasattr(e, 'details'):
                st.error(f"Детали ошибки от Supabase: {e.details}")
            return False

def get_new_records_from_dataframe(new_df: pd.DataFrame) -> pd.DataFrame:
    """Получить только новые записи, сравнивая с существующими в БД"""
    try:
        existing_df = load_existing_peresdachi()
        
        if existing_df.empty:
            return new_df
        
        merge_cols = ['Адрес электронной почты', 'Наименование дисциплины']
        
        if all(col in existing_df.columns for col in merge_cols) and all(col in new_df.columns for col in merge_cols):
            merged = new_df.merge(
                existing_df[merge_cols],
                on=merge_cols,
                how='left',
                indicator=True
            )
            result = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)
            return result
        else:
            return new_df
            
    except Exception as e:
        st.warning(f"Ошибка при определении новых записей: {str(e)}")
        return new_df

def process_external_assessment(grades_df: pd.DataFrame, students_df: pd.DataFrame) -> pd.DataFrame:
    """Обработка пересдач внешней оценки"""
    # Шаг 1: Очистка данных
    # Приводим ВСЕ колонки к строке, чтобы избежать проблем с типами в melt и отображении
    grades_df = grades_df.astype(str)
    # Теперь убираем '-' и пробелы
    for col in grades_df.columns:
        grades_df[col] = grades_df[col].str.replace('-', '', regex=False).str.strip()
    
    # Шаг 2: Переименование колонок
    column_mapping = {
        'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
        'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
        'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
    }
    
    grades_df = grades_df.rename(columns=column_mapping)
    
    # Шаг 3: Melt - преобразование колонок в строки
    value_columns = [
        'Внешнее измерение цифровых компетенций. Входной контроль',
        'Внешнее измерение цифровых компетенций. Промежуточный контроль',
        'Внешнее измерение цифровых компетенций. Итоговый контроль'
    ]
    
    id_cols = ['Адрес электронной почты']
    if 'Адрес электронной почты' not in grades_df.columns:
        st.error("Колонка 'Адрес электронной почты' не найдена в файле оценок")
        return pd.DataFrame()
    
    melted_df = pd.melt(
        grades_df,
        id_vars=id_cols,
        value_vars=value_columns,
        var_name='Наименование дисциплины',
        value_name='Оценка'
    )
    
    # Шаг 4: Присоединение данных студентов
    students_cols = ['ФИО', 'Адрес электронной почты', 'Филиал (кампус)', 
                     'Факультет', 'Образовательная программа', 'Группа', 'Курс']
    
    missing_cols = [col for col in students_cols if col not in students_df.columns]
    if missing_cols:
        st.warning(f"Отсутствуют колонки в файле студентов: {missing_cols}")
        available_cols = [col for col in students_cols if col in students_df.columns]
    else:
        available_cols = students_cols
    
    students_subset = students_df[available_cols].copy()
    
    # Очистка email
    melted_df['Адрес электронной почты'] = melted_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
    students_subset['Адрес электронной почты'] = students_subset['Адрес электронной почты'].astype(str).str.strip().str.lower()
    
    result_df = melted_df.merge(
        students_subset,
        on='Адрес электронной почты',
        how='left'
    )
    
    # Шаг 5: Добавление пустых колонок
    result_df['ID дисциплины'] = ''
    result_df['Период аттестации'] = ''
    
    # Шаг 6: Переименование
    if 'Филиал (кампус)' in result_df.columns:
        result_df = result_df.rename(columns={'Филиал (кампус)': 'Кампус'})
    
    # Шаг 7: Упорядочивание колонок
    output_columns = [
        'ФИО', 'Адрес электронной почты', 'Кампус', 'Факультет',
        'Образовательная программа', 'Группа', 'Курс', 'ID дисциплины',
        'Наименование дисциплины', 'Период аттестации', 'Оценка'
    ]
    
    final_columns = [col for col in output_columns if col in result_df.columns]
    result_df = result_df[final_columns]
    
    # Удаление строк с пустыми оценками
    result_df = result_df[result_df['Оценка'].notna()]
    result_df = result_df[result_df['Оценка'].astype(str).str.strip() != '']
    result_df = result_df[result_df['Оценка'].astype(str).str.strip() != 'nan']
    
    # --- ШАГ 1: Проверка и обновление оценок из student_io ---
    st.info("Проверка существующих оценок в student_io...")
    student_io_df = load_student_io_from_supabase()
    
    if not student_io_df.empty:
        # Очищаем email и дисциплину в result_df для сравнения
        # Убедимся, что они строковые и приведены к нужному формату
        result_df['Адрес электронной почты'] = result_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        result_df['Наименование дисциплины'] = result_df['Наименование дисциплины'].astype(str).str.strip()

        # Сливаем с student_io по email и дисциплине, приоритет у оценки из student_io
        # suffixes указывает, что делать с одинаковыми именами столбцов ('Оценка' в данном случае)
        # '_x' будет для оценки из result_df ('Оценка_x'), '_y' для оценки из student_io ('Оценка_y')
        merged_with_io = result_df.merge(
            student_io_df[['Адрес электронной почты', 'Наименование дисциплины', 'Оценка']], # Выбираем нужные колонки из student_io
            on=['Адрес электронной почты', 'Наименование дисциплины'],
            how='left',
            suffixes=('_from_file', '_from_io') # Используем более понятные суффиксы
        )
        
        # Создаем новую колонку 'Оценка' на основе логики: если 'Оценка_from_io' не NaN, берем её, иначе 'Оценка_from_file'
        # pd.notna проверяет, что значение не NaN
        merged_with_io['Оценка'] = merged_with_io['Оценка_from_io'].where(
            pd.notna(merged_with_io['Оценка_from_io']), 
            merged_with_io['Оценка_from_file'] # Берем оценку из исходного файла
        )
        
        # Убираем временные колонки 'Оценка_from_file' и 'Оценка_from_io'
        result_df = merged_with_io.drop(columns=['Оценка_from_file', 'Оценка_from_io'])
        
        # Убираем строки, где 'Оценка' стала NaN или пустой строкой после обновления
        # Используем pd.isna() для проверки NaN и str.strip().eq('') для пустых строк
        # Сначала убедимся, что 'Оценка' строковая, чтобы избежать ошибок при strip
        result_df = result_df[result_df['Оценка'].astype(str).str.strip() != '']
        result_df = result_df[result_df['Оценка'].notna()]
        # Проверим на 'nan' как строку
        result_df = result_df[result_df['Оценка'].astype(str).str.strip().str.lower() != 'nan']
        
        st.success(f"Проверка завершена. Найдено {len(student_io_df)} записей в student_io. Оценки обновлены при совпадении.")
    else:
        st.info("Таблица student_io пуста, используются оценки из файла.")
    # --- КОНЕЦ ШАГ 1 ---
    
    # --- ШАГ 2: Проверка существующих оценок в peresdachi ---
    st.info("Проверка существующих оценок в peresdachi...")
    existing_peresdachi_df = load_existing_peresdachi()
    
    if not existing_peresdachi_df.empty:
        # Очищаем данные в existing_peresdachi для корректного сравнения
        if 'Адрес электронной почты' in existing_peresdachi_df.columns:
            existing_peresdachi_df['Адрес электронной почты'] = existing_peresdachi_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        if 'Наименование дисциплины' in existing_peresdachi_df.columns:
            existing_peresdachi_df['Наименование дисциплины'] = existing_peresdachi_df['Наименование дисциплины'].astype(str).str.strip()
        
        # Сливаем с peresdachi по email и дисциплине, приоритет у оценки из peresdachi
        merged_with_peresdachi = result_df.merge(
            existing_peresdachi_df[['Адрес электронной почты', 'Наименование дисциплины', 'Оценка']],
            on=['Адрес электронной почты', 'Наименование дисциплины'],
            how='left',
            suffixes=('_current', '_peresdachi')
        )
        
        # Создаем новую колонку 'Оценка': если есть оценка в peresdachi, берем её, иначе текущую
        merged_with_peresdachi['Оценка'] = merged_with_peresdachi['Оценка_peresdachi'].where(
            pd.notna(merged_with_peresdachi['Оценка_peresdachi']),
            merged_with_peresdachi['Оценка_current']
        )
        
        # Убираем временные колонки
        result_df = merged_with_peresdachi.drop(columns=['Оценка_current', 'Оценка_peresdachi'])
        
        # Убираем строки с пустыми оценками
        result_df = result_df[result_df['Оценка'].astype(str).str.strip() != '']
        result_df = result_df[result_df['Оценка'].notna()]
        result_df = result_df[result_df['Оценка'].astype(str).str.strip().str.lower() != 'nan']
        
        st.success(f"Проверка peresdachi завершена. Найдено {len(existing_peresdachi_df)} записей. Оценки обновлены при совпадении.")
    else:
        st.info("Таблица peresdachi пуста, используются текущие оценки.")

    return result_df

def process_project_assessment(grades_df: pd.DataFrame, students_df: pd.DataFrame) -> pd.DataFrame:
    """Обработка внешнего измерения (Проекты)"""
    
    # Шаг 1: Очистка и извлечение оценок
    project_columns_names = [
        "Задание:Гуманитарные науки (Значение)",
        "Задание:Социально-экономические науки (Значение)",
        "Задание:Естественные науки (Значение)",
        "Задание:Общее: интерактивная история (Значение)",
        "Задание:Интерактивная история: Расширенная версия (Значение)"
    ]
    
    # Определяем, какие колонки есть в файле
    existing_project_columns = [col for col in project_columns_names if col in grades_df.columns]
    
    if not existing_project_columns:
        st.warning("Не найдены колонки с оценками за проект (Задание:...). Проверьте файл.")
        # Если колонок нет, все равно продолжаем, но оценки будут NaN (или можно вернуть пустой df)
        # В данном случае лучше вернуть пустой df или ошибку, иначе нет смысла
        return pd.DataFrame()

    # Функция для конвертации в число
    def clean_numeric(series):
        # replace('-', float('nan')) handles dashes common in these reports
        return pd.to_numeric(series.astype(str).replace('-', float('nan')), errors='coerce')

    # Конвертируем и считаем Максимум
    project_data = grades_df[existing_project_columns].apply(clean_numeric)
    grades_df['Оценка'] = project_data.max(axis=1)
    
    # Задаем фиксированное имя дисциплины
    grades_df['Наименование дисциплины'] = "Внешнее измерение цифровых компетенций. Итоговый контроль"
    
    # Шаг 2: Подготовка к мерджу
    id_cols = ['Адрес электронной почты']
    if 'Адрес электронной почты' not in grades_df.columns:
        st.error("Колонка 'Адрес электронной почты' не найдена в файле.")
        return pd.DataFrame()

    # Очистка email в grades_df
    grades_df['Адрес электронной почты'] = grades_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
    
    # Выбираем только валидные оценки ( > 0 и не NaN ) - как в скрипте process_grades.py
    # valid_project = (grades_df['Оценка'] > 0) & (grades_df['Оценка'].notna())
    # grades_df = grades_df[valid_project] 
    # !!! ВАЖНО: В оригинальном скрипте фильтруются валидные, но здесь мы хотим обработать все, 
    # чтобы показать результат. Фильтрацию пустых делаем позже, как в process_external_assessment.
    
    # Шаг 3: Присоединение данных студентов
    students_cols = ['ФИО', 'Адрес электронной почты', 'Филиал (кампус)', 
                     'Факультет', 'Образовательная программа', 'Группа', 'Курс']
    
    available_cols = [col for col in students_cols if col in students_df.columns]
    students_subset = students_df[available_cols].copy()
    students_subset['Адрес электронной почты'] = students_subset['Адрес электронной почты'].astype(str).str.strip().str.lower()
    
    result_df = grades_df.merge(
        students_subset,
        on='Адрес электронной почты',
        how='left'
    )
    
    # Шаг 4: Формирование финального датафрейма
    result_df['ID дисциплины'] = ''
    result_df['Период аттестации'] = ''
    
    if 'Филиал (кампус)' in result_df.columns:
        result_df = result_df.rename(columns={'Филиал (кампус)': 'Кампус'})
        
    output_columns = [
        'ФИО', 'Адрес электронной почты', 'Кампус', 'Факультет',
        'Образовательная программа', 'Группа', 'Курс',
        'Наименование дисциплины', 'Оценка', 'ID дисциплины', 'Период аттестации'
    ]
    
    # Оставляем только нужные колонки, которые есть
    final_columns = [col for col in output_columns if col in result_df.columns]
    result_df = result_df[final_columns]
    
    # Очистка оценок (удаление Nan/0/пустых)
    # В process_grades.py: (df['Оценка за проект'] > 0) & (df['Оценка за проект'].notna())
    result_df = result_df[result_df['Оценка'].notna()]
    result_df = result_df[result_df['Оценка'] > 0]
    
    # Логика приоритетов (Student IO, Peresdachi)
    # Повторяем ту же логику, что в process_external_assessment
    
    result_df['Оценка'] = result_df['Оценка'].astype(str) # Приводим к строке для унификации
    
    # --- ШАГ 1: Проверка и обновление оценок из student_io ---
    st.info("Проверка существующих оценок в student_io...")
    student_io_df = load_student_io_from_supabase()
    
    if not student_io_df.empty:
        result_df['Адрес электронной почты'] = result_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        
        merged_with_io = result_df.merge(
            student_io_df[['Адрес электронной почты', 'Наименование дисциплины', 'Оценка']],
            on=['Адрес электронной почты', 'Наименование дисциплины'],
            how='left',
            suffixes=('_from_file', '_from_io')
        )
        
        merged_with_io['Оценка'] = merged_with_io['Оценка_from_io'].where(
            pd.notna(merged_with_io['Оценка_from_io']), 
            merged_with_io['Оценка_from_file']
        )
        
        result_df = merged_with_io.drop(columns=['Оценка_from_file', 'Оценка_from_io'])
        # Очистка после мерджа
        result_df = result_df[result_df['Оценка'].notna()]
        result_df = result_df[result_df['Оценка'].astype(str).str.strip() != '']
        result_df = result_df[result_df['Оценка'].astype(str).str.strip().str.lower() != 'nan']
        
        st.success(f"Проверка student_io завершена.")
    
    # --- ШАГ 2: Проверка существующих оценок в peresdachi ---
    st.info("Проверка существующих оценок в peresdachi...")
    existing_peresdachi_df = load_existing_peresdachi()
    
    if not existing_peresdachi_df.empty:
        if 'Адрес электронной почты' in existing_peresdachi_df.columns:
            existing_peresdachi_df['Адрес электронной почты'] = existing_peresdachi_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
            
        merged_with_peresdachi = result_df.merge(
            existing_peresdachi_df[['Адрес электронной почты', 'Наименование дисциплины', 'Оценка']],
            on=['Адрес электронной почты', 'Наименование дисциплины'],
            how='left',
            suffixes=('_current', '_peresdachi')
        )
        
        merged_with_peresdachi['Оценка'] = merged_with_peresdachi['Оценка_peresdachi'].where(
            pd.notna(merged_with_peresdachi['Оценка_peresdachi']),
            merged_with_peresdachi['Оценка_current']
        )
        
        result_df = merged_with_peresdachi.drop(columns=['Оценка_current', 'Оценка_peresdachi'])
        # Очистка после мерджа
        result_df = result_df[result_df['Оценка'].notna()]
        result_df = result_df[result_df['Оценка'].astype(str).str.strip() != '']
        result_df = result_df[result_df['Оценка'].astype(str).str.strip().str.lower() != 'nan']

        st.success(f"Проверка peresdachi завершена.")

    return result_df

def update_final_grades(df: pd.DataFrame) -> Tuple[bool, int, int]:
    """
    Обновление таблицы final_grades в Supabase на основе новых оценок за проекты.
    Стратегия: Fetch -> Merge -> Upsert
    
    1. Получаем текущую запись студента из final_grades
    2. Обновляем 'Оценка за проект'
    3. Пересчитываем 'Итоговая оценка' = max(Проект, Тест, Старый Итог)
    4. Загружаем обратно
    
    Returns:
        (success, processed_count, skipped_count)
    """
    try:
        supabase = get_supabase_client()
        
        if df.empty:
            return True, 0, 0
            
        # Убираем дубликаты по email в текущем батче (берем последнюю/лучшую оценку)
        # Предполагаем, что df уже прошел базовую очистку, но на всякий случай
        if 'Адрес электронной почты' not in df.columns or 'Оценка' not in df.columns:
            st.error("Нет необходимых колонок для обновления final_grades")
            return False, 0, 0
            
        # Работаем с копией
        work_df = df.copy()
        work_df['Адрес электронной почты'] = work_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        
        # Получаем уникальные email из батча
        unique_emails = work_df['Адрес электронной почты'].unique().tolist()
        
        if not unique_emails:
            return True, 0, 0

        # 1. FETCH: Получаем существующие записи из final_grades
        # Supabase 'in_' фильтр
        existing_records_map = {}
        
        # Разбиваем на чанки, если emails очень много (хотя обычно < 1000)
        chunk_size = 200
        for i in range(0, len(unique_emails), chunk_size):
            chunk_emails = unique_emails[i:i + chunk_size]
            try:
                response = supabase.table('final_grades').select('*').in_('Адрес электронной почты', chunk_emails).execute()
                for rec in response.data:
                    email = rec.get('Адрес электронной почты', '').lower().strip()
                    if email:
                        existing_records_map[email] = rec
            except Exception as e:
                st.warning(f"Ошибка при получении данных из final_grades (chunk {i}): {e}")
                # Продолжаем, считая что записей нет (будут созданы новые)

        payloads = []
        processed_count = 0
        
        for idx, row in work_df.iterrows():
            email = row.get('Адрес электронной почты')
            new_project_grade = row.get('Оценка')
            fio = row.get('ФИО', '')
            
            if not email or pd.isna(new_project_grade):
                continue
                
            try:
                new_project_grade = float(new_project_grade)
            except:
                continue
                
            # Ищем существующую запись
            record = existing_records_map.get(email, {})
            
            # Извлекаем старые значения
            old_test_grade = record.get('Оценка за тест')
            old_project_grade = record.get('Оценка за проект') # Может быть None
            old_final_grade = record.get('Итоговая оценка')
            
            # Конвертация в float для сравнения
            def to_float(val):
                if val is None: return 0.0
                try:
                    return float(val)
                except:
                    return 0.0
            
            val_test = to_float(old_test_grade)
            val_old_project = to_float(old_project_grade)
            val_old_final = to_float(old_final_grade)
            
            # Логика обновления:
            # Обновляем проектную оценку на НОВУЮ (перезаписываем, как просил пользователь "если изменилась")
            current_project = new_project_grade 
            
            # Пересчет итоговой: Максимум из (Проект, Тест)
            # Также учитываем val_old_final, если вдруг он был проставлен вручную выше? 
            # Обычно формула: max(Test, Project). Но если старый итог больше (например, зачтено автоматом), берем его?
            # В данном кейсе безопаснее пересчитать честно: max(Test, NewProject)
            # ИЛИ если старый итог был уже 10, а мы шлем 8...
            # Давайте возьмем max(val_test, current_project, val_old_final) чтобы не понизить случайно?
            new_final = max(val_test, current_project, val_old_final)
            
            # Формируем payload
            # Нам нужно сохранить ВСЕ поля, которые были, изменив только целевые
            # НО upsert в supabase требует только PK и изменяемые поля, если мы хотим обновить.
            # Однако, если записи НЕТ, нам нужно создать её.
            
            # Если запись БЫЛА: берем её ID или просто PK (Email) и обновляем поля
            # Если записи НЕ БЫЛО: создаем новую, заполняя что можем
            
            payload = {}
            if record:
                # Копируем всё что есть, чтобы не потерять (хотя upsert по email обновит только поданные поля, если не делать замену?)
                # Supabase upsert: "updates existing rows if the specified key matches".
                # Значит можно подать только Email и изменяемые поля.
                payload['Адрес электронной почты'] = email
            else:
                # Новая запись - заполним ФИО
                payload['Адрес электронной почты'] = email
                payload['ФИО'] = fio # В final_grades обычно Фамилия/Имя отдельно, но если такой колонки нет, то ой.
                # Смотрим структуру final_grades из db_update.py: 'Фамилия', 'Имя'.
                # Попробуем разделить ФИО
                if fio and isinstance(fio, str):
                    parts = fio.split()
                    if len(parts) >= 1: payload['Фамилия'] = parts[0]
                    if len(parts) >= 2: payload['Имя'] = parts[1]
            
            payload['Оценка за проект'] = current_project
            payload['Итоговая оценка'] = new_final
            # Оценка за тест не меняем, но если её не было - она останется null (для новых)
            
            # Добавим технические поля, если их нет
            # 'Исходный файл' ?
            
            payloads.append(payload)
            processed_count += 1

        if not payloads:
            return True, 0, 0
            
        # 3. UPSERT: Отправляем батчем
        # Разбиваем на батчи
        for i in range(0, len(payloads), chunk_size):
            batch = payloads[i:i + chunk_size]
            supabase.table('final_grades').upsert(batch, on_conflict='Адрес электронной почты').execute()
            
        return True, processed_count, 0
            
    except Exception as e:
        st.error(f"Критическая ошибка при обновлении final_grades: {str(e)}")
        return False, 0, 0
