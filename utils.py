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

HTML_TEMPLATE_DATALENS = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #f5f7fa;
      padding: 40px 20px;
      margin: 0;
    }}
    .card {{
      max-width: 860px;
      margin: 0 auto;
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.08);
      border: 1px solid #e5ebf8;
      overflow: hidden;
    }}
    .header {{
      background: linear-gradient(135deg, #0066ff, #0050cc);
      color: white;
      padding: 32px 40px;
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .header img {{
      height: 42px;
    }}
    .header h1 {{
      margin: 0;
      font-size: 28px;
      font-weight: 700;
    }}
    .body {{
      padding: 40px 40px 48px;
      color: #1a1a1a;
      line-height: 1.65;
    }}
    .section {{
      background: #fff;
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 24px;
      border: 1px solid #e5ebf8;
    }}
    .section h2 {{
      font-size: 24px;
      font-weight: 700;
      margin-top: 0;
      margin-bottom: 16px;
      color: #000;
    }}
    .section p {{
      margin: 0 0 16px 0;
    }}
    .section ul {{
      padding-left: 24px;
      margin: 16px 0;
    }}
    .section li {{
      margin-bottom: 10px;
    }}
    .cta-button {{
      display: inline-block;
      background: #0066ff;
      color: white;
      font-weight: 600;
      padding: 14px 32px;
      border-radius: 8px;
      text-decoration: none;
      margin-top: 32px;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <img src="{{logo_url}}" alt="Yandex DataLens">
      <h1>{{title}}</h1>
    </div>
    <div class="body">
      <!-- Основной контент будет вставлен здесь -->
      {{{body_content}}}
      
      <!-- Кнопка CTA -->
      <a href="{{button_url}}" class="cta-button">{{button_text}}</a>
    </div>
  </div>
</body>
</html>"""

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
        "user": '<svg width="{s}" height="{s}" viewBox="0 0 26 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.05129 19.2084C4.81816 17.7564 6.70745 14.3141 7.05129 12.7084C7.23239 11.8627 7.23769 11.514 7.05129 10.7084C6.87501 9.94655 7.02087 9.91049 6.55129 9.34837C6.0817 8.78626 5.98105 8.66259 5.05129 8.66259C4.8936 8.66259 4.52077 8.73005 4.05129 8.98862C3.58181 9.24719 3.16629 10.7316 3.45814 10.8661C3.94604 11.0909 3.72632 11.3825 3.55098 11.7084C3.44211 11.9108 2.72288 12.6311 2.49274 12.3388C2.36513 12.1767 2.15988 11.0717 2.38738 11.1584C2.69298 11.2748 2.38666 12.5028 2.07849 12.6086M2.07849 12.6086C1.7838 12.7098 2.22304 12.4965 2.07849 12.6086ZM2.07849 12.6086C1.63272 12.9544 1.32848 11.6652 1.65505 11.1584C1.99552 10.63 0.922155 12.2426 0.550883 12.1365C0.11823 12.0128 0.752985 11.4844 0.752973 11.1584C0.752966 10.9623 1.21274 9.74185 1.70984 8.66259C1.89433 8.26205 1.94203 7.55848 2.14294 7.1699C2.4006 6.67158 2.66601 5.9521 3.10541 5.7084C3.45001 5.51729 3.56111 5.57873 5.05129 6.1106C5.68126 6.33544 5.57401 6.24666 6.10223 6.54905C6.98597 7.05495 7.60075 7.42594 8.80866 7.42594C9.48066 7.42594 9.28773 7.43617 9.5861 6.30172C9.85815 5.26734 9.96397 3.6776 9.12982 3.30003C8.81296 3.1566 8.12652 3.30003 7.87787 3.62606C7.43643 4.20486 7.37982 4.35914 7.29792 5.14376C7.24664 5.63504 7.42576 5.84078 7.73058 6.1106C8.0354 6.38041 9.28389 6.40969 10.0872 5.85202C10.5933 5.5007 10.5217 4.84612 11.1458 4.57041C11.6766 4.33594 11.5001 4.35874 12.0509 4.2084C13.3244 3.86083 12.6072 2.40964 13.8644 2.6907C14.4847 2.82937 14.8615 2.86245 15.3804 3.30003C16.0248 3.84342 16.135 7.2676 15.3804 7.85247C14.9301 8.20146 12.7151 8.22985 12.2804 7.85247C11.8291 7.46062 12.0749 5.99036 12.3529 5.40543C12.6715 4.73488 14.9841 4.30797 15.5277 4.7084C16.1076 5.13561 15.8498 4.94112 16.3193 4.95264C16.744 4.96307 17.2112 5.13295 17.5253 4.57041C17.8014 4.07575 19.5549 3.38521 20.0402 3.54792C20.5097 3.70531 20.9235 5.2291 20.5779 5.59654C20.2064 5.99144 18.7753 6.6538 18.376 6.30172C17.7641 5.76218 16.423 4.86607 16.8648 4.11875C17.2419 3.48068 17.6012 2.9065 18.2456 2.91358C18.8808 2.92056 21.2577 1.97944 21.5115 2.6907C21.9165 3.82617 21.2823 9.07868 21.3571 9.87791C21.5781 12.2388 25.5578 11.949 24.4754 13.7441C22.8553 16.431 23.893 14.5681 23.0513 16.2084C22.9665 16.3736 22.1724 17.5813 22.0513 17.7084C21.7977 17.9745 21.1904 16.9386 21.0513 17.2084C20.9122 17.4782 21.1818 18.3008 21.0513 18.7084C20.9208 19.116 20.5513 19.2084 20.0513 18.7084C19.6608 18.318 19.7521 17.8767 19.8082 17.2084C19.9419 15.6169 21.5976 14.6387 21.3572 13.3843C21.256 12.856 20.3827 13.1297 20.0513 13.2084C19.4871 13.3424 19.309 13.4611 19.0513 13.7084C18.5012 14.2363 18.3169 14.8121 18.05 15.5766C17.4689 17.2407 17.3319 19.5564 17.3319 19.5564M13.8719 19.5564L14.2625 16.847L17.9211 11.1584C17.9211 11.1584 16.9177 10.2863 15.3804 9.94655C14.9417 9.84961 13.3091 9.34837 13.3091 9.34837C13.3091 9.34837 13.7104 9.24025 14.1652 9.34837C15.0214 9.55188 14.8672 9.55094 15.5277 9.6744C16.4298 9.84303 17.9211 10.6525 17.9211 10.6525V8.98862C17.9211 8.98862 22.8822 8.09064 24.0513 7.7084C25.2204 7.32617 19.315 7.09992 18.376 7.09992C17.437 7.09992 17.1628 6.63496 16.6231 5.27867C16.3594 4.61581 16.4333 4.63284 16.4298 3.89587C16.4209 2.0154 17.5253 0.208405 17.5253 0.208405" stroke="currentColor" stroke-width="0.9"/></svg>',
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
