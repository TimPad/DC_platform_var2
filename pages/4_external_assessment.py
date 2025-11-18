"""
Модуль 4: Обработка пересдач внешней оценки
Supabase интеграция — теперь с UPSERT (без дублей!)
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from utils import icon, apply_custom_css, get_supabase_client

apply_custom_css()
st.markdown(f'<h1>{icon("file-edit", 32)} Обработка пересдач внешней оценки</h1>', unsafe_allow_html=True)
st.markdown("""
**Автоматическая обработка результатов внешнего тестирования**

Теперь используется **upsert** — существующие записи обновляются, новые добавляются.  
Дубли невозможны (уникальный индекс в базе по email + дисциплина).
""")

# === Универсальная загрузка с пагинацией ===
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

# === Загрузка студентов (Курс 4) ===
@st.cache_data(ttl=3600)
def load_students():
    df = fetch_all('students', filters={'курс': 'Курс 4'})
    if df.empty:
        return df
    mapping = {
        'корпоративная_почта': 'Адрес электронной почты',
        'фио': 'ФИО',
        'филиал_кампус': 'Филиал (кампус)',
        'факультет': 'Факультет',
        'образовательная_программа': 'Образовательная программа',
        'группа': 'Группа',
        'курс': 'Курс'
    }
    return df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})

# === Загрузка student_io ===
@st.cache_data(ttl=3600)
def load_student_io():
    df = fetch_all('student_io', columns='"Адрес электронной почты", "Наименование дисциплины", "Оценка"')
    if not df.empty:
        df['Адрес электронной почты'] = df['Адрес электронной почты'].astype(str).str.strip().str.lower()
        df['Наименование дисциплины'] = df['Наименование дисциплины'].astype(str).str.strip()
        df['Оценка'] = df['Оценка'].astype(str).str.strip()
    return df

# === UPSERT в peresdachi (ГЛАВНОЕ ИЗМЕНЕНИЕ) ===
def save_to_supabase(df: pd.DataFrame) -> bool:
    if df.empty:
        st.info("Нет данных для сохранения")
        return True
    try:
        records = [{k: (v if pd.notna(v) else None) for k, v in r.items()} 
                  for r in df.to_dict('records')]
        
        get_supabase_client().table('peresdachi') \
            .upsert(records, on_conflict=['Адрес электронной почты', 'Наименование дисциплины']) \
            .execute()
        
        st.success(f"Успешно сохранено/обновлено {len(df)} записей в `peresdachi`")
        return True
    except Exception as e:
        st.error("Ошибка при сохранении в Supabase")
        st.code(str(e))
        return False

# === Проверка подключения ===
try:
    get_supabase_client().table('students').select('id').limit(1).execute()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения: {e}")
    st.stop()

st.markdown("---")

# === Загрузка файла ===
grades_file = st.file_uploader(
    "Загрузите файл с оценками (xlsx)",
    type=['xlsx', 'xls'],
    help="Обязательно: 'Адрес электронной почты' и колонки 'Тест:... (Значение)'"
)

if not grades_file:
    st.info("Загрузите файл для начала")
    with st.expander("Текущие данные в peresdachi"):
        curr = fetch_all('peresdachi')
        st.metric("Записей", len(curr))
        st.dataframe(curr.head(10)) if not curr.empty else st.info("Пусто")
    st.stop()

try:
    grades_df = pd.read_excel(grades_file)
    st.success(f"Файл загружен: {len(grades_df)} строк")
except Exception as e:
    st.error(f"Ошибка чтения файла: {e}")
    st.stop()

# === Обработка ===
if st.button("Обработать и сохранить в Supabase", type="primary", use_container_width=True):
    with st.spinner("Обработка..."):

        students_df = load_students()
        if students_df.empty:
            st.error("Нет студентов на Курсе 4")
            st.stop()

        # Переименование колонок тестов
        grades_df = grades_df.rename(columns={
            'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
            'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
            'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
        })

        value_cols = [col for col in grades_df.columns if 'цифровых компетенций' in col]
        if not value_cols:
            st.error("Не найдено колонок с результатами тестирования")
            st.stop()

        # Melt
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
        io_df = load_student_io()
        if not io_df.empty:
            key_map = dict(zip(
                io_df['Адрес электронной почты'] + '|' + io_df['Наименование дисциплины'],
                io_df['Оценка']
            ))
            result_key = result['Адрес электронной почты'] + '|' + result['Наименование дисциплины']
            result['Оценка'] = result_key.map(key_map).fillna(result['Оценка'])

        # Финальные колонки
        result['ID дисциплины'] = ''
        result['Период аттестации'] = ''
        result['Курс'] = 'Курс 4'
        if 'Филиал (кампус)' in result.columns:
            result = result.rename(columns={'Филиал (кампус)': 'Кампус'})

        final_cols = ['ФИО','Адрес электронной почты','Кампус','Факультет','Образовательная программа',
                      'Группа','Курс','ID дисциплины','Наименование дисциплины','Период аттестации','Оценка']
        result = result[[c for c in final_cols if c in result.columns]]

        # === Сохранение через UPSERT ===
        save_to_supabase(result)

        st.balloons()
        st.metric("Обработано и сохранено записей", len(result))

        tab1, tab2 = st.tabs(["Результат", "Статистика"])
        with tab1:
            st.dataframe(result, use_container_width=True)
            buf = io.BytesIO()
            result.to_excel(buf, index=False, engine='openpyxl')
            buf.seek(0)
            st.download_button("Скачать результат", buf.getvalue(),
                               f"peresdachi_{datetime.now():%d-%m-%Y}.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.bar_chart(result['Наименование дисциплины'].value_counts())
            with c2:
                st.bar_chart(result['Кампус'].value_counts().head(10))
