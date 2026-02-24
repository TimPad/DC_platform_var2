"""
Модуль 4: Обработка пересдач внешней оценки
Supabase интеграция для пересдач
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
from typing import Tuple
from utils import icon, apply_custom_css, get_supabase_client, load_lottie_url
from constants import LOTTIE_SUCCESS_URL, LOTTIE_EMPTY_URL
from streamlit_lottie import st_lottie

# Применяем кастомные стили
apply_custom_css()

# Заголовок страницы
st.markdown(
    f'<h1>{icon("file-edit", 32)} Обработка пересдач внешней оценки</h1>',
    unsafe_allow_html=True
)

st.markdown("""
📊 **1. Отображение результатов**

Все обновлённые оценки автоматически отражаются на дэшборде:
🔗 [Yandex DataLens — Внешнее измерение](https://datalens.yandex/n77d62nm8lus8)

**2. Процесс сдачи для студентов**

**Студенты 4 курса
Внешнее измерение состоит из трёх этапов.
Сдача происходит через курс:
🔗 [edu.hse.ru/course/view.php?id=253000](https://edu.hse.ru/course/view.php?id=253000)

**Студенты 3 курса
Сдача проходит через итоговый проект.
Курс для загрузки:
🔗 [edu.hse.ru/course/view.php?id=273033](https://edu.hse.ru/course/view.php?id=273033)

⚠️ **Если студент 3 курса утверждает, что сдал проект, но оценки нет:**
Скорее всего, возникла техническая ошибка при обработке.
**Решение:** попросите студента перезагрузить проект через тот же курс.

🚀 Студенты продвинутого уровня
Вместо проекта используется перезачёт оценки за курсовую работу со 2 курса.
Дополнительная загрузка не требуется — оценка импортируется из архива.

**3. Обработка оценок сотрудником**

**Шаг 1: Экспорт данных из SmartLMS**
Перейдите в соответствующий курс сдачи:
- 4 курс: `id=253000`
- 3 курс: `id=273033`
Откройте раздел **Оценки → Экспорт**.
Выберите формат:
**Текстовый документ (CSV)** или
**Excel (.xlsx)**
Скачайте файл на устройство.

**Шаг 2: Загрузка в систему обработки**
Перейдите в меню обработки оценок.
Выберите тип данных:
**Тест** — для этапов 4 курса
**Проект** — для итогового проекта 3 курса
Загрузите экспортированный файл.
Запустите обработку.

**Шаг 3: Выгрузка результатов**
После успешной обработки доступны два варианта выгрузки:
**Только новые записи** — для инкрементального обновления
**Полная ведомость** — для сверки и архивации

**Шаг 4: Дополнение данными из SmartReg**
Откройте файл с результатами обработки.
Для каждой записи добавьте:
- ID дисциплины (из системы SmartReg)
- Период реализации (например, 2024/2025 2 модуль)

**Шаг 5: Передача на финальную загрузку**
📬 Отправьте подготовленный файл ответственному:
**Голубев Александр**
💡 *Рекомендуется указывать в тексте письма: загрузка первичной попытки*
""")

from logic.external_assessment import (
    load_existing_peresdachi,
    load_student_io_from_supabase,
    save_to_supabase,
    get_new_records_from_dataframe,
    process_external_assessment,
    process_project_assessment,
    update_final_grades
)
from logic.student_management import load_students_from_supabase

# Проверка подключения к Supabase
try:
    supabase = get_supabase_client()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения к Supabase: {str(e)}")
    st.stop()

st.markdown("---")

# Используем табы для разделения функционала
tab_tests, tab_projects = st.tabs(["Пересдачи (Тесты)", "Внешнее измерение (Проекты)"])

# --- ВКЛАДКА 1: ПЕРЕСДАЧИ (ТЕСТЫ) ---
with tab_tests:
    st.subheader("Загрузка файла с оценками (Тесты)")
    grades_file = st.file_uploader(
        "Выберите файл с оценками (external_assessment)",
        type=['xlsx', 'xls', 'csv'],
        key="external_grades_file",
        help="Файл должен содержать колонки: Адрес электронной почты, Тест:Входное/Промежуточное/Итоговое тестирование (Значение)"
    )

    if grades_file:
        try:
            with st.spinner("Загрузка файла с оценками..."):
                if grades_file.name.endswith('.csv'):
                    grades_df = pd.read_csv(grades_file)
                else:
                    grades_df = pd.read_excel(grades_file)

            st.success("Файл с оценками успешно загружен!")

            # Загрузка студентов
            with st.spinner("Загрузка списка студентов из Supabase..."):
                students_df = load_students_from_supabase(filters={'курс': ['Курс 2', 'Курс 3', 'Курс 4']})

            if students_df.empty:
                st.error("Список студентов пуст. Загрузите данные в таблицу `students` в Supabase.")
            else:
                st.success(f"Загружено {len(students_df)} студентов из Supabase")

            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Записей с оценками", len(grades_df))
            with col2: st.metric("Студентов в базе", len(students_df))
            with col3: st.metric("Колонок в оценках", len(grades_df.columns))

            col_preview1, col_preview2 = st.columns(2)
            with col_preview1:
                with st.expander("Предпросмотр файла с оценками"):
                    st.dataframe(grades_df.head(), use_container_width=True)

            with col_preview2:
                with st.expander("Предпросмотр списка студентов"):
                    st.dataframe(students_df.head(10), use_container_width=True)

            # Кнопка запуска обработки
            if st.button("Обработать данные (Тесты)", type="primary", key="process_btn_tests"):
                with st.spinner("Обработка пересдач..."):
                    try:
                        result_df, logs = process_external_assessment(grades_df, students_df)
                        for log_msg in logs:
                            st.info(log_msg)

                        if result_df.empty:
                            st.error("Не удалось обработать данные. Проверьте структуру файла.")
                        else:
                            # 1. Сохраняем результат в session_state
                            st.session_state['result_df_tests'] = result_df
                            
                            # 2. Логика обработки дубликатов и сохранения
                            # Определяем новые записи
                            display_new_records_uncleaned = get_new_records_from_dataframe(result_df)
                            new_count_uncleaned = len(display_new_records_uncleaned)
                            total_count_uncleaned = len(result_df)

                            # Проверка и удаление дубликатов
                            conflict_cols = ["Адрес электронной почты", "Наименование дисциплины"]
                            result_df_cleaned = result_df.drop_duplicates(subset=conflict_cols, keep='first')
                            duplicates_removed_result = total_count_uncleaned - len(result_df_cleaned)
                            
                            if duplicates_removed_result > 0:
                                result_df = result_df_cleaned
                                display_new_records = get_new_records_from_dataframe(result_df)
                                new_count = len(display_new_records)
                                total_count = len(result_df)
                            else:
                                display_new_records = display_new_records_uncleaned
                                new_count = new_count_uncleaned
                                total_count = total_count_uncleaned

                            display_new_records = display_new_records.drop_duplicates(subset=conflict_cols, keep='first')
                            
                            # Сохраняем обработанное состояние для отображения
                            st.session_state['tests_processed_state'] = {
                                'result_df': result_df,
                                'display_new_records': display_new_records,
                                'total_count': total_count,
                                'new_count': new_count,
                                'duplicates_removed': duplicates_removed_result,
                                'processed_at': datetime.now(),
                                'save_msg': ''
                            }

                            # Автоматическое сохранение при обработке
                            save_success, save_msg = save_to_supabase(display_new_records)
                            st.session_state['tests_processed_state']['save_success'] = save_success
                            st.session_state['tests_processed_state']['save_msg'] = save_msg
                            
                    except Exception as e:
                        st.error(f"Ошибка: {str(e)}")
                        # st.exception(e)

            # ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ ИЗ SESSION STATE
            if 'tests_processed_state' in st.session_state:
                state = st.session_state['tests_processed_state']
                
                st.success("Обработка успешно завершена!")
                
                if state['duplicates_removed'] > 0:
                     st.warning(f"Удалено {state['duplicates_removed']} дубликатов.")

                if state['save_success']:
                    st.success(f"{state.get('save_msg', 'Сохранено новых записей')}: {state['new_count']}.") 
                    lottie_success = load_lottie_url(LOTTIE_SUCCESS_URL)
                    if lottie_success:
                        st_lottie(lottie_success, height=150, key="success_anim_tests", loop=False) # LOOP FALSE
                else:
                    st.error(f"Ошибка при сохранении данных в Supabase: {state.get('save_msg', '')}")

                # Статистика
                st.subheader("Результаты")
                col1, col2, col3 = st.columns(3)
                with col1: st.metric("Всего", state['total_count'])
                with col2: st.metric("Новых", state['new_count'])
                with col3: st.metric("Старых", state['total_count'] - state['new_count'])

                # Табы для скачивания
                subtab1, subtab2 = st.tabs(["Все данные", "Только новые"])
                current_date = datetime.now().strftime('%d-%m-%Y')
                
                with subtab1:
                    st.dataframe(state['result_df'], use_container_width=True)
                    output_all = io.BytesIO()
                    with pd.ExcelWriter(output_all, engine='openpyxl') as writer:
                        state['result_df'].to_excel(writer, index=False)
                    output_all.seek(0)
                    st.download_button("Скачать все (XLSX)", output_all, f"Tests_All_{current_date}.xlsx", key="dl_all_tests")

                with subtab2:
                    if state['display_new_records'].empty:
                        st.info("Новых нет")
                    else:
                        st.dataframe(state['display_new_records'], use_container_width=True)
                        output_new = io.BytesIO()
                        with pd.ExcelWriter(output_new, engine='openpyxl') as writer:
                            state['display_new_records'].to_excel(writer, index=False)
                        output_new.seek(0)
                        st.download_button("Скачать новые (XLSX)", output_new, f"Tests_New_{current_date}.xlsx", key="dl_new_tests")

        except Exception as e:
            st.error(f"Ошибка файла: {str(e)}")
    else:
        st.info("Загрузите файл XLSX для обработки тестов")

# --- ВКЛАДКА 2: ВНЕШНЕЕ ИЗМЕРЕНИЕ (ПРОЕКТЫ) ---
with tab_projects:
    st.subheader("Загрузка файла с оценками (Проекты)")
    project_file = st.file_uploader(
        "Выберите файл с оценками (CSV или Excel)",
        type=['csv', 'xlsx', 'xls'],
        key="project_grades_file",
        help="Файл (CSV или Excel) с колонками 'Задание:...' и 'Адрес электронной почты'"
    )

    if project_file:
        try:
            with st.spinner("Загрузка файла..."):
                if project_file.name.endswith('.csv'):
                    project_grades_df = pd.read_csv(project_file)
                else:
                    project_grades_df = pd.read_excel(project_file)
            
            st.success("Файл успешно загружен!")
            
            with st.spinner("Загрузка студентов..."):
                students_df = load_students_from_supabase(filters={'курс': ['Курс 2', 'Курс 3', 'Курс 4']})
            
            if students_df.empty:
                st.error("Список студентов пуст.")
            else:
                col1, col2 = st.columns(2)
                with col1: st.metric("Строк в файле", len(project_grades_df))
                with col2: st.metric("Студентов в базе", len(students_df))

                with st.expander("Предпросмотр CSV"):
                    st.dataframe(project_grades_df.head(), use_container_width=True)

                if st.button("Обработать данные (Проекты)", type="primary", key="process_btn_projects"):
                     with st.spinner("Обработка проектов..."):
                        try:
                            result_df, logs = process_project_assessment(project_grades_df, students_df)
                            for log_msg in logs:
                                st.info(log_msg)
                            
                            if result_df.empty:
                                st.error("Результат пуст. Проверьте соответствие колонок (email, задания).")
                            else:
                                # 1. Сохраняем в session_state
                                st.session_state['result_df_projects'] = result_df
                                
                                # 2. Обработка дублей
                                display_new_records_uncleaned = get_new_records_from_dataframe(result_df)
                                new_count_uncleaned = len(display_new_records_uncleaned)
                                total_count_uncleaned = len(result_df)

                                conflict_cols = ["Адрес электронной почты", "Наименование дисциплины"]
                                result_df_cleaned = result_df.drop_duplicates(subset=conflict_cols, keep='first')
                                duplicates_removed = total_count_uncleaned - len(result_df_cleaned)
                                
                                if duplicates_removed > 0:
                                    result_df = result_df_cleaned
                                    display_new_records = get_new_records_from_dataframe(result_df)
                                else:
                                    display_new_records = display_new_records_uncleaned
                                
                                display_new_records = display_new_records.drop_duplicates(subset=conflict_cols, keep='first')
                                new_count = len(display_new_records)
                                total_count = len(result_df)

                                # Сохранение состояния
                                st.session_state['projects_processed_state'] = {
                                    'result_df': result_df,
                                    'display_new_records': display_new_records,
                                    'total_count': total_count,
                                    'new_count': new_count,
                                    'duplicates_removed': duplicates_removed,
                                    'processed_at': datetime.now(),
                                    'save_msg': ''
                                }

                                save_success, save_msg = save_to_supabase(display_new_records)
                                st.session_state['projects_processed_state']['save_success'] = save_success
                                st.session_state['projects_processed_state']['save_msg'] = save_msg
                                
                                # Обновляем final_grades для ВСЕХ обработанных записей (результат шага 1)
                                # так как даже если запись не новая для peresdachi, оценка могла измениться
                                if save_success:
                                    st.info("Обновление сводной таблицы final_grades...")
                                    fg_success, fg_updated, fg_msg = update_final_grades(result_df)
                                    if fg_success:
                                        st.success(f"Таблица final_grades успешно обновлена. Обработано записей: {fg_updated}")
                                    else:
                                        st.warning(f"Не удалось обновить/синхронизировать final_grades: {fg_msg}")

                        except Exception as e:
                            st.error(f"Ошибка: {str(e)}")
                            st.exception(e)

                # ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ (ПРОЕКТЫ)
                if 'projects_processed_state' in st.session_state:
                    state = st.session_state['projects_processed_state']
                    
                    st.success("Обработка завершена!")
                    
                    if state['duplicates_removed'] > 0:
                         st.warning(f"Удалено {state['duplicates_removed']} дубликатов.")

                    if state['save_success']:
                        st.success(f"{state.get('save_msg', 'Сохранено новых записей')}: {state['new_count']}")
                        lottie_success = load_lottie_url(LOTTIE_SUCCESS_URL)
                        if lottie_success:
                            st_lottie(lottie_success, height=150, key="success_anim_projects", loop=False) # LOOP FALSE
                    else:
                        st.error(f"Ошибка сохранения: {state.get('save_msg', '')}")

                    # Статистика и скачивание
                    st.subheader("Результаты")
                    col1, col2 = st.columns(2)
                    with col1: st.metric("Всего", state['total_count'])
                    with col2: st.metric("Новых", state['new_count'])

                    subtab1, subtab2 = st.tabs(["Все данные", "Только новые"])
                    current_date = datetime.now().strftime('%d-%m-%Y')

                    with subtab1:
                        st.dataframe(state['result_df'], use_container_width=True)
                        output_all = io.BytesIO()
                        with pd.ExcelWriter(output_all, engine='openpyxl') as writer:
                            state['result_df'].to_excel(writer, index=False)
                        output_all.seek(0)
                        st.download_button("Скачать все (XLSX)", output_all, f"Projects_All_{current_date}.xlsx", key="dl_all_projects")
                    
                    with subtab2:
                        if state['display_new_records'].empty:
                            st.info("Новых записей нет")
                        else:
                            st.dataframe(state['display_new_records'], use_container_width=True)
                            output_new = io.BytesIO()
                            with pd.ExcelWriter(output_new, engine='openpyxl') as writer:
                                state['display_new_records'].to_excel(writer, index=False)
                            output_new.seek(0)
                            st.download_button("Скачать новые (XLSX)", output_new, f"Projects_New_{current_date}.xlsx", key="dl_new_projects")

        except Exception as e:
            st.error(f"Ошибка чтения файла: {str(e)}")
    else:
        st.info("Загрузите CSV файл для обработки проектов")


# Общая инфо панель внизу (вне табов)
with st.expander("Текущее состояние базы данных (peresdachi)"):
    existing_peresdachi = load_existing_peresdachi()
    if existing_peresdachi.empty:
        st.info("База пуста")
    else:
        st.metric("Всего записей", len(existing_peresdachi))
        st.dataframe(existing_peresdachi.head(10), use_container_width=True)
