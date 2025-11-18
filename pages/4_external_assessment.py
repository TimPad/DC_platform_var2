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

# --- НОВАЯ УНИВЕРСАЛЬНАЯ ФУНКЦИЯ ЗАГРУЗКИ С КЭШИРОВАНИЕМ И ПАГИНАЦИЕЙ ---
@st.cache_data(ttl=3600, show_spinner="Загрузка данных из Supabase...")
def fetch_all(table: str, filters: dict = None, columns: str = "*"):
    """Универсальная загрузка с пагинацией и кэшированием"""
    supabase = get_supabase_client()
    query = supabase.table(table).select(columns)
    
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    
    data = []
    offset = 0
    while True:
        resp = query.range(offset, offset + 999).execute()
        if not resp.data:
            break
        data.extend(resp.data)
        if len(resp.data) < 1000:
            break
        offset += 1000
    
    return pd.DataFrame(data) if data else pd.DataFrame()
# --- КОНЕЦ НОВОЙ ФУНКЦИИ ---

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

# --- ОБНОВЛЁННАЯ ФУНКЦИЯ СОХРАНЕНИЯ С ПРАВИЛЬНЫМ UPSERT ---
def save_to_supabase(df: pd.DataFrame) -> bool:
    """
    Сохранение данных в таблицу peresdachi в Supabase с использованием upsert.
    Обновляет существующие записи по комбинации 'Адрес электронной почты', 'Наименование дисциплины'.
    """
    try:
        supabase = get_supabase_client()

        if df.empty:
            st.info("Данные для сохранения отсутствуют.")
            return True  # Нечего сохранять, считаем успехом

        # Подготовка данных: очистка NaN
        cleaned_records = []
        for record in df.to_dict('records'):
            cleaned_record = {k: (v if pd.notna(v) else None) for k, v in record.items()}
            cleaned_records.append(cleaned_record)

        # Выполнение upsert
        # on_conflict указывает, по каким полям определяется конфликт/уникальность
        # ВАЖНО: 'Оценка' исключена из уникального ключа
        response = (
            supabase.table('peresdachi')
            .upsert(
                cleaned_records,
                on_conflict=['Адрес электронной почты', 'Наименование дисциплины'] # <-- Поля, определяющие уникальность
            )
            .execute()
        )

        # response.data содержит вставленные/обновлённые записи
        st.success(f"Данные успешно сохранены/обновлены в Supabase (upsert).")
        return True

    except Exception as e:
        st.error(f"Ошибка при сохранении в Supabase: {str(e)}")
        # Для отладки можно раскомментировать следующую строку
        # st.exception(e)
        return False
# --- КОНЕЦ ОБНОВЛЁННОЙ ФУНКЦИИ ---

