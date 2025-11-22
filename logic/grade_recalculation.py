"""
Logic for Grade Recalculation Module
"""
import pandas as pd
import numpy as np

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
