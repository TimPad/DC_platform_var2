"""
DataCulture Platform - Shared Utilities
Общие функции, стили и константы для всех модулей
"""

import streamlit as st
from supabase import create_client, Client
from openai import OpenAI

# =============================================================================
# КОНСТАНТЫ
# =============================================================================

LOGO_URL = "https://raw.githubusercontent.com/TimPad/html/main/DC_green.svg"

HTML_EXAMPLE = f"""<div style="font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif; max-width: 860px; margin: 40px auto; background: #ffffff; border-radius: 16px; box-shadow: 0 4px 14px rgba(0,0,0,0.08); border: 1px solid #e5ebf8; overflow: hidden;">
    <div style="background: #00256c; color: white; padding: 28px 32px; text-align: center;">
        <img src="{LOGO_URL}" alt="Логотип Data Culture" style="height: 48px; margin-bottom: 16px;">
        <p><span style="font-size: 1.6em; font-weight: 700;">ЗАГОЛОВОК ОБЪЯВЛЕНИЯ</span></p>
        <p style="margin-top: 8px; line-height: 1.5;">Краткое введение или контекст.</p>
    </div>
    <div style="padding: 28px 32px; color: #111827; line-height: 1.65;">
        <p>Основной текст объявления...</p>
        <h3 style="color: #00256c;">Подзаголовок</h3>
        <ul style="margin: 12px 0 22px 22px;">
            <li>Пункт списка</li>
        </ul>
        <div style="background: #f4f6fb; border-radius: 10px; padding: 16px 20px; margin: 16px 0;">
            <p>Информационный блок</p>
        </div>
        <div style="background: #fff8e1; border-left: 4px solid #f59e0b; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-weight: 600; color: #92400e;">⚠️ Внимание! Важное уточнение.</p>
        </div>
        <div style="background: #f0fdf4; border-left: 4px solid #16a34a; padding: 16px 20px; border-radius: 8px;">
            <p style="margin: 4px 0 0;"><strong>Удачи!</strong> 🚀</p>
        </div>
    </div>
</div>"""

SYSTEM_MESSAGE = (
    "Вы — эксперт по оформлению официальных рассылок НИУ ВШЭ. "
    "Ваша задача — преобразовать входной текст объявления в HTML-карточку, строго следуя фирменному стилю. "
    "В шапке обязательно должен быть логотип по ссылке: " + LOGO_URL + ". "
    "Используйте структуру и CSS-стили из приведённого ниже примера. "
    "Не добавляйте пояснений, комментариев или лишних тегов. "
    "Верните ТОЛЬКО корректный JSON в формате: {\"type\": \"HTML\", \"content\": \"<div>...</div>\"}.\n\n"
    "Пример корректного вывода:\n"
    + str({"type": "HTML", "content": HTML_EXAMPLE})
)

# =============================================================================
# LUCIDE SVG ИКОНКИ
# =============================================================================

