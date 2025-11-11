"""
Модуль 6: Обновление списка студентов
UPSERT в таблицу students
"""

import streamlit as st
import pandas as pd
import time
from io import StringIO
from utils import icon, apply_custom_css, get_supabase_client

# Применяем кастомные стили
apply_custom_css()

# Заголовок страницы
st.markdown(
    f'<h1>{icon("users", 32)} Обновление списка студентов</h1>',
    unsafe_allow_html=True
)

st.markdown("""
Загрузка и обновление списка студентов в базе данных Supabase.

**Возможности:**
- Загрузка списка студентов из Excel или CSV файла
- Автоматическое удаление дубликатов по email
- UPSERT - обновление существующих и добавление новых записей
- Пакетная обработка с повторными попытками при ошибках

**Требуемые колонки в файле:**
- ФИО (или Учащийся)
- Адрес электронной почты (или Корпоративная почта, Email)
- Филиал (кампус)
- Факультет
- Образовательная программа
- Группа
- Курс
""")

def upload_students_to_supabase(supabase, student_data):
    """Загрузка данных студентов в таблицу students с использованием оптимизированного UPSERT"""
    try:
        st.info("👥 Загрузка данных студентов (UPSERT)...")
        records_for_upsert = []
        processed_emails = set()
        
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
            st.info("Нет записей для обработки")
            return True
        
        st.info(f"Подготовлено {len(records_for_upsert)} записей для UPSERT")
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
                st.success(f"Батч {batch_num}/{total_batches}: обработано {len(batch)} записей")
            except Exception as e:
                error_str = str(e)
                if any(pat in error_str.lower() for pat in ["connection", "timeout", "ssl", "eof"]):
                    st.warning(f"Сетевая ошибка в батче {batch_num}, повтор...")
                    time.sleep(2)
                    try:
                        result = supabase.table('students').upsert(batch, on_conflict='корпоративная_почта').execute()
                        total_processed += len(batch)
                        st.success(f"Батч {batch_num} (после повтора)")
                    except Exception as retry_error:
                        st.error(f"Батч {batch_num} не удался после повтора: {retry_error}")
                        return False
                else:
                    st.error(f"Ошибка в батче {batch_num}: {e}")
                    return False
        
        st.success(f"UPSERT завершён! Обработано {total_processed} записей")
        return True
    except Exception as e:
        st.error(f"Критическая ошибка UPSERT студентов: {e}")
        return False

def load_student_list_file(uploaded_file) -> pd.DataFrame:
    """Загрузка списка студентов из файла Excel или CSV"""
    try:
        file_name = uploaded_file.name.lower()
        if file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        elif file_name.endswith('.csv'):
            content = uploaded_file.getvalue()
            try:
                df = pd.read_csv(StringIO(content.decode('utf-16')), sep='\t')
            except (UnicodeDecodeError, pd.errors.ParserError):
                try:
                    df = pd.read_csv(StringIO(content.decode('utf-8')))
                except UnicodeDecodeError:
                    df = pd.read_csv(StringIO(content.decode('cp1251')))
        else:
            st.error("Неподдерживаемый формат файла")
            return pd.DataFrame()

        required_columns = {
            'ФИО': ['фио', 'фio', 'имя', 'name'],
            'Корпоративная почта': ['адрес электронной почты', 'корпоративная почта', 'email', 'почта', 'e-mail'],
            'Филиал (кампус)': ['филиал', 'кампус', 'campus'],
            'Факультет': ['факультет', 'faculty'],
            'Образовательная программа': ['образовательная программа', 'программа', 'educational program'],
            'Версия образовательной программы': ['версия образовательной программы', 'версия программы', 'program version', 'version'],
            'Группа': ['группа', 'group'],
            'Курс': ['курс', 'course'],
            'Уровень образования': ['уровень образования', 'уровень', 'level', 'образование']
        }

        found_columns = {}
        df_columns_lower = [str(col).lower().strip() for col in df.columns]
        for target_col, possible_names in required_columns.items():
            for col_idx, col_name in enumerate(df_columns_lower):
                if any(possible_name in col_name for possible_name in possible_names):
                    found_columns[target_col] = df.columns[col_idx]
                    break

        result_df = pd.DataFrame()
        for target_col, source_col in found_columns.items():
            if source_col in df.columns:
                result_df[target_col] = df[source_col]

        if 'Данные о пользователе' in df.columns:
            user_data = df['Данные о пользователе'].astype(str)
            parsed_data = user_data.str.split(';', expand=True)
            if len(parsed_data.columns) >= 4:
                result_df['Факультет'] = parsed_data[0]
                result_df['Образовательная программа'] = parsed_data[1] 
                result_df['Курс'] = parsed_data[2]
                result_df['Группа'] = parsed_data[3]

        for required_col in required_columns.keys():
            if required_col not in result_df.columns:
                if required_col == 'ФИО':
                    result_df[required_col] = None
                else:
                    result_df[required_col] = ''

        if 'Корпоративная почта' in result_df.columns:
            result_df = result_df[result_df['Корпоративная почта'].astype(str).str.contains('@edu.hse.ru', na=False)]
            result_df['Корпоративная почта'] = pd.Series(result_df['Корпоративная почта']).astype(str).str.lower().str.strip()
        return result_df
    except Exception as e:
        st.error(f"Ошибка загрузки списка студентов: {e}")
        return pd.DataFrame()