# --- УПРОЩЕННАЯ ФУНКЦИЯ ОБРАБОТКИ ---
def process_external_assessment(grades_df: pd.DataFrame, students_df: pd.DataFrame) -> pd.DataFrame:
    """Обработка пересдач внешней оценки"""
    # Шаг 1: Очистка данных
    for col in grades_df.columns:
        if grades_df[col].dtype == 'object':
            grades_df[col] = grades_df[col].astype(str).str.replace('-', '', regex=False).str.strip()
    
    # Шаг 2: Переименование колонок
    DISCIPLINE_MAPPING = {
        'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
        'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
        'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
    }
    
    grades_df = grades_df.rename(columns=DISCIPLINE_MAPPING)
    
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
    
    # --- НОВЫЙ ШАГ: Проверка и обновление оценок из student_io ---
    st.info("Проверка существующих оценок в student_io...")
    student_io_df = fetch_all(
        'student_io',
        columns='"Адрес электронной почты", "Наименование дисциплины", "Оценка"'
    )
    
    if not student_io_df.empty:
        # Очищаем email и дисциплину в result_df для сравнения
        result_df['Адрес электронной почты'] = result_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        result_df['Наименование дисциплины'] = result_df['Наименование дисциплины'].astype(str).str.strip()

        # --- КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: Переименовываем дисциплины в student_io_df ---
        # Предполагаем, что в student_io дисциплины хранятся в оригинальном формате
        # Создаём обратное маппинг-отображение
        REVERSE_DISCIPLINE_MAPPING = {v: k for k, v in DISCIPLINE_MAPPING.items()}
        
        # Применяем обратное переименование к student_io_df
        if 'Наименование дисциплины' in student_io_df.columns:
            # Заменяем дисциплины в student_io_df на формат до melt (до переименования)
            student_io_df['Наименование дисциплины'] = student_io_df['Наименование дисциплины'].map(REVERSE_DISCIPLINE_MAPPING).fillna(student_io_df['Наименование дисциплины'])
            # Теперь в student_io_df дисциплины в том же формате, что и в grades_df до melt

        # Очищаем student_io_df
        student_io_df['Адрес электронной почты'] = student_io_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        student_io_df['Наименование дисциплины'] = student_io_df['Наименование дисциплины'].astype(str).str.strip()

        # Теперь выполняем merge по email и дисциплине (в формате исходного файла)
        # Но result_df у нас уже в новом формате! 
        # Нужно временно вернуть дисциплины в result_df к старому формату для слияния
        temp_result_df = result_df.copy()
        temp_result_df['Наименование дисциплины'] = temp_result_df['Наименование дисциплины'].map(REVERSE_DISCIPLINE_MAPPING).fillna(temp_result_df['Наименование дисциплины'])

        # Сливаем
        merged_with_io = temp_result_df.merge(
            student_io_df[['Адрес электронной почты', 'Наименование дисциплины', 'Оценка']],
            on=['Адрес электронной почты', 'Наименование дисциплины'],
            how='left',
            suffixes=('', '_io') # Более простые суффиксы
        )
        
        # Переносим оценку из student_io, если она не NaN и не пустая строка
        # Сначала убедимся, что обе колонки 'Оценка' и 'Оценка_io' строковые для корректного сравнения
        merged_with_io['Оценка_io'] = merged_with_io['Оценка_io'].astype(str).str.strip()
        merged_with_io['Оценка'] = merged_with_io['Оценка'].astype(str).str.strip()
        
        # Создаём новую колонку 'Оценка', где приоритет у 'Оценка_io', если она не пустая
        # Используем combine_first, но сначала проверим на пустые строки
        # Создадим вспомогательную колонку, где NaN/пустые строки в 'Оценка_io' заменены на None
        mask_io_valid = merged_with_io['Оценка_io'].notna() & (merged_with_io['Оценка_io'] != '') & (merged_with_io['Оценка_io'].str.lower() != 'nan')
        merged_with_io['Оценка_final'] = merged_with_io['Оценка_io'].where(mask_io_valid, merged_with_io['Оценка'])
        
        # Присваиваем финальную оценку
        result_df = merged_with_io.drop(columns=['Оценка_io'], errors='ignore').rename(columns={'Оценка_final': 'Оценка'})
        
        st.success(f"Проверка завершена. Найдено {len(student_io_df)} записей в student_io. Оценки обновлены при совпадении.")
    else:
        st.info("Таблица student_io пуста, используются оценки из файла.")
    # --- КОНЕЦ НОВОГО ШАГА ---
    
    # Убираем строки, где 'Оценка' стала NaN или пустой строкой после обновления
    # Используем pd.isna() для проверки NaN и str.strip().eq('') для пустых строк
    # Сначала убедимся, что 'Оценка' строковая, чтобы избежать ошибок при strip
    result_df = result_df[result_df['Оценка'].astype(str).str.strip() != '']
    result_df = result_df[result_df['Оценка'].notna()]
    # Проверим на 'nan' как строку
    result_df = result_df[result_df['Оценка'].astype(str).str.strip().str.lower() != 'nan']
    
    return result_df
# --- КОНЕЦ ФУНКЦИИ ОБРАБОТКИ ---

# Проверка подключения к Supabase
try:
    supabase = get_supabase_client()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения к Supabase: {str(e)}")
    # Не используем st.stop() здесь, а просто выходим из блока
    st.stop() # Это оставляем, чтобы остановить выполнение скрипта, если нет подключения

st.markdown("---")