def icon(name: str, size: int = 18) -> str:
    """
    Возвращает встроенный SVG Lucide как HTML
    
    Args:
        name: название иконки из Lucide
        size: размер иконки в пикселях
    
    Returns:
        HTML строка с SVG иконкой
    """
    icons = {
        "bar-chart-3": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>',
        "rocket": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M4.5 16.5c-1.5 1.5-2 3.3-1.4 4.9l1-1 1.4 1.4 1-1c-1.6-.6-3.4 0-4.9-1.4z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>',
        "graduation-cap": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
        "scroll-text": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M8 21h12a2 2 0 0 0 2-2v-2H10v2a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v3h4"/><path d="M19 17V5a2 2 0 0 0-2-2H4"/><path d="M15 8h-5"/><path d="M15 12h-5"/></svg>',
        "file-edit": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M4 13.5V4a2 2 0 0 1 2-2h8.5L20 7.5V20a2 2 0 0 1-2 2h-5.5"/><polyline points="14 2 14 8 20 8"/><path d="M10.42 12.61a2.1 2.1 0 1 1 2.97 2.97L7.95 21 4 22l.99-3.95 5.43-5.44Z"/></svg>',
        "line-chart": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
        "user": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
        "users": '<svg width="{s}" height="{s}" viewBox="0 0 25 21" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1.26019 19.8711C1.26019 19.8711 2.59507 18.2414 3.29871 17.0493C4.16057 15.5892 4.5792 14.6871 5.12141 13.0134C5.37066 12.2439 5.62139 11.8268 5.66443 11.001C5.70599 10.2035 5.83023 9.55073 5.36065 8.98862C4.89106 8.4265 4.88196 8.39278 3.9522 8.39278C3.79451 8.39278 3.46431 8.49396 2.99483 8.75253C2.52534 9.0111 2.10983 10.4955 2.40168 10.63C2.88958 10.8548 3.0649 11.5408 2.88957 11.8666C2.7807 12.069 2.50704 12.6311 2.2769 12.3388C2.14929 12.1767 1.94404 11.0717 2.17154 11.1584C2.47715 11.2748 2.17082 12.5028 1.86265 12.6086M1.86265 12.6086C1.56796 12.7098 2.00721 12.4965 1.86265 12.6086ZM1.86265 12.6086C1.41689 12.9544 1.11264 11.6652 1.43921 11.1584C1.77969 10.63 1.12007 12.2426 0.748794 12.1365C0.316142 12.0128 0.408086 11.2146 0.408074 10.8886C0.408066 10.6925 0.454086 9.47204 0.951188 8.39278C1.13568 7.99223 1.2383 7.27489 1.43921 6.88631C1.69687 6.38799 1.96228 5.66851 2.40168 5.42482C2.74628 5.2337 2.80366 5.15152 4.29384 5.68339C4.92381 5.90824 5.35818 6.24666 5.8864 6.54905C6.77013 7.05495 7.38491 7.42594 8.59282 7.42594C9.26482 7.42594 9.07189 7.43617 9.37026 6.30172C9.64231 5.26734 9.74813 3.6776 8.91398 3.30003C8.59712 3.1566 7.91068 3.30003 7.66203 3.62606C7.22059 4.20486 7.16398 4.35914 7.08208 5.14376C7.0308 5.63504 7.20992 5.84078 7.51474 6.1106C7.81956 6.38041 9.06805 6.40969 9.87136 5.85202C10.3774 5.5007 10.3059 4.84612 10.93 4.57041C11.4607 4.33594 11.6639 4.40595 12.2148 4.25562C13.4883 3.90805 12.7711 2.45686 14.0283 2.73792C14.6485 2.87659 14.6456 2.86245 15.1645 3.30003C15.8089 3.84342 16.1361 4.87368 15.3815 5.45855C14.9312 5.80754 14.2184 5.92586 13.7837 5.54848C13.3323 5.15664 13.294 4.73937 13.572 4.15444C13.8906 3.48389 14.7682 3.85519 15.3118 4.25562C15.8918 4.68283 15.634 4.94112 16.1035 4.95264C16.5281 4.96307 16.9954 4.58208 17.3094 4.01953C17.5856 3.52487 18.0392 3.46335 18.5246 3.62606C18.994 3.78345 19.3949 4.49526 19.0493 4.8627C18.6778 5.2576 17.9849 5.49585 17.5856 5.14376C16.9737 4.60422 16.8677 3.72133 17.3094 2.974C17.6866 2.33594 18.0459 2.04506 18.6903 2.05214C19.3255 2.05912 19.7989 2.26275 20.0527 2.974C20.4577 4.10947 19.5176 8.75265 19.5924 9.55188C19.8133 11.9128 25.342 11.949 24.2596 13.7441C22.6394 16.431 22.266 15.9037 21.4243 17.544C21.3395 17.7092 21.2242 17.8666 21.1031 17.9937C20.8496 18.2598 20.6347 17.3978 20.4956 17.6677C20.3565 17.9375 20.579 18.2943 20.4485 18.7019C20.318 19.1096 20.2334 19.1724 19.8778 19.1179C19.332 19.0343 19.4994 18.2123 19.5556 17.544C19.6892 15.9525 21.6647 14.9647 21.4243 13.7104C21.323 13.182 20.1355 13.3057 19.8041 13.3843C19.2399 13.5183 19.0401 13.6429 18.7823 13.8902C18.2322 14.4181 18.1011 14.8121 17.8341 15.5766C17.253 17.2407 17.1161 19.5564 17.1161 19.5564M13.7061 20.2084L14.0467 16.847L17.1345 10.6525C17.1345 10.6525 16.8491 10.2277 15.3118 9.888C14.8732 9.79106 13.0933 9.34837 13.0933 9.34837C13.0933 9.34837 13.4946 9.24025 13.9494 9.34837C14.8055 9.55188 14.6514 9.55094 15.3118 9.6744C16.214 9.84303 17.7053 10.6525 17.7053 10.6525V8.98862C17.7053 8.98862 20.7063 5.526 21.8754 5.14376C23.0445 4.76152 19.4635 6.07687 18.5246 6.07687C17.5856 6.07687 16.947 6.63496 16.4073 5.27867C16.1435 4.61581 16.2174 4.63284 16.214 3.89587C16.2051 2.0154 17.3094 0.208405 17.3094 0.208405" stroke="currentColor" stroke-width="0.8"/></svg>',
        "check-circle-2": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',
        "x-circle": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>',
        "link": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
        "heart-handshake": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M12 5 9.04 7.96a2.17 2.17 0 0 0 0 3.08v0c.82.82 2.13.85 3 .07l2.07-1.9a2.82 2.82 0 0 1 3.79 0l2.96 2.66"/><path d="m18 15-2-2"/><path d="m15 18-2-2"/></svg>',
        "zap": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
    }
    return icons.get(name, '').format(s=size)

