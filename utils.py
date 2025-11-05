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
        "users": '<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle; margin-right:6px;"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
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