def load_students_from_supabase() -> pd.DataFrame:
    """Загрузка списка студентов из Supabase"""
    try:
        supabase = get_supabase_client()
        
        all_data = []
        page_size = 1000
        offset = 0
        
        while True:
            response = supabase.table('students').select('*').range(offset, offset + page_size - 1).execute()
            
            if response.data:
                all_data.extend(response.data)
                if len(response.data) < page_size:
                    break
                offset += page_size
            else:
                break
        
        if all_data:
            df = pd.DataFrame(all_data)
            
            column_mapping = {
                'корпоративная_почта': 'Адрес электронной почты',
                'фио': 'ФИО',
                'филиал_кампус': 'Филиал (кампус)',
                'факультет': 'Факультет',
                'образовательная_программа': 'Образовательная программа',
                'версия_образовательной_программы': 'Версия образовательной программы',
                'группа': 'Группа',
                'курс': 'Курс',
                'уровень_образования': 'Уровень образования'
            }
            
            existing_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
            df = df.rename(columns=existing_columns)
            
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.warning(f"Не удалось загрузить данные: {str(e)}")
        return pd.DataFrame()

# Проверка пароля
st.markdown("---")
st.subheader("Авторизация")

# Используем session_state для хранения статуса авторизации
if 'students_authorized' not in st.session_state:
    st.session_state['students_authorized'] = False

if not st.session_state['students_authorized']:
    password_input = st.text_input(
        "Введите пароль для доступа к модулю",
        type="password",
        key="students_password_input",
        help="Введите пароль для обновления списка студентов"
    )
    
    if st.button("Войти", type="primary", key="students_login_btn"):
        # Получаем пароль из secrets
        correct_password = st.secrets.get("STUDENTS_UPDATE_PASSWORD", "default_password")
        if password_input == correct_password:
            st.session_state['students_authorized'] = True
            st.success("Доступ разрешен!")
            st.rerun()
        else:
            st.error("Неверный пароль")
    
    st.info("Для доступа к функции обновления списка студентов необходимо ввести пароль.")
    st.stop()

# Если авторизован, показываем основной функционал
st.success("Вы авторизованы")

# Проверка подключения
try:
    supabase = get_supabase_client()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения к Supabase: {str(e)}")
    st.stop()

st.markdown("---")

# Загрузка файла
st.subheader("Загрузка файла со студентами")

students_file = st.file_uploader(
    "Выберите файл со списком студентов (Excel или CSV)",
    type=['xlsx', 'xls', 'csv'],
    key="students_upload_file",
    help="Файл должен содержать колонки: ФИО, Адрес электронной почты, Филиал, Факультет, Образовательная программа, Группа, Курс"
)