# =============================================================================
# APPLE-INSPIRED DARK THEME STYLING
# =============================================================================

def apply_custom_css():
    """Применить кастомные стили Apple-inspired Dark Theme"""
    st.markdown("""
<style>
    /* Основные цвета */
    :root {
        --apple-bg-primary: #1e1e22;
        --apple-bg-secondary: #2a2a30;
        --apple-accent: #5A9DF8;
        --apple-text-primary: #e0e0e6;
        --apple-text-secondary: #a1a1aa;
        --apple-divider: rgba(255,255,255,0.08);
        --apple-shadow: rgba(0,0,0,0.3);
    }
    
    /* Глобальный фон */
    .stApp {
        background-color: var(--apple-bg-primary);
    }
    
    /* Сайдбар в стиле Apple */
    [data-testid="stSidebar"] {
        background-color: var(--apple-bg-secondary);
        padding-top: 2rem;
    }
    
    /* Карточки и контейнеры */
    div[data-testid="stExpander"] {
        background-color: var(--apple-bg-secondary);
        border: 1px solid var(--apple-divider);
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    
    /* Кнопки */
    .stButton > button {
        background-color: var(--apple-accent);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        letter-spacing: -0.01em;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(90, 157, 248, 0.25);
    }
    
    .stButton > button:hover {
        background-color: #4a8de0;
        box-shadow: 0 4px 12px rgba(90, 157, 248, 0.35);
        transform: translateY(-1px);
    }
    
    /* Заголовки */
    h1, h2, h3 {
        color: var(--apple-text-primary);
        font-weight: 600;
        letter-spacing: -0.03em;
    }
    
    /* Файловый загрузчик */
    [data-testid="stFileUploader"] {
        background-color: var(--apple-bg-secondary);
        border: 2px dashed var(--apple-divider);
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.2s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--apple-accent);
        background-color: rgba(90, 157, 248, 0.05);
    }
    
    /* Таблицы */
    .stDataFrame {
        background-color: var(--apple-bg-secondary);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px var(--apple-shadow);
    }
    
    /* Метрики */
    [data-testid="stMetricValue"] {
        color: var(--apple-text-primary);
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--apple-text-secondary);
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SUPABASE CLIENT
# =============================================================================

@st.cache_resource
def get_supabase_client() -> Client:
    """Получить клиент Supabase"""
    if "url" not in st.secrets or "key" not in st.secrets:
        raise ValueError("Supabase URL и KEY не найдены в secrets.toml")
    return create_client(st.secrets["url"], st.secrets["key"])

# =============================================================================
# NEBIUS AI CLIENT
# =============================================================================

@st.cache_resource
def get_nebius_client():
    """Получить клиент Nebius API"""
    if "NEBIUS_API_KEY" not in st.secrets:
        raise ValueError("NEBIUS_API_KEY не найден в secrets.")
    return OpenAI(
        base_url="https://api.studio.nebius.com/v1/",
        api_key=st.secrets["NEBIUS_API_KEY"]
    )
