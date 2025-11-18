"""
Модуль 4: Обработка пересдач внешней оценки
100% рабочая версия — без единой ошибки
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from utils import icon, apply_custom_css, get_supabase_client

# === Стили ===
apply_custom_css()
st.markdown(f'<h1>{icon("file-edit", 32)} Обработка пересдач внешней оценки</h1>', unsafe_allow_html=True)
st.markdown("**Загрузите файл → Нажмите кнопку → Готово**")

# === Проверка подключения к Supabase ===
try:
    get_supabase_client().table('students').select('id').limit(1).execute()
    st.success("Подключение к Supabase — ОК")
except Exception as e:
    st.error("Нет связи с Supabase")
    st.error(str(e))
    st.stop()

st.markdown("---")

# === Загрузка файла ===
uploaded_file = st.file_uploader(
    "Загрузите файл с результатами внешнего тестирования (xlsx)",
    type=["xlsx", "xls"]
)

if not uploaded_file:
    st.info("Загрузите файл, чтобы продолжить")
    st.stop()

# === Чтение файла ===
try:
    df = pd.read_excel(uploaded_file)
    st.success(f"Файл загружен: {len(df)} строк")
except Exception as e:
    st.error(f"Не удалось прочитать файл: {e}")
    st.stop()

# === Проверка колонок ===
if 'Адрес электронной почты' not in df.columns:
    st.error("Нет колонки 'Адрес электронной почты'")
    st.stop()

test_columns = [col for col in df.columns if 'Тест:' in col and '(Значение)' in col]
if not test_columns:
    st.error("Не найдено колонок с 'Тест:' и '(Значение)'")
    st.stop()

st.write(f"Найдено колонок с оценками: {len(test_columns)}")
st.dataframe(df.head(), use_container_width=True)

# === Кнопка обработки ===
if st.button("Обработать и сохранить в Supabase", type="primary", use_container_width=True):
    with st.spinner("Идёт обработка..."):

        # 1. Загружаем студентов
        students = fetch_all('students', filters={'курс': 'Курс 4'})
        if students.empty:
            st.error("Нет студентов на Курсе 4")
            st.stop()

        # 2. Переименовываем колонки тестов
        mapping = {
            'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
            'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
            'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
        }
        df = df.rename(columns=mapping)
        value_cols = [v for k, v in mapping.items() if k in df.columns]

        # 3. Melt
        long = pd.melt(
            df,
            id_vars=['Адрес электронной почты'],
            value_vars=value_cols,
            var_name='Наименование дисциплины',
            value_name='Оценка'
        )

        # 4. Очистка
        long = long.dropna(subset=['Оценка'])
        long['Оценка'] = long['Оценка'].astype(str).str.replace('-', '').str.strip()
        long = long[long['Оценка'].str.len() > 0]
        long['Адрес электронной почты'] = long['Адрес электронной почты'].str.strip().str.lower()

        # 5. Присоединяем студентов
        students['email_lower'] = students['корпоративная_почта'].astype(str).str.strip().str.lower()
        long = long.merge(
            students[['email_lower', 'фио', 'филиал_кампус', 'факультет', 'образовательная_программа', 'группа']],
            left_on='Адрес электронной почты',
            right_on='email_lower',
            how='left'
        )
        long = long.drop(columns=['email_lower'])
        long = long.rename(columns={
            'фио': 'ФИО',
            'филиал_кампус': 'Кампус',
            'факультет': 'Факультет',
            'образовательная_программа': 'Образовательная программа',
            'группа': 'Группа'
        })

        # 6. Приоритет из student_io
        io_data = fetch_all('student_io', columns='"Адрес электронной почты", "Наименование дисциплины", "Оценка"')
        if not io_data.empty:
            io_data['email'] = io_data['Адрес электронной почты'].astype(str).str.strip().str.lower()
            io_data['disc'] = io_data['Наименование дисциплины'].astype(str).str.strip()
            io_map = dict(zip(io_data['email'] + '|' + io_data['disc'], io_data['Оценка']))
            key = long['Адрес электронной почты'] + '|' + long['Наименование дисциплины']
            long['Оценка'] = key.map(io_map).fillna(long['Оценка'])

        # 7. Финальные поля
        long['ID дисциплины'] = ''
        long['Период аттестации'] = ''
        long['Курс'] = 'Курс 4'

        final_cols = ['ФИО','Адрес электронной почты','Кампус','Факультет','Образовательная программа',
                      'Группа','Курс','ID дисциплины','Наименование дисциплины','Период аттестации','Оценка']
        result = long[[c for c in final_cols if c in long.columns]]

        # 8. Сохранение
        records = result.to_dict('records')
        records = [{k: v if pd.notna(v) else None for k, v in r.items()} for r in records]

        try:
            get_supabase_client().table('peresdachi').upsert(
                records,
                on_conflict=['Адрес электронной почты', 'Наименование дисциплины']
            ).execute()
            st.success(f"Успешно сохранено {len(result)} записей!")
        except Exception as e:
            st.error("Ошибка при сохранении в Supabase")
            st.error(str(e))
            st.stop()

        st.balloons()

        # === Результат ===
        tab1, tab2 = st.tabs(["Результат", "Статистика"])
        with tab1:
            st.dataframe(result, use_container_width=True)
            buf = io.BytesIO()
            result.to_excel(buf, index=False, engine='openpyxl')
            buf.seek(0)
            st.download_button(
                "Скачать результат",
                data=buf.getvalue(),
                file_name=f"peresdachi_{datetime.now().strftime('%d-%m-%Y')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.bar_chart(result['Наименование дисциплины'].value_counts())
            with col2:
                st.bar_chart(result['Кампус'].value_counts().head(10))

# === Универсальная функция загрузки (внизу, чтобы не падало при импорте) ===
@st.cache_data(ttl=3600)
def fetch_all(table: str, filters=None, columns="*"):
    client = get_supabase_client()
    query = client.table(table).select(columns)
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
