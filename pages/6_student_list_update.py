"""
Модуль 6: Обновление списка студентов
UPSERT в таблицу students
"""

import streamlit as st
import pandas as pd
from utils import icon, get_supabase_client
from logic.student_management import (
    load_student_list_file, 
    upload_students_to_supabase, 
    load_students_from_supabase
)

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
            try:
                students_df = load_student_list_file(students_file)
            except ValueError as ve:
                st.error(str(ve))
                st.stop()
        
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
                    success, msg = upload_students_to_supabase(supabase, students_df)
                    if success:
                        st.success(msg)
                        st.balloons()
                    else:
                        st.error(msg)
                    
                except Exception as e:
                    st.error(f"Ошибка при обновлении: {str(e)}")
    
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
        all_students = load_students_from_supabase() # Без фильтров = загрузить ВСЕХ
        if not all_students.empty:
            # Создаем фильтры
            st.subheader("Фильтры для скачивания")
            
            # Получаем уникальные значения для каждого фильтра
            campus_options = ['Все'] + sorted(all_students['Филиал (кампус)'].dropna().unique().tolist()) if 'Филиал (кампус)' in all_students.columns else ['Все']
            faculty_options = ['Все'] + sorted(all_students['Факультет'].dropna().unique().tolist()) if 'Факультет' in all_students.columns else ['Все']
            program_version_options = ['Все'] + sorted(all_students['Версия образовательной программы'].dropna().unique().tolist()) if 'Версия образовательной программы' in all_students.columns else ['Все']
            course_options = ['Все'] + sorted(all_students['Курс'].dropna().unique().tolist()) if 'Курс' in all_students.columns else ['Все']
            level_options = ['Все'] + sorted(all_students['Уровень образования'].dropna().unique().tolist()) if 'Уровень образования' in all_students.columns else ['Все']
            
            # Создаем колонки для фильтров
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