if students_file:
    try:
        with st.spinner("Загрузка файла..."):
            students_df = load_student_list_file(students_file)
        
        if students_df.empty:
            st.error("Не удалось загрузить данные из файла. Проверьте формат файла.")
            st.stop()
        
        st.success(f"Файл успешно загружен!")
        
        # Статистика перед обработкой
        st.subheader("Предварительная информация")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Записей в файле", len(students_df))
        with col2:
            unique_emails = students_df['Корпоративная почта'].nunique()
            st.metric("Уникальных email", unique_emails)
        
        # Предпросмотр
        with st.expander("Предпросмотр данных"):
            st.dataframe(students_df.head(20), use_container_width=True)
        
        # Кнопка обработки
        if st.button("Обновить список студентов в Supabase", type="primary", key="update_students_btn"):
            with st.spinner("Обновление базы данных..."):
                try:
                    if upload_students_to_supabase(supabase, students_df):
                        st.success("Список студентов обновлён!")
                        st.balloons()
                    else:
                        st.error("Не удалось обновить список студентов")
                    
                except Exception as e:
                    st.error(f"Ошибка при обновлении: {str(e)}")
                    st.exception(e)
    
    except Exception as e:
        st.error(f"Ошибка при загрузке файла: {str(e)}")
        st.exception(e)

