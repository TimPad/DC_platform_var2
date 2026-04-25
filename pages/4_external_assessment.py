"""
Модуль 4: Обработка пересдач внешней оценки
Supabase интеграция для пересдач
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
from typing import Tuple
from utils import icon, get_supabase_client, load_lottie_url
from constants import LOTTIE_SUCCESS_URL, LOTTIE_EMPTY_URL
from streamlit_lottie import st_lottie

# Заголовок страницы
st.markdown(
    f'<h1>{icon("file-edit", 32)} Обработка пересдач внешней оценки</h1>',
    unsafe_allow_html=True
)

st.markdown("""
<style>
.instr-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
}
.instr-card {
    background: var(--apple-bg-secondary, #2a2a30);
    border: 1px solid var(--apple-divider, rgba(255,255,255,0.08));
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.instr-card-title {
    color: var(--apple-text-primary, #e0e0e6);
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-bottom: 1px solid var(--apple-divider, rgba(255,255,255,0.08));
    padding-bottom: 0.8rem;
}
.instr-card-title svg {
    color: var(--apple-accent, #5A9DF8);
}
.instr-section {
    margin-bottom: 1.2rem;
}
.instr-section:last-child {
    margin-bottom: 0;
}
.instr-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--apple-accent, #5A9DF8);
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.instr-text {
    font-size: 0.95rem;
    color: var(--apple-text-secondary, #a1a1aa);
    line-height: 1.5;
}
.instr-text strong {
    color: var(--apple-text-primary, #e0e0e6);
}
.instr-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    color: var(--apple-text-primary, #e0e0e6);
    text-decoration: none !important;
    background: rgba(255,255,255,0.05);
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    font-size: 0.9rem;
    margin-top: 0.5rem;
    transition: background 0.2s;
    border: 1px solid rgba(255,255,255,0.05);
}
.instr-link:hover {
    background: rgba(255,255,255,0.1);
}
.instr-alert {
    background: rgba(250, 204, 21, 0.1);
    border-left: 3px solid #facc15;
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    margin-top: 0.8rem;
    font-size: 0.9rem;
    color: var(--apple-text-primary, #e0e0e6);
}
.instr-alert strong {
    color: #fde047;
}
.instr-step {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}
.instr-step:last-child {
    margin-bottom: 0;
}
.instr-step-num {
    background: rgba(90, 157, 248, 0.15);
    color: var(--apple-accent, #5A9DF8);
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 600;
    flex-shrink: 0;
    margin-top: 2px;
}
.instr-step-content {
    flex: 1;
}
.instr-step-title {
    color: var(--apple-text-primary, #e0e0e6);
    font-weight: 600;
    margin-bottom: 0.2rem;
    font-size: 0.95rem;
}
kode {
    background: rgba(255,255,255,0.1);
    padding: 0.1rem 0.3rem;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.85em;
    color: #e0e0e6;
}
</style>
""", unsafe_allow_html=True)

col_info_1, col_info_2 = st.columns([1, 1])

with col_info_1:
    html_1 = '''
<div class="instr-card">
<div class="instr-card-title">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>
1. Данные и результаты
</div>
<div class="instr-text">
Все обновлённые оценки автоматически отражаются на дэшборде:
<br/>
<a href="https://datalens.yandex/n77d62nm8lus8" target="_blank" class="instr-link">
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
Yandex DataLens — Внешнее измерение
</a>
</div>
</div>
<div class="instr-card" style="margin-top: 1rem;">
<div class="instr-card-title">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
2. Инфо по студентам
</div>
<div class="instr-section">
<div class="instr-label">🎓 4 курс</div>
<div class="instr-text">
Внешнее измерение состоит из 3 этапов.<br/>
<a href="https://edu.hse.ru/grade/export/txt/index.php?id=253000" target="_blank" class="instr-link">Перейти к экспорту оценок курса id=253000 (самозапись)</a>
</div>
</div>
<div class="instr-section">
<div class="instr-label">🎓 3 курс</div>
<div class="instr-text">
Оценка формируется через итоговый проект.<br/>
<a href="https://edu.hse.ru/grade/export/txt/index.php?id=273033" target="_blank" class="instr-link">Перейти к экспорту оценок курса id=273033 (самозапись)</a>
<div class="instr-alert">
<strong>⚠️ Нет оценки за проект?</strong> Возможна была техническая ошибка. Попросите студента перезагрузить проект.
</div>
</div>
</div>
<div class="instr-section">
<div class="instr-label">🚀 Продвинутый уровень 3 курс</div>
<div class="instr-text">
Дополнительная загрузка <strong>не требуется</strong>.<br/>Идёт перезачёт оценки курсовой 2 курса.
</div>
</div>
</div>
'''
    st.markdown(html_1, unsafe_allow_html=True)

with col_info_2:
    html_2 = '''
<div class="instr-card" style="height: 100%;">
<div class="instr-card-title">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
3. Обработка оценок сотрудником
</div>
<div class="instr-step">
<div class="instr-step-num">1</div>
<div class="instr-step-content instr-text">
<div class="instr-step-title">Экспорт из SmartLMS</div>
Зайдите в курс (4к: <kode>253000</kode>, 3к: <kode>273033</kode>).<br/>
<strong>Оценки → Экспорт</strong>: 📄 CSV или 📊 Excel.
</div>
</div>
<div class="instr-step">
<div class="instr-step-num">2</div>
<div class="instr-step-content instr-text">
<div class="instr-step-title">Загрузка файлов</div>
🧪 <strong>Тест</strong> (4 курс) или 📁 <strong>Проект</strong> (3 курс).<br/>
Загрузите файл ниже и нажмите обработать.
</div>
</div>
<div class="instr-step">
<div class="instr-step-num">3</div>
<div class="instr-step-content instr-text">
<div class="instr-step-title">Выгрузка</div>
🆕 <strong>Только новые</strong> — для инкрементального обновления.<br/>
📋 <strong>Полная ведомость</strong> — для сверки.
</div>
</div>
<div class="instr-step">
<div class="instr-step-num">4</div>
<div class="instr-step-content instr-text">
<div class="instr-step-title">Дополнение из SmartReg</div>
Добавьте ID дисциплины и Период (напр., <kode>2024/2025 2 модуль</kode>).
</div>
</div>
<div class="instr-step">
<div class="instr-step-num">5</div>
<div class="instr-step-content instr-text">
<div class="instr-step-title">Финальная загрузка</div>
Отправьте файл Голубеву Александру.<br/>
<span style="color:var(--apple-accent)">💡 Рекомендация:</span> в письме указать <em>«загрузка первичной попытки»</em>.
</div>
</div>
</div>
'''
    st.markdown(html_2, unsafe_allow_html=True)

from logic.external_assessment import (
    load_existing_peresdachi,
    load_peresdachi_by_date_range,
    load_student_io_from_supabase,
    save_to_supabase,
    get_new_records_from_dataframe,
    deduplicate_and_split,
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
tab_tests, tab_projects = st.tabs(["Для 4 курса (Тесты)", "Для 3 курса (Проекты)"])

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

            # Загрузка студентов (с кэшированием в session_state)
            if 'students_df_tests' not in st.session_state:
                with st.spinner("Загрузка списка студентов из Supabase..."):
                    st.session_state['students_df_tests'] = load_students_from_supabase(filters={'курс': ['Курс 2', 'Курс 3', 'Курс 4']})
            students_df = st.session_state['students_df_tests']

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
                            
                            # 2. Дедупликация и разделение на новые/старые
                            split = deduplicate_and_split(result_df)

                            # Сохраняем обработанное состояние для отображения
                            st.session_state['tests_processed_state'] = {
                                **split,
                                'processed_at': datetime.now(),
                                'save_msg': ''
                            }

                            # Автоматическое сохранение при обработке
                            save_success, save_msg = save_to_supabase(split['display_new_records'])
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
            
            # Загрузка студентов (с кэшированием в session_state)
            if 'students_df_projects' not in st.session_state:
                with st.spinner("Загрузка студентов из Supabase..."):
                    st.session_state['students_df_projects'] = load_students_from_supabase(filters={'курс': ['Курс 2', 'Курс 3', 'Курс 4']})
            students_df = st.session_state['students_df_projects']
            
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
                                
                                # 2. Дедупликация и разделение на новые/старые
                                split = deduplicate_and_split(result_df)

                                # Сохранение состояния
                                st.session_state['projects_processed_state'] = {
                                    **split,
                                    'processed_at': datetime.now(),
                                    'save_msg': ''
                                }

                                save_success, save_msg = save_to_supabase(split['display_new_records'])
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
st.markdown("---")
with st.expander("📥 Выгрузка данных из базы (peresdachi)", expanded=False):
    st.markdown("Выберите диапазон дат добавления записей в базу данных:")

    from datetime import date, timedelta
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        date_from = st.date_input(
            "Дата от",
            value=date.today() - timedelta(days=30),
            key="peresdachi_date_from"
        )
    with col_date2:
        date_to = st.date_input(
            "Дата до",
            value=date.today(),
            key="peresdachi_date_to"
        )

    if st.button("Загрузить записи", key="load_peresdachi_by_date"):
        if date_from > date_to:
            st.error("Дата начала не может быть позже даты окончания.")
        else:
            with st.spinner("Загрузка данных из базы..."):
                try:
                    filtered_df = load_peresdachi_by_date_range(date_from, date_to)
                    st.session_state["peresdachi_filtered_df"] = filtered_df
                    st.session_state["peresdachi_filter_dates"] = (date_from, date_to)
                except Exception as e:
                    st.error(f"Ошибка при загрузке данных: {str(e)}")

    if "peresdachi_filtered_df" in st.session_state:
        filtered_df = st.session_state["peresdachi_filtered_df"]
        d_from, d_to = st.session_state.get("peresdachi_filter_dates", (None, None))

        if filtered_df.empty:
            st.info(f"Записей за период {d_from} — {d_to} не найдено.")
        else:
            st.metric("Найдено записей", len(filtered_df))
            st.dataframe(filtered_df, use_container_width=True)

            output_filtered = io.BytesIO()
            with pd.ExcelWriter(output_filtered, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, index=False)
            output_filtered.seek(0)

            file_label = f"{d_from}_to_{d_to}".replace("-", "") if d_from else "filtered"
            st.download_button(
                label="⬇️ Скачать XLSX",
                data=output_filtered,
                file_name=f"peresdachi_{file_label}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_peresdachi_filtered"
            )
