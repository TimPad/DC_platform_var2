"""
Модуль 5: Аналитика курсов
Загрузка данных курсов в Supabase
"""

import streamlit as st
import pandas as pd
import time
from io import StringIO
from utils import icon, apply_custom_css, get_supabase_client

# Применяем кастомные стили
apply_custom_css()

# Заголовок страницы
st.markdown(
    f'<h1>{icon("line-chart", 32)} Аналитика курсов</h1>',
    unsafe_allow_html=True
)

st.markdown("""
Автоматическая обработка и загрузка аналитики курсов в Supabase.

**Режим работы:**
- **Обработать курсы** → обновляет только таблицы курсов (course_cg, course_python, course_analysis)

**Что делает инструмент:**
- Рассчитывает процент завершения курсов
- Фильтрует данные по корпоративной почте
- Загружает данные в отдельные таблицы Supabase
- Использует UPSERT для обновления существующих записей
""")

def upload_course_data_to_supabase(supabase, course_data, course_name):
    """Загрузка данных одного курса в соответствующую таблицу"""
    try:
        table_mapping = {'ЦГ': 'course_cg', 'Питон': 'course_python', 'Андан': 'course_analysis'}
        table_name = table_mapping.get(course_name)
        if not table_name:
            st.error(f"Неизвестный курс: {course_name}")
            return False
            
        st.info(f"Загрузка курса {course_name} в {table_name}...")
        if course_data is None or course_data.empty:
            st.warning(f"Нет данных для курса {course_name}")
            return True

        records_for_upsert = []
        processed_emails = set()
        
        for _, row in course_data.iterrows():
            email = str(row.get('Корпоративная почта', '')).strip().lower()
            if not email or '@edu.hse.ru' not in email:
                continue
            if email in processed_emails:
                continue
                
            processed_emails.add(email)
            
            percent_col = f'Процент_{course_name}'
            progress_value = None
            if percent_col in row and pd.notna(row[percent_col]) and row[percent_col] != '':
                try:
                    progress_value = float(row[percent_col])
                except (ValueError, TypeError):
                    progress_value = None
            
            records_for_upsert.append({
                'корпоративная_почта': email,
                'процент_завершения': progress_value
            })
        
        if not records_for_upsert:
            st.info(f"Нет записей для курса {course_name}")
            return True

        batch_size = 200
        total_processed = 0
        for i in range(0, len(records_for_upsert), batch_size):
            batch = records_for_upsert[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            try:
                supabase.table(table_name).upsert(batch, on_conflict='корпоративная_почта').execute()
                total_processed += len(batch)
                st.success(f"Курс {course_name} - батч {batch_num}: {len(batch)} записей")
            except Exception as e:
                st.error(f"Ошибка загрузки курса {course_name}, батч {batch_num}: {e}")
                return False

        st.success(f"Курс {course_name}: {total_processed} записей загружено")
        return True
    except Exception as e:
        st.error(f"Ошибка загрузки курса {course_name}: {e}")
        return False

def extract_course_data(uploaded_file, course_name):
    """Извлечение данных курса из файла"""
    try:
        file_name = uploaded_file.name.lower()
        if file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        elif file_name.endswith('.csv'):
            content = uploaded_file.getvalue()
            try:
                df = pd.read_csv(StringIO(content.decode('utf-16')), sep='\t')
            except (UnicodeDecodeError, pd.errors.ParserError):
                try:
                    df = pd.read_csv(StringIO(content.decode('utf-8')))
                except UnicodeDecodeError:
                    df = pd.read_csv(StringIO(content.decode('cp1251')))
        else:
            st.error(f"Неподдерживаемый формат файла для курса {course_name}")
            return None

        email_column = None
        possible_email_names = ['Адрес электронной почты', 'Корпоративная почта', 'Email', 'Почта', 'E-mail']
        for col_name in possible_email_names:
            if col_name in df.columns:
                email_column = col_name
                break
        if email_column is None:
            st.error(f"Столбец с email не найден в файле {course_name}")
            return None

        cg_excluded_keywords = [
            'take away', 'шпаргалка', 'консультация', 'общая информация', 'промо-ролик',
            'поддержка студентов', 'пояснение', 'случайный вариант для студентов с овз',
            'материалы по модулю', 'копия', 'демонстрационный вариант', 'спецификация',
            'демо-версия', 'правила проведения независимого экзамена',
            'порядок организации и проведения независимых экзаменов',
            'интерактивный тренажер правил нэ', 'пересдачи в сентябре', 'незрячих и слабовидящих',
            'проекты с использование tei', 'тренировочный тест', 'ключевые принципы tei',
            'базовые возможности tie', 'специальные модули tei', 'будут идентичными',
            'опрос', 'тест по модулю', 'анкета', 'user information', 'страна', 'user_id', 'данные о пользователе'
        ]

        completed_columns = []
        timestamp_columns = []

        for col in df.columns:
            if col not in ['Unnamed: 0', email_column, 'Данные о пользователе', 'User information', 'Страна']:
                if course_name == 'ЦГ':
                    should_exclude = False
                    col_str = str(col).strip().lower()
                    for excluded_keyword in cg_excluded_keywords:
                        if excluded_keyword.lower() in col_str:
                            should_exclude = True
                            break
                    if should_exclude:
                        continue

                if not col.startswith('Unnamed:') and len(str(col).strip()) > 0:
                    sample_values = df[col].dropna().astype(str).head(100)
                    if any('Выполнено' in str(val) or 'выполнено' in str(val).lower() for val in sample_values):
                        if not all(str(val) == 'Не выполнено' for val in sample_values if pd.notna(val)):
                            completed_columns.append(col)
                elif col.startswith('Unnamed:') and col != 'Unnamed: 0':
                    sample_values = df[col].dropna().astype(str).head(20)
                    for val in sample_values:
                        val_str = str(val).strip()
                        if any(pattern in val_str for pattern in ['2020', '2021', '2022', '2023', '2024']) and ':' in val_str:
                            timestamp_columns.append(col)
                            break

        if timestamp_columns:
            completion_data = []
            for idx, row in df.iterrows():
                email_val = row[email_column]
                if pd.isna(email_val) or '@edu.hse.ru' not in str(email_val).lower():
                    continue
                total_tasks = len(timestamp_columns)
                completed_tasks = 0
                for col in timestamp_columns:
                    cell_val = row[col]
                    val_str = str(cell_val).strip() if not pd.isna(cell_val) else ''
                    if val_str and val_str != 'nan' and val_str != '':
                        if any(pattern in val_str for pattern in ['2020', '2021', '2022', '2023', '2024']) and ':' in val_str:
                            completed_tasks += 1
                percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                completion_data.append({'email': str(email_val).lower().strip(), 'percentage': percentage})
            if completion_data:
                result_df = pd.DataFrame(completion_data)
                result_df.columns = ['Корпоративная почта', f'Процент_{course_name}']
                st.success(f"Рассчитан процент завершения для {len(result_df)} студентов курса {course_name}")
                return result_df

        elif completed_columns:
            completion_data = []
            for idx, row in df.iterrows():
                email_val = row[email_column]
                if pd.isna(email_val) or '@edu.hse.ru' not in str(email_val).lower():
                    continue
                total_tasks = 0
                completed_tasks = 0
                for col in completed_columns:
                    cell_val = row[col]
                    val = str(cell_val).strip() if not pd.isna(cell_val) else ''
                    if val and val != 'nan':
                        total_tasks += 1
                        if 'Выполнено' in val or 'выполнено' in val.lower():
                            completed_tasks += 1
                percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                completion_data.append({'email': str(email_val).lower().strip(), 'percentage': percentage})
            if completion_data:
                result_df = pd.DataFrame(completion_data)
                result_df.columns = ['Корпоративная почта', f'Процент_{course_name}']
                st.success(f"Рассчитан процент завершения для {len(result_df)} студентов курса {course_name}")
                return result_df

        st.warning(f"Не найдено данных о завершении для курса {course_name}")
        return None
    except Exception as e:
        st.error(f"Ошибка обработки данных курса {course_name}: {e}")
        return None

# Проверка подключения
try:
    supabase = get_supabase_client()
    st.success("Подключение к Supabase установлено")
except Exception as e:
    st.error(f"Ошибка подключения к Supabase: {str(e)}")
    st.stop()

st.markdown("---")

# Загрузка файлов
st.subheader("Загрузка файлов курсов")

col1, col2, col3 = st.columns(3)
with col1:
    course_cg_file = st.file_uploader("Курс ЦГ", type=['csv', 'xlsx', 'xls'], key="cg_file")
with col2:
    course_python_file = st.file_uploader("Курс Python", type=['csv', 'xlsx', 'xls'], key="python_file")
with col3:
    course_analysis_file = st.file_uploader("Курс Анализ данных", type=['csv', 'xlsx', 'xls'], key="analysis_file")

# Статус загрузки
files_uploaded = all([
    course_cg_file is not None,
    course_python_file is not None,
    course_analysis_file is not None
])

if not files_uploaded:
    st.info("📝 Пожалуйста, загрузите все три файла курсов:")
    file_status = {
        "Курс ЦГ": "" if course_cg_file else "",
        "Курс Python": "" if course_python_file else "",
        "Курс Анализ данных": "" if course_analysis_file else ""
    }
    status_df = pd.DataFrame([{"Файл": k, "Статус": v} for k, v in file_status.items()])
    st.table(status_df)
else:
    st.success("Все файлы загружены! Готово к обработке.")
    
    if st.button("Обработать курсы", type="primary", key="process_courses_btn"):
        with st.spinner("Обработка данных..."):
            try:
                from logic.student_management import load_students_from_supabase
                st.info("Получение списка зарегистрированных студентов из базы...")
                all_students_df = load_students_from_supabase()
                enrolled_emails = set(all_students_df['Адрес электронной почты'].str.lower().str.strip())
                st.success(f"Загружено {len(enrolled_emails)} уникальных студентов из базы.")

                st.info("Обработка файлов курсов...")
                course_names = ['ЦГ', 'Питон', 'Андан']
                course_files = [course_cg_file, course_python_file, course_analysis_file]
                course_data_list = []
                
                for course_file, course_name in zip(course_files, course_names):
                    course_data = extract_course_data(course_file, course_name)
                    if course_data is None:
                        st.error(f"Ошибка обработки курса {course_name}")
                        st.stop()
                    
                    # Отфильтровать только тех студентов, чья почта есть в загруженном списке
                    initial_count = len(course_data)
                    course_data = course_data[course_data['Корпоративная почта'].str.lower().str.strip().isin(enrolled_emails)]
                    filtered_count = len(course_data)
                    
                    st.success(f"Обработан курс {course_name}: {filtered_count} записей (отброшено {initial_count - filtered_count} незарегистрированных)")
                    course_data_list.append(course_data)
                
                # Загрузка в Supabase
                st.info("Обновление данных курсов в Supabase...")
                success_count = 0
                for course_data, course_name in zip(course_data_list, course_names):
                    if upload_course_data_to_supabase(supabase, course_data, course_name):
                        success_count += 1
                
                if success_count == len(course_names):
                    st.success(f"Все {success_count} курса успешно загружены!")
                    
                    # Сводная статистика
                    st.subheader("Сводная статистика")
                    summary_data = []
                    for course_data, course_name in zip(course_data_list, course_names):
                        col_name = f'Процент_{course_name}'
                        if col_name in course_data.columns:
                            course_stats = course_data[col_name].dropna()
                            if len(course_stats) > 0:
                                avg_completion = course_stats.mean()
                                students_100 = len(course_stats[course_stats == 100.0])
                                students_0 = len(course_stats[course_stats == 0.0])
                                total_students = len(course_stats)
                                summary_data.append({
                                    'Курс': course_name,
                                    'Студентов всего': total_students,
                                    'Средний %': f"{avg_completion:.1f}%",
                                    '100%': students_100,
                                    '0%': students_0
                                })
                    
                    if summary_data:
                        summary_df = pd.DataFrame(summary_data)
                        st.table(summary_df)
                    
                    st.balloons()
                else:
                    st.error(f"Загружено только {success_count} из {len(course_names)} курсов")
            
            except Exception as e:
                st.error(f"Ошибка при обработке: {str(e)}")
                st.exception(e)
