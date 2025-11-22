"""
Модуль 1: Перезачет оценок
Автоматический расчет итоговых оценок студентов
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
from utils import icon, apply_custom_css

# Применяем кастомные стили
apply_custom_css()

# Заголовок страницы
st.markdown(
    f'<h1>{icon("bar-chart-3", 32)} Перезачет оценок</h1>',
    unsafe_allow_html=True
)

st.markdown("""
Загрузите Excel или CSV файл с данными студентов для автоматического расчета итоговых оценок.

**Требуемые колонки:**
- Наименование НЭ
- Оценка НЭ
- Оценка дисциплины-пререквизита
- Внешнее измерение цифровых компетенций (Входной, Промежуточный, Итоговый контроль)
""")

from logic.grade_recalculation import process_grade_recalculation

# Загрузка файла
uploaded_file = st.file_uploader(
    "Выберите файл для обработки",
    type=['xlsx', 'csv'],
    key="grade_file"
)

if uploaded_file is not None:
    file_name = uploaded_file.name
    
    processing_mode = st.radio(
        "Режим обработки:",
        ("Перезачет БЕЗ динамики", "Перезачет С динамикой"),
        help="""
        - **БЕЗ динамики**: Стандартный перезачет по максимальной оценке.
        - **С динамикой**: Если оценка падает более чем на 1 балл между этапами, перезачет блокируется.
        """
    )

    if st.button("Обработать файл", type="primary"):
        with st.spinner("Обработка данных..."):
            try:
                if file_name.endswith('.xlsx'):
                    df_initial = pd.read_excel(uploaded_file, engine='openpyxl')
                else:
                    df_initial = pd.read_csv(uploaded_file)

                use_dynamics_flag = (processing_mode == "Перезачет С динамикой")
                result_df = process_grade_recalculation(df_initial, use_dynamics=use_dynamics_flag)
                
                st.success("Обработка успешно завершена!")
                
                st.subheader("Предварительный просмотр")
                st.dataframe(result_df.head(10), use_container_width=True)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    result_df.to_excel(writer, index=False, sheet_name='Результат')
                excel_data = output.getvalue()

                current_date = datetime.now().strftime('%d-%m-%y')
                download_filename = f"Результат_{file_name.split('.')[0]}_{current_date}.xlsx"
                
                st.download_button(
                    label="Скачать результат",
                    data=excel_data,
                    file_name=download_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            except KeyError as e:
                st.error(f"Ошибка в структуре файла: {e}")
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
