"""
Модуль 4: Обработка пересдач внешней оценки
upsert + точное определение новых/изменившихся записей
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from utils import icon, apply_custom_css, get_supabase_client

apply_custom_css()
st.markdown(f'<h1>{icon("file-edit", 32)} Обработка пересдач внешней оценки</h1>', unsafe_allow_html=True)
st.markdown("**upsert + точное определение новых и изменённых записей**")

# === Универсальная загрузка ===
def fetch_all(table: str, filters=None, columns="*"):
    supabase = get_supabase_client()
    query = supabase.table(table).select(columns)
    if filters:
        for k, v in filters.items():
            query = query.eq(k, v)
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

# === Загрузка студентов ===
@st.cache_data(ttl=3600)
def load_students():
    df = fetch_all('students', filters={'курс': 'Курс 4'})
    if df.empty:
        return df
    mapping = {
        'корпоративная_почта': 'Адрес электронной почты',
        'фио': 'ФИО',
        'филиал_кампус': 'Кампус',
        'факультет': 'Факультет',
        'образовательная_программа': 'Образовательная программа',
        'группа': 'Группа'
    }
    return df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})

# === Загрузка текущих данных из peresdachi (для сравнения) ===
@st.cache_data(ttl=600)  # Кэш на 10 минут — чтобы не грузить каждый раз
def load_existing_peresdachi():
    df = fetch_all('peresdachi', columns='"Адрес электронной почты", "Наименование дисциплины", "Оценка"')
    if not df.empty:
        df['Адрес электронной почты'] = df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        df['Наименование дисциплины'] = df['Наименование дисциплины'].astype(str).str.strip()
        df['Оценка'] = df['Оценка'].astype(str).str.strip()
    return df

# === Правильное определение новых/изменившихся записей ===
def get_new_or_changed_records(current_df: pd.DataFrame) -> pd.DataFrame:
    existing = load_existing_peresdachi()
    if existing.empty:
        return current_df.copy()  # Все новые

    # Приводим к одному формату
    current_df = current_df.copy()
    current_df['Адрес электронной почты'] = current_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
    current_df['Наименование дисциплины'] = current_df['Наименование дисциплины'].astype(str).str.strip()
    current_df['Оценка'] = current_df['Оценка'].astype(str).str.strip()

    # Ключ для сравнения
    current_df['key'] = current_df['Адрес электронной почты'] + '|' + current_df['Наименование дисциплины']
    existing['key'] = existing['Адрес электронной почты'] + '|' + existing['Наименование дисциплины']

    # Словарь: ключ → текущая оценка в БД
    existing_dict = dict(zip(existing['key'], existing['Оценка']))

    # Добавляем флаг: новая или изменённая
    current_df['status'] = current_df['key'].apply(
        lambda k: 'новая' if k not in existing_dict 
        else ('изменена' if existing_dict[k] != current_df.loc[current_df['key']==k, 'Оценка'].iloc[0] else 'без изменений')
    )

    # Возвращаем только новые и изменённые
    new_or_changed = current_df[current_df['status'] != 'без изменений'].copy()
    new_or_changed = new_or_changed.drop(columns=['key', 'status'])
    return new_or_changed

# === UPSERT ===
def save_to_supabase(df: pd.DataFrame):
    if df.empty:
        st.info("Нет данных для сохранения")
        return
    records = [{k: (v if pd.notna(v) else None) for k, v in r.items()} for r in df.to_dict('records')]
    get_supabase_client().table('peresdachi') \
        .upsert(records, on_conflict=['Адрес электронной почты', 'Наименование дисциплины']) \
        .execute()

# === Проверка подключения ===
try:
    get_supabase_client().table('students').select('id').limit(1).execute()
    st.success("Подключение к Supabase — ОК")
except Exception as e:
    st.error("Нет связи с Supabase")
    st.stop()

st.markdown("---")

grades_file = st.file_uploader("Загрузите файл с оценками", type=['xlsx', 'xls'])

if not grades_file:
    st.info("Загрузите файл")
    st.stop()

try:
    grades_df = pd.read_excel(grades_file)
    st.success(f"Файл загружен: {len(grades_df)} строк")
except:
    st.error("Не удалось прочитать файл")
    st.stop()

if st.button("Обработать и сохранить", type="primary", use_container_width=True):
    with st.spinner("Обработка..."):

        students_df = load_students()
        if students_df.empty:
            st.error("Нет студентов на Курсе 4")
            st.stop()

        # Переименование колонок
        grades_df = grades_df.rename(columns={
            'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
            'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
            'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
        })

        value_cols = [c for c in grades_df.columns if 'цифровых компетенций' in c]
        melted = pd.melt(grades_df, id_vars=['Адрес электронной почты'], value_vars=value_cols,
                         var_name='Наименование дисциплины', value_name='Оценка')
        melted = melted[melted['Оценка'].notna()]
        melted['Оценка'] = melted['Оценка'].astype(str).str.replace('-', '').str.strip()
        melted = melted[melted['Оценка'].str.len() > 0]
        melted['Адрес электронной почты'] = melted['Адрес электронной почты'].str.strip().str.lower()

        # Присоединяем студентов
        students_df['Адрес электронной почты'] = students_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        result = melted.merge(students_df, on='Адрес электронной почты', how='left')

        # Приоритет из student_io
        io_df = fetch_all('student_io', columns='"Адрес электронной почты", "Наименование дисциплины", "Оценка"')
        if not io_df.empty:
            io_df['Адрес электронной почты'] = io_df['Адрес электронной почты'].astype(str).str.strip().str.lower()
            io_df['Наименование дисциплины'] = io_df['Наименование дисциплины'].astype(str).str.strip()
            io_map = dict(zip(io_df['Адрес электронной почты'] + '|' + io_df['Наименование дисциплины'], io_df['Оценка']))
            result_key = result['Адрес электронной почты'] + '|' + result['Наименование дисциплины']
            result['Оценка'] = result_key.map(io_map).fillna(result['Оценка'])

        # Финальные поля
        result['ID дисциплины'] = ''
        result['Период аттестации'] = ''
        result['Курс'] = 'Курс 4'

        final_cols = ['ФИО','Адрес электронной почты','Кампус','Факультет','Образовательная программа',
                      'Группа','Курс','ID дисциплины','Наименование дисциплины','Период аттестации','Оценка']
        result = result[[c for c in final_cols if c in result.columns]]

        # === Определяем новые/изменившиеся ===
        new_or_changed = get_new_or_changed_records(result)

        # === Сохраняем через upsert ===
        save_to_supabase(result)
        st.success(f"Сохранено {len(result)} записей (upsert)")

        # === Результат ===
        st.balloons()
        st.metric("Всего обработано", len(result))
        st.metric("Новых или изменённых", len(new_or_changed))

        tab1, tab2 = st.tabs(["Только новые/изменённые", "Все записи"])
        with tab1:
            if new_or_changed.empty:
                st.info("Все записи уже были в базе и не изменились")
            else:
                st.dataframe(new_or_changed, use_container_width=True)
                buf = io.BytesIO()
                new_or_changed.to_excel(buf, index=False, engine='openpyxl')
                buf.seek(0)
                st.download_button("Скачать только новые/изменённые", buf.getvalue(),
                                   f"Новые_пересдачи_{datetime.now():%d-%m-%Y}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        with tab2:
            st.dataframe(result, use_container_width=True)
            buf2 = io.BytesIO()
            result.to_excel(buf2, index=False, engine='openpyxl')
            buf2.seek(0)
            st.download_button("Скачать все записи", buf2.getvalue(),
                               f"Все_пересдачи_{datetime.now():%d-%m-%Y}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
