"""
Модуль 4: Обработка пересдач внешней оценки
Supabase интеграция (оптимизированная версия)
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from utils import icon, apply_custom_css, get_supabase_client

# Стили и заголовок
apply_custom_css()
st.markdown(f'<h1>{icon("file-edit", 32)} Обработка пересдач внешней оценки</h1>', unsafe_allow_html=True)
st.markdown("""
Автоматическая обработка пересдач из внешней системы оценивания с интеграцией Supabase.

**Требуется:** файл с оценками (до 1000 строк)  
**Что делает инструмент:**
- Очищает и преобразует данные
- Объединяет со списком студентов из Supabase
- Приоритет оценок: `student_io` → файл
- Сохраняет в `peresdachi` через upsert (без дублирования)
- Скачивание всех обработанных данных
""")

# === Универсальная загрузка из Supabase с кэшем ===
@st.cache_data(ttl=3600, show_spinner="Загрузка данных из Supabase...")
def fetch_all(table: str, filters: dict = None, columns: str = "*"):
    supabase = get_supabase_client()
    query = supabase.table(table).select(columns, count='exact')
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
    get_supabase_client().table('students').select('id', count='exact').limit(1).execute()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения к Supabase: {e}")
    st.stop()

st.markdown("---")

# === Загрузка файла ===
st.subheader("Загрузка файла с оценками")
grades_file = st.file_uploader(
    "Выберите файл (xlsx)",
    type=['xlsx', 'xls'],
    help="Обязательные колонки: 'Адрес электронной почты' и колонки с 'Тест:... (Значение)'"
)

if not grades_file:
    st.info("Загрузите файл с оценками для начала работы")
    
    with st.expander("Текущее состояние таблицы peresdachi"):
        current = fetch_all('peresdachi')
        if current.empty:
            st.info("Таблица пуста")
        else:
            st.metric("Записей в peresdachi", len(current))
            st.dataframe(current.head(10), use_container_width=True)
    st.stop()

# === Чтение и валидация файла ===
try:
    grades_df = pd.read_excel(grades_file)
    st.success(f"Файл загружен: {len(grades_df)} строк")
except Exception as e:
    st.error(f"Не удалось прочитать файл: {e}")
    st.stop()

# Проверка обязательных колонок
required_base = ['Адрес электронной почты']
test_cols = [col for col in grades_df.columns if 'Тест:' in col and '(Значение)' in col]
if not test_cols:
    st.error("Не найдено колонок вида 'Тест:... (Значение)'")
    st.stop()

# === Предпросмотр ===
col1, col2 = st.columns(2)
with col1:
    with st.expander("Предпросмотр загруженного файла"):
        st.dataframe(grades_df.head(10), use_container_width=True)
with col2:
    st.metric("Строк в файле", len(grades_df))
    st.metric("Тестовых колонок найдено", len(test_cols))

# === Кнопка обработки (вне условий — не сбрасывается) ===
if st.button("Обработать данные и сохранить в Supabase", type="primary", use_container_width=True):
    with st.spinner("Обработка данных..."):
        
        # 1. Загрузка студентов
        students_df = fetch_all('students', filters={'курс': 'Курс 4'})
        if students_df.empty:
            st.error("Нет студентов на Курсе 4 в таблице `students`")
            st.stop()
        st.info(f"Загружено студентов: {len(students_df)}")

        # 2. Переименование колонок дисциплин
        DISCIPLINE_MAPPING = {
            'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
            'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
            'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
        }
        grades_df = grades_df.rename(columns=DISICIPLINE_MAPPING)

        # 3. Melt в длинный формат
        value_cols = [v for k, v in DISCIPLINE_MAPPING.items() if k in grades_df.columns]
        if not value_cols:
            st.error("Не удалось сопоставить колонки тестирований")
            st.stop()

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

        # 4. Присоединение данных студентов
        students_df['Адрес электронной почты'] = students_df['корпоративная_почта'].str.strip().str.lower()
        result = melted.merge(
            students_df[['Адрес электронной почты', 'фио', 'филиал_кампус', 'факультет', 
                         'образовательная_программа', 'группа']],
            on='Адрес электронной почты',
            how='left'
        )
        result = result.rename(columns={
            'фио': 'ФИО',
            'филиал_кампус': 'Кампус',
            'факультет': 'Факультет',
            'образовательная_программа': 'Образовательная программа',
            'группа': 'Группа'
        })

        # 5. Приоритет оценок из student_io
        student_io = fetch_all('student_io', columns='"Адрес электронной почты", "Наименование дисциплины", "Оценка"')
        if not student_io.empty:
            student_io['Адрес электронной почты'] = student_io['Адрес электронной почты'].astype(str).str.strip().str.lower()
            student_io['Наименование дисциплины'] = student_io['Наименование дисциплины'].astype(str).str.strip()
            student_io['Оценка'] = student_io['Оценка'].astype(str).str.strip()

            result['key'] = result['Адрес электронной почты'] + '|' + result['Наименование дисциплины']
            student_io['key'] = student_io['Адрес электронной почты'] + '|' + student_io['Наименование дисциплины']

            io_dict = dict(zip(student_io['key'], student_io['Оценка']))
            result['Оценка'] = result['key'].map(io_dict).fillna(result['Оценка'])
            result.drop('key', axis=1, inplace=True)
            st.success(f"Применены оценки из student_io для {len(io_dict)} совпадений")

        # 6. Финальные колонки
        result['ID дисциплины'] = ''
        result['Период аттестации'] = ''
        result['Курс'] = 'Курс 4'

        final_cols = ['ФИО', 'Адрес электронной почты', 'Кампус', 'Факультет',
                      'Образовательная программа', 'Группа', 'Курс', 'ID дисциплины',
                      'Наименование дисциплины', 'Период аттестации', 'Оценка']
        result = result[[c for c in final_cols if c in result.columns]]

        # === Сохранение в Supabase ===
        with st.spinner("Сохранение в Supabase (upsert)..."):
            supabase = get_supabase_client()
            records = result.to_dict('records')
            # Замена NaN на None для Supabase
            records = [{k: (v if pd.notna(v) else None) for k, v in r.items()} for r in records]

            response = supabase.table('peresdachi') \
                .upsert(records, on_conflict=['Адрес электронной почты', 'Наименование дисциплины']) \
                .execute()

            st.success(f"Успешно сохранено/обновлено {len(result)} записей в таблицу `peresdachi`")

        # === Результаты ===
        st.balloons()
        st.subheader("Готово! Результат обработки")
        st.metric("Обработано и сохранено записей", len(result))

        tab1, tab2 = st.tabs(["Все записи", "Статистика"])

        with tab1:
            st.dataframe(result, use_container_width=True)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                result.to_excel(writer, index=False, sheet_name='Пересдачи')
            output.seek(0)
            st.download_button(
                "Скачать результат (XLSX)",
                data=output.getvalue(),
                file_name=f"Пересдачи_{datetime.now():%d-%m-%Y}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("По дисциплинам:")
                st.bar_chart(result['Наименование дисциплины'].value_counts())
            with col2:
                st.write("По кампусам:")
                st.bar_chart(result['Кампус'].value_counts().head(10))
