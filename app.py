"""
DataCulture Unified Platform
Объединённое приложение для инструментов Data Culture @ HSE University
Автор: Тимошка

Версия с использованием st.navigation (Page-based navigation)
"""

import streamlit as st
from utils import icon, apply_custom_css, LOGO_URL

# =============================================================================
# КОНФИГУРАЦИЯ ПРИЛОЖЕНИЯ
# =============================================================================

st.set_page_config(
    page_title="DataCulture Platform",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Применяем кастомные стили
apply_custom_css()

# =============================================================================
# ОПРЕДЕЛЕНИЕ СТРАНИЦ
# =============================================================================

# Создаем объекты Page для каждого модуля
grade_recalculation_page = st.Page(
    "pages/1_grade_recalculation.py",
    title="Перезачет оценок",
    icon=":material/analytics:",
    default=True
)

html_card_generator_page = st.Page(
    "pages/2_html_card_generator.py",
    title="Генератор HTML-карточек",
    icon=":material/mail:"
)

certificate_generator_page = st.Page(
    "pages/3_certificate_generator.py",
    title="Генератор сертификатов",
    icon=":material/workspace_premium:"
)

external_assessment_page = st.Page(
    "pages/4_external_assessment.py",
    title="Обработка пересдач внешней оценки",
    icon=":material/assignment:"
)

course_analytics_page = st.Page(
    "pages/5_course_analytics.py",
    title="Аналитика курсов",
    icon=":material/book:"
)

student_list_update_page = st.Page(
    "pages/6_student_list_update.py",
    title="Списки студентов",
    icon=":material/group:"
)

# =============================================================================
# НАСТРОЙКА НАВИГАЦИИ
# =============================================================================

pg = st.navigation(
    {
        "Основные модули": [
            grade_recalculation_page,
            html_card_generator_page,
            certificate_generator_page,
        ],
        "Интеграция БД": [
            external_assessment_page,
            course_analytics_page,
            student_list_update_page,
        ]
    }
)

# =============================================================================
# САЙДБАР: ЛОГОТИП И ИНФОРМАЦИЯ
# =============================================================================

with st.sidebar:
    # Логотип и заголовок (уменьшенный, сверху)
    st.markdown(
        f"""
        <div style="text-align: center; padding: 1rem 0.5rem 0.5rem 0.5rem;">
            <img src="{LOGO_URL}" alt="DataCulture Logo" style="max-width: 100px; margin-bottom: 0.5rem;">
            <div style="color: #e0e0e6; font-size: 0.95rem; font-weight: 600; text-align: center; margin-bottom: 0.15rem;">DataCulture Platform</div>
            <div style="color: #a1a1aa; font-size: 0.75rem; text-align: center;">HSE University</div>
        </div>
        <hr class="sidebar-divider">
        """,
        unsafe_allow_html=True
    )
    
   
    
    # Статистика и статус
    with st.expander("Статистика", expanded=False):
        try:
            from utils import get_supabase_client
            supabase = get_supabase_client()
            
            # Проверка подключения
            students_response = supabase.table('students').select('*', count='exact').limit(1).execute()
            students_count = students_response.count if hasattr(students_response, 'count') else 0
            
            peresdachi_response = supabase.table('peresdachi').select('*', count='exact').limit(1).execute()
            peresdachi_count = peresdachi_response.count if hasattr(peresdachi_response, 'count') else 0
            
            st.markdown(
                f"""
                <div style='font-size: 0.8rem; line-height: 1.8;'>
                <div style='display: flex; justify-content: space-between; align-items: center; padding: 0.25rem 0;'>
                    <span style='color: var(--apple-text-secondary);'>{icon('users', 16)} Студенты:</span>
                    <strong style='color: var(--apple-accent);'>{students_count:,}</strong>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center; padding: 0.25rem 0;'>
                    <span style='color: var(--apple-text-secondary);'>{icon('file-edit', 16)} Пересдачи:</span>
                    <strong style='color: var(--apple-accent);'>{peresdachi_count:,}</strong>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center; padding: 0.25rem 0; border-top: 1px solid var(--apple-divider); margin-top: 0.5rem; padding-top: 0.5rem;'>
                    <span style='color: var(--apple-text-secondary);'>{icon('check-circle-2', 16)} Статус БД:</span>
                    <strong style='color: #16a34a;'>Активна</strong>
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.markdown(
                f"""
                <div style='color: #ef4444; font-size: 0.85rem;'>
                    {icon('x-circle', 16)}
                    Ошибка подключения
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    
    # Информация о платформе
    st.markdown(
        f"""
        <div style='color: var(--apple-text-secondary); font-size: 0.75rem; padding: 0.5rem 0; text-align: center;'>
        <strong style='color: var(--apple-text-primary);'>DataCulture Platform v1.0</strong><br>
        {icon('rocket', 14)} Powered by Streamlit + Supabase<br>
        {icon('heart-handshake', 14)} Created by Тимошка
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# ЗАПУСК НАВИГАЦИИ
# =============================================================================

pg.run()

# Футер
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666;'>
        <p>Culture Platform v1.0 | Created with {icon('heart-handshake', 16)} by Тимошка {icon('rocket', 16)}</p>
    </div>
    """, 
    unsafe_allow_html=True
)