else:
    st.info("Загрузите файл со списком студентов")
    
    # Добавляем возможность скачивания актуального списка из Supabase с фильтрацией
    st.markdown("---")
    st.markdown("### Скачать актуальный список студентов")

    # Загружаем данные для фильтрации
    try:
        all_students = load_students_from_supabase()
        if not all_students.empty:
            # Создаем фильтры
            st.subheader("Фильтры для скачивания")
            
            # Получаем уникальные значения для каждого фильтра
            campus_options = ['Все'] + sorted(all_students['Филиал (кампус)'].dropna().unique().tolist()) if 'Филиал (кампус)' in all_students.columns else ['Все']
            faculty_options = ['Все'] + sorted(all_students['Факультет'].dropna().unique().tolist()) if 'Факультет' in all_students.columns else ['Все']
            program_version_options = ['Все'] + sorted(all_students['Версия образовательной программы'].dropna().unique().tolist()) if 'Версия образовательной программы' in all_students.columns else ['Все']
            course_options = ['Все'] + sorted(all_students['Курс'].dropna().unique().tolist()) if 'Курс' in all_students.columns else ['Все']
            level_options = ['Все'] + sorted(all_students['Уровень образования'].dropna().unique().tolist()) if 'Уровень образования' in all_students.columns else ['Все']
            
            # Создаем колонки для фильтров (делаем 3 колонки чтобы не было слишком узко)
            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)
            
            with col1:
                selected_campus = st.selectbox("Филиал (кампус)", campus_options, key="filter_campus")
                if st.button("🔄", key="reset_campus", help="Сбросить фильтр"):
                    st.session_state["filter_campus"] = 'Все'
                    st.rerun()
            
            with col2:
                selected_faculty = st.selectbox("Факультет", faculty_options, key="filter_faculty")
                if st.button("🔄", key="reset_faculty", help="Сбросить фильтр"):
                    st.session_state["filter_faculty"] = 'Все'
                    st.rerun()
            
            with col3:
                selected_program_version = st.selectbox("Версия образовательной программы", program_version_options, key="filter_program_version")
                if st.button("🔄", key="reset_program_version", help="Сбросить фильтр"):
                    st.session_state["filter_program_version"] = 'Все'
                    st.rerun()
            
            with col4:
                selected_course = st.selectbox("Курс", course_options, key="filter_course")
                if st.button("🔄", key="reset_course", help="Сбросить фильтр"):
                    st.session_state["filter_course"] = 'Все'
                    st.rerun()
            
            with col5:
                selected_level = st.selectbox("Уровень образования", level_options, key="filter_level")
                if st.button("🔄", key="reset_level", help="Сбросить фильтр"):
                    st.session_state["filter_level"] = 'Все'
                    st.rerun()
            
            # Пустая колонка для симметрии
            with col6:
                st.write("")
            
            # Применяем фильтры
            filtered_students = all_students.copy()
            if selected_campus != 'Все' and 'Филиал (кампус)' in filtered_students.columns:
                filtered_students = filtered_students[filtered_students['Филиал (кампус)'] == selected_campus]
            if selected_faculty != 'Все' and 'Факультет' in filtered_students.columns:
                filtered_students = filtered_students[filtered_students['Факультет'] == selected_faculty]
            if selected_program_version != 'Все' and 'Версия образовательной программы' in filtered_students.columns:
                filtered_students = filtered_students[filtered_students['Версия образовательной программы'] == selected_program_version]
            if selected_course != 'Все' and 'Курс' in filtered_students.columns:
                filtered_students = filtered_students[filtered_students['Курс'] == selected_course]
            if selected_level != 'Все' and 'Уровень образования' in filtered_students.columns:
                filtered_students = filtered_students[filtered_students['Уровень образования'] == selected_level]
            
            st.info(f"После фильтрации: {len(filtered_students)} записей из {len(all_students)}")
            
            # Кнопки скачивания
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("Получить отфильтрованный список (CSV)", key="download_filtered_csv_btn"):
                    with st.spinner("Подготовка CSV файла..."):
                        try:
                            if filtered_students.empty:
                                st.info("Нет данных для скачивания по выбранным фильтрам")
                            else:
                                csv_data = filtered_students.to_csv(index=False, sep=';', encoding='utf-8-sig')
                                
                                st.download_button(
                                    label="📥 Скачать список студентов (CSV)",
                                    data=csv_data,
                                    file_name=f"students_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv",
                                    key="download_filtered_csv"
                                )
                                
                                st.success(f"CSV файл готов! {len(filtered_students)} записей")
                                
                        except Exception as e:
                            st.error(f"Ошибка при подготовке CSV: {str(e)}")
                            st.exception(e)

            with col_btn2:
                if st.button("Получить отфильтрованный список (Excel)", key="download_filtered_xlsx_btn"):
                    with st.spinner("Подготовка Excel-файла..."):
                        try:
                            if filtered_students.empty:
                                st.info("Нет данных для скачивания по выбранным фильтрам")
                            else:
                                from io import BytesIO
                                buffer = BytesIO()
                                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                    filtered_students.to_excel(writer, index=False, sheet_name='Students')
                                
                                buffer.seek(0)
                                
                                st.download_button(
                                    label="📥 Скачать список студентов (Excel)",
                                    data=buffer,
                                    file_name=f"students_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key="download_filtered_xlsx"
                                )
                                
                                st.success(f"Excel-файл готов! {len(filtered_students)} записей")
                                
                        except Exception as e:
                            st.error(f"Ошибка при подготовке Excel-файла: {str(e)}")
                            st.exception(e)
            
            # Показываем предпросмотр отфильтрованных данных
            with st.expander("Предпросмотр отфильтрованных данных"):
                st.dataframe(filtered_students.head(20), use_container_width=True)
        
        else:
            st.info("В базе данных нет студентов для скачивания")
            # Кнопки скачивания для пустого списка
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.download_button(
                    label="📥 Скачать пустой список (CSV)",
                    data="",
                    file_name=f"students_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    disabled=True
                )
            with col_btn2:
                st.download_button(
                    label="📥 Скачать пустой список (Excel)",
                    data="",
                    file_name=f"students_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    disabled=True
                )

    except Exception as e:
        st.error(f"Ошибка при загрузке данных для фильтрации: {str(e)}")
        st.exception(e)
    
    st.markdown("---")
    st.markdown("### Инструкция")
    st.markdown("""
    **Как использовать:**
    
    1. **Подготовьте файл** с данными студентов (Excel или CSV)
    2. **Убедитесь**, что файл содержит необходимые колонки
    3. **Загрузите файл** через форму выше
    4. **Проверьте предпросмотр** данных
    5. **Нажмите кнопку "Обновить"**
    
    **Важно:**
    - Дубликаты по email автоматически удаляются
    - Используется UPSERT - существующие записи обновляются
    - Email нормализуются для корректного сравнения
    - Записи без валидного email пропускаются
    """)
    
    # Проверка текущего состояния базы
    with st.expander("Текущее состояние базы данных"):
        try:
            current_students = load_students_from_supabase()
            if current_students.empty:
                st.info("Таблица students пуста или не создана")
            else:
                st.success(f"В базе данных: {len(current_students)} студентов")
                st.dataframe(current_students.head(10), use_container_width=True)
        except Exception as e:
            st.warning(f"Не удалось загрузить данные: {str(e)}")
