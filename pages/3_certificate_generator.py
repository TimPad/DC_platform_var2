"""
Модуль 3: Генератор сертификатов
Обработка данных экзаменов студентов
"""

import streamlit as st
import pandas as pd
import io
import os
import tempfile
from typing import Dict, Tuple
from utils import icon, apply_custom_css

# Применяем кастомные стили
apply_custom_css()

# Заголовок страницы
st.markdown(
    f'<h1>{icon("scroll-text", 32)} Генератор сертификатов</h1>',
    unsafe_allow_html=True
)

st.markdown("""
Автоматическая обработка данных экзаменов студентов и генерация текста для сертификатов.

**Требуется два файла:**
1. Excel с данными студентов (колонки: Учащийся, Дисциплина 1/2/3, Оценка 5 баллов)
2. Excel со справочником навыков (колонки: Дисциплина, Уровень_оценки, Описание_навыков)
""")

def deduplicate_lines(text):
    """Удаляет дублирующиеся строки из текста"""
    if pd.isna(text) or not isinstance(text, str):
        return text
    
    lines = text.split('\n')
    seen_lines = set()
    unique_lines = []
    
    for line in lines:
        line_clean = line.strip()
        if line_clean and line_clean not in seen_lines:
            seen_lines.add(line_clean)
            unique_lines.append(line)
    
    return '\n'.join(unique_lines)

@st.cache_data
def load_reference_data(skills_content: bytes) -> Dict[str, str]:
    """Загрузка справочных данных из файла навыков"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        tmp_file.write(skills_content)
        tmp_file_path = tmp_file.name
    
    try:
        skills_df = pd.read_excel(tmp_file_path)
        
        grade_mapping = {}
        for _, row in skills_df.iterrows():
            discipline = row['Дисциплина']
            level = row['Уровень_оценки']
            description = row['Описание_навыков']
            clean_description = deduplicate_lines(description)
            composite_key = f"{discipline}—{level}"
            grade_mapping[composite_key] = clean_description
        
        return grade_mapping
    finally:
        os.unlink(tmp_file_path)

def process_student_data(df: pd.DataFrame, grade_mapping: Dict[str, str]) -> Tuple[pd.DataFrame, list]:
    """Обработка данных студентов для сертификатов"""
    results = []
    processing_log = []
    
    processing_log.append(f"Обрабатываем {len(df)} студентов")
    
    for index, row in df.iterrows():
        student_results = []
        processed_keys = set()
        
        for discipline_num in range(1, 4):
            discipline_col = f"Дисциплина {discipline_num}"
            grade_5_col = f"Оценка 5 баллов Дисциплина {discipline_num}"
            
            if discipline_col not in df.columns or grade_5_col not in df.columns:
                continue
                
            discipline_value = str(row[discipline_col]).strip()
            grade_value = str(row[grade_5_col]).strip()
            
            if pd.isna(discipline_value) or pd.isna(grade_value) or discipline_value == 'nan' or grade_value == 'nan':
                continue
            
            lookup_key = f"{discipline_value}—{grade_value}"
            
            if lookup_key in processed_keys:
                continue
            
            if lookup_key in grade_mapping:
                skill_description = grade_mapping[lookup_key]
                
                short_name_col = f"Название Дисциплины {discipline_num}"
                if short_name_col in df.columns:
                    display_name = str(row[short_name_col]).strip()
                    formatted_discipline = display_name.capitalize() if display_name != 'nan' and display_name else discipline_value
                else:
                    formatted_discipline = discipline_value
                
                formatted_result = f"{formatted_discipline}:\n{skill_description}"
                student_results.append(formatted_result)
                processed_keys.add(lookup_key)
        
        final_result = "\n\n".join(student_results) if student_results else "Навыки не найдены."
        results.append(final_result)
    
    processing_log.append(f"Успешно обработано")
    
    df_result = df.copy()
    df_result['Итоговый результат'] = results
    
    columns_to_remove = [col for col in df_result.columns if col.startswith("Название Дисциплины ")]
    if columns_to_remove:
        df_result = df_result.drop(columns=columns_to_remove)
    
    return df_result, processing_log

# Кнопки скачивания примеров
st.markdown("### Примеры файлов")
st.markdown("Скачайте примеры файлов для правильного форматирования данных:")

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    # Excel пример студентов
    excel_example_path = os.path.join(current_dir, 'Сертификаты пример.xlsx')
    if os.path.exists(excel_example_path):
        with open(excel_example_path, 'rb') as example_file:
            excel_example_data = example_file.read()
        
        st.download_button(
            label="Пример данных студентов",
            data=excel_example_data,
            file_name="Сертификаты_пример.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Скачайте этот файл как шаблон для ваших данных студентов",
            use_container_width=True
        )

with col_btn2:
    # Excel справочник навыков
    skills_example_path = os.path.join(current_dir, 'агрегированные_навыки.xlsx')
    if os.path.exists(skills_example_path):
        with open(skills_example_path, 'rb') as skills_file:
            skills_data = skills_file.read()
        
        st.download_button(
            label="Справочник навыков",
            data=skills_data,
            file_name="агрегированные_навыки.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Скачайте справочник с описаниями навыков",
            use_container_width=True
        )

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Данные студентов")
    excel_file = st.file_uploader(
        "Выберите Excel файл",
        type=['xlsx', 'xls'],
        key="students_file"
    )

with col2:
    st.subheader("Справочник навыков")
    skills_file = st.file_uploader(
        "Выберите Excel файл",
        type=['xlsx', 'xls'],
        key="skills_file"
    )

if excel_file and skills_file:
    try:
        with st.spinner("Загрузка файлов..."):
            df = pd.read_excel(excel_file)
            skills_content = skills_file.read()
            grade_mapping = load_reference_data(skills_content)
        
        st.success("Файлы успешно загружены!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Студентов", len(df))
        with col2:
            st.metric("Колонок", len(df.columns))
        with col3:
            st.metric("Навыков в справочнике", len(grade_mapping))
        
        with st.expander("Предпросмотр данных"):
            st.dataframe(df.head(), use_container_width=True)
        
        if st.button("Обработать данные", type="primary"):
            with st.spinner("Обработка..."):
                result_df, processing_log = process_student_data(df, grade_mapping)
            
            st.success("Обработка завершена!")
            
            st.subheader("Результаты")
            st.dataframe(result_df, use_container_width=True)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
                result_df.to_excel(writer, index=False)
            output.seek(0)
            
            st.download_button(
                label="Скачать результаты",
                data=output.getvalue(),
                file_name="Сертификаты_с_результатами.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    except Exception as e:
        st.error(f"Ошибка: {str(e)}")

elif excel_file:
    st.info("Загрузите также файл со справочником навыков")
elif skills_file:
    st.info("Загрузите также файл с данными студентов")
else:
    st.info("Загрузите оба файла для начала работы")
