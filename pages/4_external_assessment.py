"""
Модуль 4: Обработка пересдач внешней оценки
Supabase интеграция для пересдач
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
from typing import Tuple
from utils import icon, apply_custom_css, get_supabase_client

# Применяем кастомные стили
apply_custom_css()

# Заголовок страницы
st.markdown(
    f'<h1>{icon("file-edit", 32)} Обработка пересдач внешней оценки</h1>',
    unsafe_allow_html=True
)

st.markdown("""
Автоматическая обработка пересдач из внешней системы оценивания с интеграцией Supabase.

**Требуется:**
1. **Файл с оценками** - таблица из внешней системы с тестированиями
2. **Список студентов** - загружается автоматически из Supabase (таблица `students`)

**Что делает инструмент:**
- Очищает данные от лишних символов и пробелов
- Переименовывает колонки в соответствии со стандартами
- Преобразует данные из широкого в длинный формат (melt)
- Объединяет данные с информацией о студентах из Supabase
- Проверяет существующие оценки в `student_io` и использует их, если найдены
- Сохраняет результаты в таблицу `peresdachi` в Supabase
- Позволяет скачать все данные или только новые записи
""")

def load_paginated_data(table: str, select: str = '*', filters: dict = None, page_size: int = 1000) -> pd.DataFrame:
    """Загрузка данных с пагинацией, оптимизированная с помощью .count()"""
    supabase = get_supabase_client()
    
    # Сначала получаем общее количество записей
    count_res = supabase.table(table).select('*', count='exact')
    if filters:
        for key, val in filters.items():
            count_res = count_res.eq(key, val)
    count_response = count_res.execute()
    total = count_response.count
    
    if total == 0:
        return pd.DataFrame()
    
    all_data = []
    progress_bar = st.progress(0)
    
    for i, offset in enumerate(range(0, total, page_size)):
        res = supabase.table(table).select(select).range(offset, min(offset + page_size - 1, total - 1))
        if filters:
            for key, val in filters.items():
                res = res.eq(key, val)
        response = res.execute()
        all_data.extend(response.data)
        
        # Обновляем прогресс-бар
        progress = (i + 1) * page_size / total
        progress_bar.progress(min(progress, 1.0))
    
    progress_bar.empty()  # Убираем прогресс-бар после завершения
    return pd.DataFrame(all_data)

def load_students_from_supabase() -> pd.DataFrame:
    """Загрузка списка студентов из Supabase (все записи с пагинацией)"""
    try:
        # Загружаем студентов только 4 курса
        df = load_paginated_data('students', filters={'курс': 'Курс 4'})
        
        if df.empty:
            st.warning("Таблица students пуста или нет студентов на Курсе 4 в Supabase")
            return pd.DataFrame()
        
        # Переименование колонок из формата Supabase в требуемый формат
        column_mapping = {
            'корпоративная_почта': 'Адрес электронной почты',
            'фио': 'ФИО',
            'филиал_кампус': 'Филиал (кампус)',
            'факультет': 'Факультет',
            'образовательная_программа': 'Образовательная программа',
            'версия_образовательной_программы': 'Версия образовательной программы',
            'группа': 'Группа',
            'курс': 'Курс'
        }
        
        existing_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=existing_columns)
        
        return df
    except Exception as e:
        st.error(f"Ошибка при загрузке студентов из Supabase: {str(e)}")
        return pd.DataFrame()

def load_existing_peresdachi() -> pd.DataFrame:
    """Загрузка существующих записей из таблицы peresdachi"""
    try:
        return load_paginated_data('peresdachi')
    except Exception as e:
        st.warning(f"Таблица peresdachi не найдена или пуста: {str(e)}")
        return pd.DataFrame()

def load_student_io_from_supabase() -> pd.DataFrame:
    """Загрузка данных из таблицы student_io (все записи с пагинацией)"""
    try:
        df = load_paginated_data('student_io', select='"Адрес электронной почты", "Наименование дисциплины", "Оценка"')
        
        if df.empty:
            st.info("Таблица student_io пуста или не создана.")
            return pd.DataFrame()
        
        # Убедимся, что email и дисциплина строковые и приведены к нижнему регистру/без пробелов для корректного сравнения
        if 'Адрес электронной почты' in df.columns:
            df['Адрес электронной почты'] = df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        if 'Наименование дисциплины' in df.columns:
            df['Наименование дисциплины'] = df['Наименование дисциплины'].astype(str).str.strip()
        if 'Оценка' in df.columns:
            df['Оценка'] = df['Оценка'].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Ошибка при загрузке данных из student_io: {str(e)}")
        return pd.DataFrame()

def save_to_supabase(df: pd.DataFrame) -> bool:
    """Сохранение данных в таблицу peresdachi в Supabase"""
    try:
        supabase = get_supabase_client()
        
        if df.empty:
            return True  # Нечего сохранять, считаем успехом
        
        cleaned_records = []
        for record in df.to_dict('records'):
            cleaned_record = {k: (v if pd.notna(v) else None) for k, v in record.items()}
            cleaned_records.append(cleaned_record)
        
        # Используем upsert для предотвращения дубликатов, если есть primary key
        response = supabase.table('peresdachi').upsert(cleaned_records).execute()
        return True
        
    except Exception as e:
        st.error(f"Ошибка при сохранении в Supabase: {str(e)}")
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
    # Шаг 1: Очистка данных - убираем дефисы и пробелы
    grades_df = grades_df.applymap(lambda x: str(x).replace('-', '').strip() if isinstance(x, str) else x)
    
    # Шаг 2: Переименование колонок
    column_mapping = {
        'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
        'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
        'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
    }
    
    grades_df = grades_df.rename(columns=column_mapping)
    
    # Шаг 3: Melt - преобразование колонок в строки (оптимально как есть)
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
    
    # --- НОВЫЙ ШАГ: Проверка и обновление оценок из student_io ---
    st.info("Проверка существующих оценок в student_io...")
    student_io_df = load_student_io_from_supabase()
    
    if not student_io_df.empty:
        # Очищаем email и дисциплину в result_df для сравнения
        result_df['Адрес электронной почты'] = result_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        result_df['Наименование дисциплины'] = result_df['Наименование дисциплины'].astype(str).str.strip()

        # Сливаем с student_io по email и дисциплине
        merged_with_io = result_df.merge(
            student_io_df[['Адрес электронной почты', 'Наименование дисциплины', 'Оценка']].rename(
                columns={'Оценка': 'Оценка_from_io'}
            ),
            on=['Адрес электронной почты', 'Наименование дисциплины'],
            how='left',
            suffixes=('', '_from_file') # Оставляем оригинальную 'Оценка' как 'Оценка_from_file'
        )
        
        # Используем combine_first для приоритета оценки из student_io
        merged_with_io['Оценка'] = merged_with_io['Оценка_from_io'].combine_first(merged_with_io['Оценка_from_file'])
        
        # Убираем временные колонки
        result_df = merged_with_io.drop(columns=['Оценка_from_file', 'Оценка_from_io'])
        
        st.success(f"Проверка завершена. Найдено {len(student_io_df)} записей в student_io. Оценки обновлены при совпадении.")
    else:
        st.info("Таблица student_io пуста, используются оценки из файла.")
    # --- КОНЕЦ НОВОГО ШАГА ---
    
    # Удаление строк с пустыми оценками
    result_df = result_df.replace({'Оценка': {'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA}}).dropna(subset=['Оценка'])
    
    return result_df

# Проверка подключения к Supabase
try:
    supabase = get_supabase_client()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения к Supabase: {str(e)}")
    st.stop()

st.markdown("---")

# Загрузка файла с оценками
st.subheader("Загрузка файла с оценками")
with st.form("upload_form"):
    grades_file = st.file_uploader(
        "Выберите файл с оценками (external_assessment)",
        type=['xlsx', 'xls'],
        key="external_grades_file",
        help="Файл должен содержать колонки: Адрес электронной почты, Тест:Входное/Промежуточное/Итоговое тестирование (Значение)"
    )
    submit_button = st.form_submit_button("Обработать данные", type="primary")

if grades_file:
    try:
        with st.spinner("Загрузка файла с оценками..."):
            grades_df = pd.read_excel(grades_file)
        
        st.success("Файл с оценками успешно загружен!")
        
        # Загрузка студентов из Supabase
        with st.spinner("Загрузка списка студентов из Supabase..."):
            students_df = load_students_from_supabase()
        
        if students_df.empty:
            st.error("Список студентов пуст. Загрузите данные в таблицу `students` в Supabase.")
            st.stop()
        else:
            st.success(f"Загружено {len(students_df)} студентов из Supabase")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Записей с оценками", len(grades_df))
        with col2:
            st.metric("Студентов в базе", len(students_df))
        with col3:
            st.metric("Колонок в оценках", len(grades_df.columns))
        
        col_preview1, col_preview2 = st.columns(2)
        with col_preview1:
            with st.expander("Предпросмотр файла с оценками"):
                st.dataframe(grades_df.head(), use_container_width=True)
        
        with col_preview2:
            with st.expander("Предпросмотр списка студентов"):
                st.dataframe(students_df.head(10), use_container_width=True)
        
        if submit_button:
            with st.spinner("Обработка пересдач..."):
                try:
                    result_df = process_external_assessment(grades_df, students_df)
                    
                    if result_df.empty:
                        st.error("Не удалось обработать данные. Проверьте структуру файла.")
                    else:
                        st.success("Обработка успешно завершена!")
                        
                        # Определяем новые записи ДО сохранения в БД
                        with st.spinner("Определение новых записей..."):
                            display_new_records = get_new_records_from_dataframe(result_df)
                            new_count = len(display_new_records)
                            total_count = len(result_df)
                        
                        # Сохранение в Supabase только новых записей
                        with st.spinner("Сохранение новых записей в Supabase..."):
                            new_df = get_new_records_from_dataframe(result_df)
                            if not new_df.empty:
                                save_success = save_to_supabase(new_df)
                                if save_success:
                                    st.success(f"Сохранено в Supabase: {len(new_df)} новых записей из {total_count}")
                                else:
                                    st.error("Ошибка при сохранении данных в Supabase")
                                    st.stop()  # Прерываем, если не удалось сохранить
                            else:
                                st.info("Все записи уже существовали в базе данных.")
                        
                        # Статистика
                        st.subheader("Результаты обработки")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Всего обработано записей", total_count)
                        with col2:
                            st.metric("Новых записей", new_count)
                        with col3:
                            existing_count = total_count - new_count
                            st.metric("Уже существовало", existing_count)
                        
                        # Предпросмотр
                        tab1, tab2 = st.tabs(["Все обработанные данные", "Только новые записи"])
                        
                        with tab1:
                            st.dataframe(result_df, use_container_width=True)
                            
                            output_all = io.BytesIO()
                            with pd.ExcelWriter(output_all, engine='openpyxl') as writer:
                                result_df.to_excel(writer, index=False, sheet_name='Все пересдачи')
                            output_all.seek(0)
                            
                            current_date = datetime.now().strftime('%d-%m-%Y')
                            download_filename_all = f"Пересдачи_все_{current_date}.xlsx"
                            
                            st.download_button(
                                label="Скачать все записи (XLSX)",
                                data=output_all.getvalue(),
                                file_name=download_filename_all,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="download_all"
                            )
                        
                        with tab2:
                            if display_new_records.empty:
                                st.info("Новых записей нет. Все данные уже были в базе.")
                            else:
                                st.dataframe(display_new_records, use_container_width=True)
                                
                                output_new = io.BytesIO()
                                with pd.ExcelWriter(output_new, engine='openpyxl') as writer:
                                    display_new_records.to_excel(writer, index=False, sheet_name='Новые пересдачи')
                                output_new.seek(0)
                                
                                download_filename_new = f"Пересдачи_новые_{current_date}.xlsx"
                                
                                st.download_button(
                                    label="Скачать только новые записи (XLSX)",
                                    data=output_new.getvalue(),
                                    file_name=download_filename_new,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="download_new"
                                )
                        
                        # Дополнительная статистика
                        with st.expander("Статистика по обработке"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Распределение по дисциплинам:**")
                                if 'Наименование дисциплины' in result_df.columns:
                                    discipline_counts = result_df['Наименование дисциплины'].value_counts()
                                    st.dataframe(discipline_counts)
                            
                            with col2:
                                st.write("**Уникальные студенты:**")
                                if 'ФИО' in result_df.columns:
                                    unique_students = result_df['ФИО'].nunique()
                                    st.metric("Уникальных студентов", unique_students)
                
                except Exception as e:
                    st.error(f"Ошибка при обработке: {str(e)}")
                    st.exception(e)
    
    except Exception as e:
        st.error(f"Ошибка при загрузке файла: {str(e)}")
        st.exception(e)

else:
    st.info("Загрузите файл с оценками для начала работы")
    
    # Показываем текущее состояние базы данных
    with st.expander("Текущее состояние базы данных"):
        existing_peresdachi = load_existing_peresdachi()
        if existing_peresdachi.empty:
            st.info("Таблица peresdachi пуста или не создана")
        else:
            st.metric("Записей в таблице peresdachi", len(existing_peresdachi))
            st.dataframe(existing_peresdachi.head(10), use_container_width=True)
