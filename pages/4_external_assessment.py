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

from logic.external_assessment import (
    load_students_from_supabase,
    load_existing_peresdachi,
    load_student_io_from_supabase,
    save_to_supabase,
    get_new_records_from_dataframe,
    process_external_assessment
)

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
grades_file = st.file_uploader(
    "Выберите файл с оценками (external_assessment)",
    type=['xlsx', 'xls'],
    key="external_grades_file",
    help="Файл должен содержать колонки: Адрес электронной почты, Тест:Входное/Промежуточное/Итоговое тестирование (Значение)"
)

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

        if st.button("Обработать данные", type="primary", key="process_btn"):
            with st.spinner("Обработка пересдач..."):
                try:
                    result_df = process_external_assessment(grades_df, students_df)

                    if result_df.empty:
                        st.error("Не удалось обработать данные. Проверьте структуру файла.")
                    else:
                        st.success("Обработка успешно завершена!")

                        # Определяем новые записи ДО удаления дубликатов (для отображения до очистки)
                        # Но используем их только после очистки
                        display_new_records_uncleaned = get_new_records_from_dataframe(result_df)
                        new_count_uncleaned = len(display_new_records_uncleaned)
                        total_count_uncleaned = len(result_df)

                        # Проверка и удаление дубликатов В result_df ПЕРЕД сохранением
                        with st.spinner("Проверка и удаление дубликатов в данных для сохранения..."):
                            conflict_cols = ["Адрес электронной почты", "Наименование дисциплины"]
                            initial_count_result = len(result_df)
                            # Удаляем дубликаты в result_df по ключевым полям
                            result_df_cleaned = result_df.drop_duplicates(subset=conflict_cols, keep='first')
                            final_count_result = len(result_df_cleaned)
                            duplicates_removed_result = initial_count_result - final_count_result
                            if duplicates_removed_result > 0:
                                st.warning(f"Найдено и удалено {duplicates_removed_result} дубликатов в наборе данных для сохранения (result_df).")
                                # Обновляем result_df, с которым будем работать дальше
                                result_df = result_df_cleaned
                                # Также пересчитываем display_new_records на основе очищенного result_df
                                display_new_records = get_new_records_from_dataframe(result_df)
                                new_count = len(display_new_records)
                                total_count = len(result_df) # Общее количество тоже обновляется, если были дубликаты
                            else:
                                st.info("Дубликатов в наборе данных для сохранения (result_df) не обнаружено.")
                                # Если дубликатов не было, используем изначальные значения
                                display_new_records = display_new_records_uncleaned
                                new_count = new_count_uncleaned
                                total_count = total_count_uncleaned

                            # Проверим, есть ли дубликаты в display_new_records (хотя маловероятно, если get_new_records_from_dataframe корректен)
                            # Используем уже potentially обновлённый display_new_records
                            initial_count_new = len(display_new_records)
                            display_new_records_cleaned = display_new_records.drop_duplicates(subset=conflict_cols, keep='first')
                            final_count_new = len(display_new_records_cleaned)
                            duplicates_removed_new = initial_count_new - final_count_new
                            if duplicates_removed_new > 0:
                                st.warning(f"Найдено и удалено {duplicates_removed_new} дубликатов в наборе 'новых' записей перед сохранением.")
                                display_new_records = display_new_records_cleaned
                                new_count = len(display_new_records) # Пересчитываем количество новых


                        # Сохранение в Supabase
                        with st.spinner("Сохранение в Supabase..."):
                            save_success = save_to_supabase(display_new_records)
                            if save_success:
                                st.success(f"Сохранено в Supabase: {new_count} новых записей из {total_count} (после удаления дубликатов из исходного набора).")
                                lottie_success = load_lottie_url(LOTTIE_SUCCESS_URL)
                                if lottie_success:
                                    st_lottie(lottie_success, height=150, key="success_anim")
                            else:
                                st.error("Ошибка при сохранении данных в Supabase")
                                st.stop()  # Прерываем, если не удалось сохранить

                        # Статистика (обновляется с учётом удаления дубликатов)
                        st.subheader("Результаты обработки (после удаления дубликатов)")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Всего обработано (без дублей)", total_count)
                        with col2:
                            st.metric("Новых записей (без дублей)", new_count)
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
            lottie_empty = load_lottie_url(LOTTIE_EMPTY_URL)
            if lottie_empty:
                st_lottie(lottie_empty, height=200, key="empty_anim")
        else:
            st.metric("Записей в таблице peresdachi", len(existing_peresdachi))
            st.dataframe(existing_peresdachi.head(10), use_container_width=True)
