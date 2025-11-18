"""
Модуль 4: Обработка пересдач внешней оценки
Supabase интеграция (финальная стабильная версия)
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
Автоматическая обработка пересдач из внешней системы оценивания с интеграцией Supabase.
**Требуется:** файл с оценками (до 1000 строк)  
**Что делает инструмент:**
- Очищает и преобразует данные
- Объединяет со списком студентов
- Приоритет оценок: `student_io` → файл
- Сохраняет в `peresdachi` через upsert (без дублирования)
""")

# === Универсальная загрузка с кэшем ===
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
    get_supabase_client().table('students').select('id', limit=1).execute()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения к Supabase: {e}")
    st.stop()

st.markdown("---")

# === Загрузка файла ===
grades_file = st.file_uploader(
    "Загрузите файл с оценками (xlsx)",
    type=['xlsx', 'xls'],
    help="Должны быть колонки: 'Адрес электронной почты' и 'Тест:... (Значение)'"
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

# === Только здесь мы читаем файл — после проверки, что он есть ===
try:
    grades_df = pd.read_excel(grades_file)
    st.success(f"Файл загружен: {len(grades_df)} строк × {len(grades_df.columns)} колонок")
except Exception as e:
    st.error(f"Не удалось прочитать файл: {e}")
    st.stop()

# Проверка колонок с тестами
test_cols = [col for col in grades_df.columns if 'Тест:' in col and '(Значение)' in col]
if not test_cols:
    st.error("Не найдено колонок вида 'Тест:... (Значение)'")
    st.stop()

# Предпросмотр
with st.expander("Предпросмотр загруженного файла", expanded=True):
    st.dataframe(grades_df.head(10), use_container_width=True)

st.metric("Найдено тестовых колонок", len(test_cols))

# === КНОПКА ОБРАБОТКИ ===
if st.button("Обработать данные и сохранить в Supabase", type="primary", use_container_width=True):
    with st.spinner("Идёт обработка..."):
        
        # 1. Студенты
        students_df = fetch_all('students', filters={'курс': 'Курс 4'})
        if students_df.empty:
            st.error("Нет студентов на Курсе 4")
            st.stop()
        st.info(f"Загружено студентов: {len(students_df)}")

        # 2. Маппинг дисциплин
        DISCIPLINE_MAPPING = {
            'Тест:Входное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Входной контроль',
            'Тест:Промежуточное тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Промежуточный контроль',
            'Тест:Итоговое тестирование (Значение)': 'Внешнее измерение цифровых компетенций. Итоговый контроль'
        }
        grades_df = grades_df.rename(columns=DISICIPLINE_MAPPING)

        # 3. Melt
        value_cols = [v for k, v in DISCIPLINE_MAPPING.items() if k in grades_df.columns]
        if not value_cols:
            st.error("Не удалось сопоставить ни одну колонку тестирования")
            st.stop()

        melted = pd.melt(
            grades_df,
            id_vars=['Адрес электронной почты'],
            value_vars=value_cols,
            var_name='Наименование дисциплины',
            value_name='Оценка'
        )

        # Очистка
        melted = melted[melted['Оценка'].notna() & (melted['Оценка'].astype(str).str.strip() != '')]
        melted['Оценка'] = melted['Оценка'].astype(str).str.replace('-', '').str.strip()
        melted['Адрес электронной почты'] = melted['Адрес электронной почты'].str.strip().str.lower()

        # 4. Присоединяем студентов
        students_df['Адрес электронной почты'] = students_df['корпоративная_почта'].astype(str).str.strip().str.lower()
        result = melted.merge(
            students_df[['Адрес электронной почты', 'фио', 'филиал_кампус', 'факультет',
                         'образовательная_программа', 'группа']],
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
            key_map = dict(zip(
                student_io['Адрес электронной почты'] + '|' + student_io['Наименование дисциплины'],
                student_io['Оценка']
            ))
            result_key = result['Адрес электронной почты'] + '|' + result['Наименование дисциплины']
            result['Оценка'] = result_key.map(key_map).fillna(result['Оценка'])

        # 6. Финальные поля
        result['ID дисциплины'] = ''
        result['Период аттестации'] = ''
        result['Курс'] = 'Курс 4'

        final_cols = ['ФИО', 'Адрес электронной почты', 'Кампус', 'Факультет',
                      'Образовательная программа', 'Группа', 'Курс', 'ID дисциплины',
                      'Наименование дисциплины', 'Период аттестации', 'Оценка']
        result = result[[c for c in final_cols if c in result.columns]]

        # === Сохранение ===
        with st.spinner("Сохранение в Supabase..."):
            records = [{k: (v if pd.notna(v) else None) for k, v in r.items()} 
                      for r in result.to_dict('records')]
            get_supabase_client().table('peresdachi') \
                .upsert(records, on_conflict=['Адрес электронной почты', 'Наименование дисциплины']) \
                .execute()
            st.success(f"Успешно сохранено/обновлено {len(result)} записей!")

        # === Результат ===
        st.balloons()
        st.subheader("Готово!")
        st.metric("Обработано записей", len(result))

        tab1, tab2 = st.tabs(["Данные", "Статистика"])
        with tab1:
            st.dataframe(result, use_container_width=True)
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                result.to_excel(writer, index=False, sheet_name='Пересдачи')
            buffer.seek(0)
            st.download_button(
                "Скачать результат",
                data=buffer.getvalue(),
                file_name=f"Пересдачи_{datetime.now():%d-%m-%Y}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("По дисциплинам")
                st.bar_chart(result['Наименование дисциплины'].value_counts())
            with col2:
                st.write("По кампусам")
                st.bar_chart(result['Кампус'].value_counts().head(10))