# Загрузка файла с оценками
st.subheader("Загрузка файла с оценками")
grades_file = st.file_uploader(
    "Выберите файл с оценками (external_assessment)",
    type=['xlsx', 'xls'],
    key="external_grades_file",
    help="Файл должен содержать колонки: Адрес электронной почты, Тест:Входное/Промежуточное/Итоговое тестирование (Значение)"
)

# --- КНОПКА ВЫНЕСЕНА СЮДА ---
process_triggered = st.button("Обработать данные", type="primary", disabled=not bool(grades_file), use_container_width=True)
# --- КОНЕЦ ВЫНОСА КНОПКИ ---

if grades_file:
    try:
        with st.spinner("Загрузка файла с оценками..."):
            grades_df = pd.read_excel(grades_file)
        
        # --- ПРОВЕРКА ОБЯЗАТЕЛЬНЫХ КОЛОНОК ---
        required_cols = ['Адрес электронной почты', 'Тест:Входное тестирование (Значение)']
        missing = [col for col in required_cols if col not in grades_df.columns]
        if missing:
            st.error(f"Не найдены обязательные колонки: {missing}")
        else:
            st.success("Файл с оценками успешно загружен!")

            # --- ЗАГРУЗКА СТУДЕНТОВ С ПОМОЩЬЮ НОВОЙ ФУНКЦИИ ---
            with st.spinner("Загрузка списка студентов из Supabase..."):
                students_df = fetch_all('students', filters={'курс': 'Курс 4'})
            
            if students_df.empty:
                st.error("Список студентов пуст. Загрузите данные в таблицу `students` в Supabase.")
                # Не используем st.stop() здесь, а просто выходим из блока
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
            
            # --- ОБНОВЛЁННЫЙ БЛОК ОБРАБОТКИ ---
            if process_triggered: # Условие теперь зависит от отдельной переменной
                with st.spinner("Обработка пересдач..."):
                    try:
                        result_df = process_external_assessment(grades_df, students_df)
                        
                        if result_df.empty:
                            st.error("Не удалось обработать данные. Проверьте структуру файла.")
                        else:
                            st.success("Обработка успешно завершена!")
                            
                            # --- УБРАНА ФУНКЦИЯ get_new_records_from_dataframe ---
                            # Определяем общее количество записей
                            total_count = len(result_df)
                            
                            # Сохранение в Supabase
                            with st.spinner("Сохранение в Supabase..."):
                                save_success = save_to_supabase(result_df)
                                if save_success:
                                    st.success(f"Данные успешно отправлены в Supabase (upsert).")
                                else:
                                    st.error("Ошибка при сохранении данных в Supabase")
                                    # Не используем st.stop() здесь, просто прерываем дальнейшую логику
                                    st.stop() # Останавливаем выполнение после ошибки
                            
                            # Статистика
                            st.subheader("Результаты обработки")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Записей обработано и отправлено", total_count)
                            with col2:
                                st.info("Дубли автоматически обновляются благодаря уникальному индексу в базе")
                            
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
                                # Показываем информацию о новизне
                                st.info("Точное количество новых записей можно увидеть только после сохранения (Supabase не возвращает счётчик при upsert)")
                                st.dataframe(result_df, use_container_width=True) # Показываем все, как пример
                                    
                                # Кнопка для новых записей не имеет смысла без точного подсчёта
                                # output_new = io.BytesIO()
                                # with pd.ExcelWriter(output_new, engine='openpyxl') as writer:
                                #     display_new_records.to_excel(writer, index=False, sheet_name='Новые пересдачи')
                                # output_new.seek(0)
                                # download_filename_new = f"Пересдачи_новые_{current_date}.xlsx"
                                # st.download_button(
                                #     label="Скачать только новые записи (XLSX)",
                                #     data=output_new.getvalue(),
                                #     file_name=download_filename_new,
                                #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                #     key="download_new"
                                # )
                            
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
        # --- ЗАГРУЗКА peresdachi С ПОМОЩЬЮ НОВОЙ ФУНКЦИИ ---
        existing_peresdachi = fetch_all('peresdachi')
        if existing_peresdachi.empty:
            st.info("Таблица peresdachi пуста или не создана")
        else:
            st.metric("Записей в таблице peresdachi", len(existing_peresdachi))
            st.dataframe(existing_peresdachi.head(10), use_container_width=True)
