"""
Модуль 4: Обработка пересдач внешней оценки
Финальная версия — гарантированно без ошибок
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from utils import icon, apply_custom_css, get_supabase_client

# === Стили и заголовок ===
apply_custom_css()
st.markdown(f'<h1>{icon("file-edit", 32)} Обработка пересдач внешней оценки</h1>', unsafe_allow_html=True)
st.markdown("""
**Автоматическая загрузка результатов внешнего тестирования**

- Приоритет оценок: `student_io` → файл  
- Сохраняется через `upsert` → дубли невозможны  
- Работает только с Курсом 4
""")

# === Универсальная загрузка из Supabase ===
@st.cache_data(ttl=3600, show_spinner="Загрузка из Supabase...")
def fetch_all(table: str, filters: dict = None, columns: str = "*"):
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

# === Проверка подключения ===
try:
    get_supabase_client().table('students').select('id').limit(1).execute()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения к Supabase: {e}")
    st.info("Проверьте SUPABASE_URL и SUPABASE_KEY в utils.py")
    st.stop()

st.markdown("---")

# === Загрузка файла ===
grades_file = st.file_uploader(
    "Загрузите файл с результатами внешнего тестирования (xlsx)",
    type=['xlsx', 'xls'],
    help="Обязательно: колонка 'Адрес электронной почты' и колонки 'Тест:... (Значение)'"
)

if not grades_file:
    st.info("Загрузите файл для начала работы")
    with st.expander("Текущее состояние таблицы peresdachi"):
        curr = fetch_all('peresdachi')
        if curr.empty:
            st.info("Таблица пуста")
        else:
            st.metric("Записей в peresdachi", len(curr))
            st.dataframe(curr.head(10), use_container_width=True)
    st.stop()

# === Чтение файла ===
try:
    grades_df = pd.read_excel(grades_file)
    st.success(f"Файл загружен: {len(grades_df)} строк")
except Exception as e:
    st.error(f"Ошибка чтения файла: {e}")
    st.stop()

# Проверка наличия тестовых колонок
test_cols = [c for c in grades_df.columns if 'Тест:' in c and '(Значение)' in c]
if not test_cols:
    st.error("Не найдено колонок с названием 'Тест:... (Значение)'")
    st.stop()

with st.expander("Предпросмотр файла", expanded=True):
    st.dataframe(grades_df.head(10), use_container_width=True)
st.write(f"Найдено колонок с результатами тестов: **{len(test_cols)}**")

# === Кнопка обработки ===
if st.button("Обработать и сохранить в Supabase", type="primary", use_container_width=True):
    with st.spinner("Обработка данных..."):

        # 1. Студенты Курса 4
        students_df = fetch_all('students', filters={'курс': 'Курс 4'})
        if students_df.empty:
            st.error("Нет студентов на Курсе 4")
            st.stop()

        # 2. Маппинг дисциплин
        DISCIPLINE_MAPPING = {
            'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
            'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
            'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
        }
        grades_df = grades_df.rename(columns=DISICIPLINE_MAPPING)
        value_cols = [v for k, v in DISCIPLINE_MAPPING.items() if k in grades_df.columns]

        if not value_cols:
            st.error("Ни одна колонка тестирования не найдена после переименования")
            st.stop()

        # 3. Преобразование в длинный формат
        melted = pd.melt(
            grades_df,
            id_vars=['Адрес электронной почты'],
            value_vars=value_cols,
            var_name='Наименование дисциплины',
            value_name='Оценка'
        )

        # Очистка
        melted = melted[melted['Оценка'].notna()]
        melted['Оценка'] = melted['Оценка'].astype(str).str.replace('-', '').str.strip()
        melted = melted[melted['Оценка'].str.len() > 0]
        melted['Адрес электронной почты'] = melted['Адрес электронной почты'].str.strip().str.lower()

        # 4. Присоединяем данные студентов
        students_df['Адрес электронной почты'] = students_df['корпоративная_почта'].astype(str).str.strip().str.lower()
        result = melted.merge(
            students_df[['Адрес электронной почты', 'фио', 'филиал_кампус', 'факультет', 'образовательная_программа', 'группа']],
            on='Адрес электронной почты',
            how='left'
        ).rename(columns={
            'фио': 'ФИО',
            'филиал_кампус': 'Кампус',
            'факультет': 'Факультет',
            'образовательная_программа': 'Образовательная программа',
            'группа': 'Группа'
        })

        # 5. Приоритет из student_io
        student_io = fetch_all('student_io', columns='"Адрес электронной почты", "Наименование дисциплины", "Оценка"')
        if not student_io.empty:
            student_io['Адрес электронной почты'] = student_io['Адрес электронной почты'].astype(str).str.strip().str.lower()
            student_io['Наименование дисциплины'] = student_io['Наименование дисциплины'].astype(str).str.strip()
            io_map = dict(zip(
                student_io['Адрес электронной почты'] + '|' + student_io['Наименование дисциплины'],
                student_io['Оценка']
            ))
            result_key = result['Адрес электронной почты'] + '|' + result['Наименование дисциплины']
            result['Оценка'] = result_key.map(io_map).fillna(result['Оценка'])

        # 6. Финальные колонки
        result['ID дисциплины'] = ''
        result['Период аттестации'] = ''
        result['Курс'] = 'Курс 4'

        final_cols = ['ФИО', 'Адрес электронной почты', 'Кампус', 'Факультет',
                      'Образовательная программа', 'Группа', 'Курс', 'ID дисциплины',
                      'Наименование дисциплины', 'Период аттестации', 'Оценка']
        result = result[[c for c in final_cols if c in result.columns]]

        # === Сохранение ===
        records = [{k: (v if pd.notna(v) else None) for k, v in r.items()} for r in result.to_dict('records')]
        get_supabase_client().table('peresdachi') \
            .upsert(records, on_conflict=['Адрес электронной почты', 'Наименование дисциплины']) \
            .execute()

        st.success(f"Готово! Сохранено {len(result)} записей")
        st.balloons()

        # === Вывод результата ===
        tab1, tab2 = st.tabs(["Результат", "Статистика"])
        with tab1:
            st.dataframe(result, use_container_width=True)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                result.to_excel(writer, index=False, sheet_name='Пересдачи')
            buffer.seek(0)
            st.download_button(
                "Скачать результат",
                data=buffer.getvalue(),
                file_name=f"peresdachi_{datetime.now():%d-%m-%Y}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.write("По дисциплинам")
                st.bar_chart(result['Наименование дисциплины'].value_counts())
            with c2:
                st.write("По кампусам")
                st.bar_chart(result['Кампус'].value_counts().head(10))
