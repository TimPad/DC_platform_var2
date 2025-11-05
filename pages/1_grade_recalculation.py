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

def process_grade_recalculation(df: pd.DataFrame, use_dynamics: bool) -> pd.DataFrame:
    """
    Обработка данных для перезачета оценок
    
    Args:
        df: DataFrame с данными студентов
        use_dynamics: Учитывать ли динамику оценок
        
    Returns:
        Обработанный DataFrame с колонками ДПР_итог и НЭ_итог
    """
    processed_df = df.copy()

    required_columns = [
        'Наименование НЭ', 'Оценка НЭ', 'Оценка дисциплины-пререквизита',
        'Внешнее измерение цифровых компетенций. Входной контроль',
        'Внешнее измерение цифровых компетенций. Промежуточный контроль',
        'Внешнее измерение цифровых компетенций. Итоговый контроль'
    ]
    
    for col in required_columns:
        if col not in processed_df.columns:
            raise KeyError(f"Отсутствует обязательный столбец: '{col}'")

    processed_df['Оценка дисциплины-пререквизита'] = processed_df['Оценка дисциплины-пререквизита'].apply(
        lambda x: 8 if x >= 9 else x
    )

    processed_df['Этап'] = 1
    processed_df.loc[processed_df['Наименование НЭ'].str.contains('анализу данных', case=False, na=False), 'Этап'] = 3
    processed_df.loc[processed_df['Наименование НЭ'].str.contains('программированию', case=False, na=False), 'Этап'] = 2

    dpr_results = []
    ie_results = []

    for index, row in processed_df.iterrows():
        if row['Этап'] == 1:
            innopolis_grade = row['Внешнее измерение цифровых компетенций. Входной контроль']
        elif row['Этап'] == 2:
            innopolis_grade = row['Внешнее измерение цифровых компетенций. Промежуточный контроль']
        else:
            innopolis_grade = row['Внешнее измерение цифровых компетенций. Итоговый контроль']

        if use_dynamics:
            vhod = row['Внешнее измерение цифровых компетенций. Входной контроль']
            prom = row['Внешнее измерение цифровых компетенций. Промежуточный контроль']
            itog = row['Внешнее измерение цифровых компетенций. Итоговый контроль']
            
            if (vhod - prom > 1) or (vhod - itog > 1) or (prom - itog > 1):
                dpr_results.append(np.nan)
                ie_results.append(np.nan)
                continue

        ne_grade = row['Оценка НЭ']
        dpr_grade = row['Оценка дисциплины-пререквизита']
        
        ne_grade = 0 if pd.isna(ne_grade) else ne_grade
        dpr_grade = 0 if pd.isna(dpr_grade) else dpr_grade
        innopolis_grade = 0 if pd.isna(innopolis_grade) else innopolis_grade

        max_grade = max(ne_grade, dpr_grade, innopolis_grade)
        
        # Расчет ДПР_итог
        dpr_final = np.nan
        if ne_grade < 4:
            dpr_final = np.nan
        elif max_grade == innopolis_grade and innopolis_grade > 3 and innopolis_grade != dpr_grade and innopolis_grade != ne_grade:
            dpr_final = innopolis_grade
        elif ne_grade == dpr_grade:
            dpr_final = np.nan
        elif dpr_grade < 4:
            dpr_final = ne_grade if ne_grade >= 4 else np.nan
        elif max_grade == dpr_grade and dpr_grade >= 4:
            dpr_final = np.nan
        else:
            dpr_final = ne_grade
        dpr_results.append(dpr_final)

        # Расчет НЭ_итог
        ie_final = np.nan
        if ne_grade < 4:
            ie_final = np.nan
        elif max_grade == innopolis_grade and innopolis_grade > 3 and innopolis_grade != dpr_grade and innopolis_grade != ne_grade:
            ie_final = innopolis_grade
        elif ne_grade == dpr_grade:
            ie_final = np.nan
        elif max_grade == dpr_grade and dpr_grade >= 4:
            if ne_grade >= 8:
                ie_final = np.nan
            elif dpr_grade >= 8:
                ie_final = 8
            else:
                ie_final = dpr_grade
        elif ne_grade < 4 and innopolis_grade > 3 and use_dynamics:
             ie_final = innopolis_grade
        else:
            ie_final = np.nan
        ie_results.append(ie_final)

    processed_df['ДПР_итог'] = dpr_results
    processed_df['НЭ_итог'] = ie_results
    
    return processed_df

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
