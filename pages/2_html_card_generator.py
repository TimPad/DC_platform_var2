"""
Модуль 2: Генератор HTML-карточек
AI-генерация рассылок в фирменном стиле ВШЭ
"""

import streamlit as st
import json
import html
import base64
from datetime import datetime
import streamlit.components.v1 as components
from utils import icon, get_nebius_client
from constants import (
    LOGO_URL, LOGO_URL_BLACK, LOGO_URL_PNG, HTML_EXAMPLE, SYSTEM_MESSAGE,
    TEMPLATES, FCS_TEMPLATE, LOGO_URL_FCS,
    COVER_BRAND_COLORS, COVER_GRADIENT_ENDS, COVER_LOGOS,
    COVER_HTML_TEMPLATE, COVER_SYSTEM_MESSAGE,
)


def render_cover_logos(selected_keys: list, bg_color: str) -> str:
    is_dark = bg_color.upper() == "#102D69"
    svg_key = "svg_dark" if is_dark else "svg"
    parts = []
    for key in selected_keys:
        logo = COVER_LOGOS[key]
        h = logo["height"]
        svg = logo[svg_key].strip()
        svg = svg.replace('width=', 'data-orig-width=', 1).replace('height=', 'data-orig-height=', 1)
        if 'style="' in svg:
            svg = svg.replace('style="', f'style="height:{h}px;width:auto;display:block;', 1)
        else:
            svg = svg.replace('<svg ', f'<svg style="height:{h}px;width:auto;display:block;" ', 1)
        parts.append(f'<div class="logo-wrapper">{svg}</div>')
    return "\n      ".join(parts)


def cover_text_color(bg_hex: str) -> str:
    light_colors = {"#DFC7F2", "#DCFF05", "#FFFFFF"}
    return "#102D69" if bg_hex.upper() in light_colors else "#FFFFFF"


def cover_accent_colors(bg_hex: str) -> dict:
    if bg_hex.upper() in ("#DFC7F2", "#FFFFFF"):
        return {
            "accent_stripe": "linear-gradient(90deg, #102D69 0%, #DCFF05 100%)",
            "marker_color": "#102D69",
            "marker_shadow": "rgba(16, 45, 105, 0.2)",
            "badge_bg": "rgba(16, 45, 105, 0.15)",
            "badge_text_color": "#102D69",
            "badge_border": "rgba(16, 45, 105, 0.3)",
        }
    elif bg_hex.upper() == "#DCFF05":
        return {
            "accent_stripe": "linear-gradient(90deg, #102D69 0%, #DFC7F2 100%)",
            "marker_color": "#102D69",
            "marker_shadow": "rgba(16, 45, 105, 0.2)",
            "badge_bg": "rgba(16, 45, 105, 0.15)",
            "badge_text_color": "#102D69",
            "badge_border": "rgba(16, 45, 105, 0.3)",
        }
    else:
        return {
            "accent_stripe": "linear-gradient(90deg, #DCFF05 0%, #DFC7F2 100%)",
            "marker_color": "#DCFF05",
            "marker_shadow": "rgba(220, 255, 5, 0.2)",
            "badge_bg": "rgba(220, 255, 5, 0.15)",
            "badge_text_color": "#DCFF05",
            "badge_border": "rgba(220, 255, 5, 0.3)",
        }


def _build_png_component(cover_html: str) -> str:
    """Build a self-contained HTML component that renders the cover and downloads as PNG."""
    import json as _json
    escaped = _json.dumps(cover_html)
    return """
    <script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.13/dist/html-to-image.js"></script>
    <div style="text-align:center;">
        <button id="png-btn" onclick="downloadPNG()" style="
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1.5rem;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            width: 100%%;
            height: 38px;
            transition: all 0.2s ease;
        ">Скачать PNG</button>
    </div>
    <div id="offscreen-render" style="
        position: fixed;
        left: -9999px;
        top: 0;
        width: 800px;
        z-index: -1;
        background: transparent;
    "></div>
    <script>
    function downloadPNG() {
        var btn = document.getElementById('png-btn');
        btn.textContent = 'Генерация...';
        btn.disabled = true;
        var container = document.getElementById('offscreen-render');
        var coverHTML = %s;
        var parser = new DOMParser();
        var doc = parser.parseFromString(coverHTML, 'text/html');
        container.innerHTML = '';
        // Inject styles, scoped to this container
        var styles = doc.querySelectorAll('style');
        styles.forEach(function(s) {
            var clone = document.createElement('style');
            clone.textContent = s.textContent;
            container.appendChild(clone);
        });
        // Inject body content
        var wrapper = document.createElement('div');
        wrapper.innerHTML = doc.body.innerHTML;
        container.appendChild(wrapper);
        var target = container.querySelector('.course-cover') || wrapper;
        // Force fixed width for consistent rendering
        var targetWidth = 1600;
        var rect = target.getBoundingClientRect();
        var aspectRatio = rect.height / rect.width;
        var targetHeight = Math.round(targetWidth * aspectRatio);
        // Wait a tick for layout
        setTimeout(function() {
            htmlToImage.toPng(target, {
                pixelRatio: 2,
                cacheBust: true,
                width: rect.width,
                height: rect.height,
                style: {
                    transform: 'none'
                }
            }).then(function(dataUrl) {
                var link = document.createElement('a');
                link.download = 'cover.png';
                link.href = dataUrl;
                link.click();
                btn.textContent = 'Скачать PNG';
                btn.disabled = false;
                container.innerHTML = '';
            }).catch(function(err) {
                console.error(err);
                alert('Ошибка: ' + err);
                btn.textContent = 'Скачать PNG';
                btn.disabled = false;
            });
        }, 100);
    }
    </script>
    """ % escaped


# Заголовок страницы
st.markdown(
    f'<h1>{icon("graduation-cap", 32)} Генератор HTML-карточек</h1>',
    unsafe_allow_html=True
)

st.markdown("""
Создайте HTML-карточку рассылки в фирменном стиле ВШЭ с помощью искусственного интеллекта.

**Как использовать:**
1. Введите текст объявления или новости
2. Нажмите кнопку генерации
3. Получите готовый HTML-код и предпросмотр
""")

tab_cards, tab_covers = st.tabs(["📧 Карточки", "🖼 Обложки"])


def generate_hse_html(client, user_text: str, accent_color: str, allow_text_edits: bool, width_css: str, tone: str, template_key: str = "data_culture") -> str:
    """
    Генерация HTML-карточки через Nebius API
    
    Args:
        client: OpenAI клиент
        user_text: Текст объявления
        accent_color: HEX код основного цвета
        allow_text_edits: Разрешить ли ИИ менять текст пользователя
        width_css: CSS значение ширины (напр. "800px" или "100%")
        tone: Тональность текста
        template_key: Ключ шаблона из TEMPLATES
        
    Returns:
        HTML-код карточки
    """
    
    # Получаем шаблон из словаря TEMPLATES
    template_data = TEMPLATES.get(template_key, TEMPLATES["data_culture"])
    current_html_example = template_data["html"]

    # Определяем цвет текста для хедера (белый или черный)
    is_light_color = False
    if accent_color.upper() == "#DFFF00":
        is_light_color = True
    header_text_color = "#000000" if is_light_color else "#ffffff"
    
    # Выбираем логотип: Черный для Лайма (светлый фон), Зеленый (SVG) для Синего (темный фон)
    current_logo_url = LOGO_URL_BLACK if is_light_color else LOGO_URL
    
    # Определяем инструкции по тональности
    tone_instruction = ""
    if tone == "Неформальная":
        tone_instruction = "Тон: Неформальный, дружелюбный. Обращайтесь к читателю на 'вы' (но можно тепло). Допустимо использование 1-2 эмодзи для настроения. Стиль живого, но уважительного общения."
    elif tone == "Строгая":
        tone_instruction = "Тон: Строгий, официально-деловой. НИКАКИХ эмодзи. Максимально четко, лаконично, по делу. Избегайте 'воды' и фамильярности."
    elif tone == "Академическая":
        tone_instruction = "Тон: Академический, университетский. Используйте профессиональную лексику, высокий стиль. Сдержанно, интеллектуально, уважительно."

    # Инструкция по работе с текстом
    text_instruction = ""
    if allow_text_edits:
        text_instruction = (
            f"5. Контент: {tone_instruction} "
            "Текст пользователя МОЖНО и НУЖНО улучшать: исправлять ошибки, делать его более продающим и структурным. "
            "Разбивайте на смысловые блоки, добавлять эмоциональные подзаголовки (если позволяет тон). "
            "Если текст слишком короткий — разверните его, добавьте деталей, но не выдумывайте факты. "
            "Сделайте красивую структуру с буллитами."
        )
    else:
        text_instruction = (
            "5. Контент: Ваша задача — ОТФОРМАТИРОВАТЬ текст для удобства чтения, НО НЕ МЕНЯТЬ слова. "
            "ЗАПРЕЩЕНО переписывать, сокращать или добавлять от себя слова. "
            "ОБЯЗАТЕЛЬНО разбивайте длинный текст на параграфы <p>. "
            "ОБЯЗАТЕЛЬНО находите списки и оформляйте их через <ul> или <ol>. "
            "Используйте <strong> для выделения важных акцентов. "
            "Главное правило: улучшайте структуру (HTML), но сохраняйте оригинальные формулировки."
        )

    # Инструкции по цветам (Apple Style)
    color_instruction = f"4. Цвета: Основной цвет {accent_color}. "
    if is_light_color:
        color_instruction += (
            "ВАЖНО: Основной цвет (Лайм) используйте ТОЛЬКО для фонов (хедер). "
            "Для ВСЕХ заголовков и подзаголовков (h1, h2, h3) на белом фоне используйте ТЕМНО-СИНИЙ цвет (#001A57). "
            "КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО использовать лайм для текста на белом фоне — это нечитаемо. "
            "Текст на фоне лайма должен быть ЧЕРНЫМ (#000000)."
        )
    else:
        color_instruction += f"Текст заголовка {header_text_color}."

    # Используем ширину из аргумента
    table_width = width_css if width_css.endswith("%") else width_css.replace("px", "")
    
    pure_html_template = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Заголовок</title>
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, sans-serif;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#ffffff">
    <tr>
      <td align="center" style="padding: 20px 0;">
        <!-- Основной контейнер -->
        <table border="0" cellpadding="0" cellspacing="0" width="{table_width}" style="border-collapse: collapse; min-width: 320px; background-color: #ffffff;">
          
          <!-- Хедер -->
          <tr>
            <td align="center" bgcolor="{accent_color}" style="padding: 40px 30px; border-radius: 12px 12px 0 0;">
              <img src="{current_logo_url}" alt="Логотип" width="60" style="display: block; width: 60px; height: auto; margin-bottom: 20px; border: 0;" />
              <h1 style="color: {header_text_color}; font-size: 24px; line-height: 32px; font-weight: bold; margin: 0 0 10px 0; font-family: Arial, sans-serif;">
                ЗАГОЛОВОК
              </h1>
              <p style="color: {header_text_color}; font-size: 16px; line-height: 24px; margin: 0; opacity: 0.9; font-family: Arial, sans-serif;">
                Вводный текст
              </p>
            </td>
          </tr>

          <!-- Основной контент -->
          <tr>
            <td bgcolor="#F5F5F7" style="padding: 30px; border-radius: 0 0 12px 12px;">
              
              <!-- Блок контента 1 -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#ffffff" style="border-radius: 8px; border: 1px solid #e5e7eb; border-collapse: separate;">
                <tr>
                  <td style="padding: 25px; font-size: 16px; line-height: 24px; color: #333333; font-family: Arial, sans-serif;">
                    Основной текст...
                  </td>
                </tr>
              </table>
              <div style="height: 20px;"></div>

              <!-- Блок контента 2 (список) -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#ffffff" style="border-radius: 8px; border: 1px solid #e5e7eb; border-collapse: separate;">
                <tr>
                  <td style="padding: 25px; font-size: 16px; line-height: 24px; color: #333333; font-family: Arial, sans-serif;">
                    <h2 style="color: {accent_color}; font-size: 20px; font-weight: bold; margin: 0 0 15px 0;">Подзаголовок</h2>
                    <ul style="margin: 0; padding-left: 20px;">
                      <li style="margin-bottom: 10px;">Пункт 1</li>
                      <li>Пункт 2</li>
                    </ul>
                  </td>
                </tr>
              </table>
              <div style="height: 20px;"></div>

              <!-- Блок ВНИМАНИЕ (Yellow) -->
               <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#FFFBEB" style="border-radius: 8px; border-left: 4px solid #F59E0B; border-collapse: separate;">
                <tr>
                  <td style="padding: 20px; font-size: 16px; line-height: 24px; color: #92400E; font-family: Arial, sans-serif;">
                    <strong>Внимание:</strong> Текст предупреждения.
                  </td>
                </tr>
              </table>
              <div style="height: 20px;"></div>

              <!-- Блок КРИТИЧНО (Red) -->
               <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#FEF2F2" style="border-radius: 8px; border-left: 4px solid #EF4444; border-collapse: separate;">
                <tr>
                  <td style="padding: 20px; font-size: 16px; line-height: 24px; color: #991B1B; font-family: Arial, sans-serif;">
                    <strong>Важно:</strong> Критическая информация.
                  </td>
                </tr>
              </table>
              <div style="height: 20px;"></div>

              <!-- Футер / Подпись -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#ecfdf5" style="border-radius: 8px; border: 1px solid #86efac; border-collapse: separate;">
                <tr>
                  <td align="center" style="padding: 20px; font-size: 16px; line-height: 24px; color: #166534; font-family: Arial, sans-serif;">
                    <strong>Команда Data Culture</strong>
                  </td>
                </tr>
              </table>

            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    system_msg = (
        "Вы — эксперт по верстке HTML-писем (Email HTML Development). "
        "Ваша задача: Преобразовать текст в HTML-код, который идеально отображается в Outlook, Gmail и Apple Mail. "
        "Используйте предоставленный шаблон как жесткую основу.\n\n"
        "ШАБЛОН:\n"
        f"{pure_html_template}\n\n"
        "ТРЕБОВАНИЯ:\n"
        "1. Используйте ТОЛЬКО табличную верстку (table, tr, td) как в шаблоне.\n"
        "2. ВСЕ стили должны быть только inline (style=\"...\").\n"
        "3. Логотип: используйте ссылку " + current_logo_url + "\n"
        f"{color_instruction}\n"
        "5. АЛЕРТЫ: Для предупреждений используйте ЖЕЛТЫЙ блок (bg: #FFFBEB, text: #92400E, border: #F59E0B).\n"
        "6. АЛЕРТЫ: Для критической информации используйте КРАСНЫЙ блок (bg: #FEF2F2, text: #991B1B, border: #EF4444).\n"
        f"{text_instruction}\n"
        "8. Верните JSON: {\"type\": \"HTML\", \"content\": \"код...\"}."
    )
    
    # Специальная логика для шаблона ФКС
    current_year = datetime.now().year
    if template_key == "fcs":
        # Заменяем ширину в шаблоне ФКС, чтобы модель видела правильный размер
        current_html_example = current_html_example.replace('width="600"', f'width="{table_width}"')
        current_html_example = current_html_example.replace('max-width: 600px;', f'max-width: {width_css};')
        fcs_system_msg = (
            "Вы — эксперт по оформлению email-рассылок в фирменном стиле ФКС НИУ ВШЭ. "
            "Ваша задача — преобразовать входной текст в HTML-рассылку. "
            "ИСПОЛЬЗУЙТЕ ТОЧНУЮ СТРУКТУРУ из приведённого ниже шаблона!\n\n"
            "ТРЕБОВАНИЯ:\n"
            "1. СОХРАНЯЙТЕ структуру шаблона: header (тёмно-синий #102D69 с логотипом) → content (блоки информации, список, алерты) → CTA кнопка → footer.\n"
            "2. Логотип ФКС: используйте ссылку " + LOGO_URL_FCS + "\n"
            "3. Заголовок и подзаголовок в header адаптируйте под контент пользователя.\n"
            "4. Основной контент размещайте в блоках: primary_content, list с пунктами, warning и critical алерты.\n"
            "5. Используйте ТОЛЬКО табличную верстку (table, tr, td) и inline стили как в шаблоне.\n"
            "6. Акцентные цвета: #DCFF05 (лайм) и #DFC7F2 (лаванда) — как в шаблоне.\n"
            "7. НЕ добавляйте лишних комментариев — только HTML-код.\n"
            f"8. ТЕКУЩИЙ ГОД: {current_year}. Если в футере используется год (например, © год), ОБЯЗАТЕЛЬНО указывайте {current_year}. НЕ используйте 2024 или любой другой устаревший год.\n"
            f"9. Ширина карточки: {width_css}. Используйте width=\"{table_width}\" и max-width: {width_css} для основного контейнера.\n"
            f"{text_instruction}\n"
            "Верните ТОЛЬКО корректный JSON в формате: {\"type\": \"HTML\", \"content\": \"<!DOCTYPE html>...\"}.\n\n"
            "ШАБЛОН:\n"
            + str({"type": "HTML", "content": current_html_example})
        )
        system_msg = fcs_system_msg

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V4-Pro",
        messages=[
            {
                "role": "system", 
                "content": system_msg
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": user_text
                    }
                ]
            }
        ],
        timeout=120.0
    )

    raw_content = response.choices[0].message.content.strip()
    
    # Очистка от markdown блоков кода, если они есть
    if raw_content.startswith("```json"):
        raw_content = raw_content[7:]
    elif raw_content.startswith("```"):
        raw_content = raw_content[3:]
    
    if raw_content.endswith("```"):
        raw_content = raw_content[:-3]
        
    raw_content = raw_content.strip()

    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        raise ValueError(f"Модель вернула не-JSON. Ответ:\n{raw_content[:500]}")

    if not isinstance(parsed, dict):
        raise ValueError("Ответ не является объектом JSON.")

    if parsed.get("type") != "HTML":
        raise ValueError("Поле 'type' должно быть 'HTML'.")

    content = parsed.get("content")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Поле 'content' отсутствует или пустое.")

    return content.strip()

with tab_cards:
    # Инициализация выбранного шаблона в session_state
    if 'selected_template' not in st.session_state:
        st.session_state['selected_template'] = 'data_culture'

    @st.dialog("Предпросмотр макета", width="large")
    def show_template_preview(template_key):
        template_data = TEMPLATES[template_key]
        st.markdown(f"### {template_data['name']}")
        st.info(template_data['description'])
        safe_html = html.escape(template_data["html"], quote=True)
        components.html(
            f"""
            <div style="
                width: 100%;
                height: 600px;
                overflow: auto;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                background: white;
                padding: 0;
                box-sizing: border-box;
            ">
                <iframe
                    srcdoc="{safe_html}"
                    style="width: 100%; height: 100%; border: none; display: block;"
                    sandbox="allow-same-origin"
                ></iframe>
            </div>
            """,
            height=620
        )
        if st.button("Использовать этот макет", type="primary", use_container_width=True):
            st.session_state['selected_template'] = template_key
            st.rerun()

    st.markdown("### 🎨 Выберите макет")

    st.markdown("""
    <style>
        .template-card-header {
            height: 70px;
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .template-card-desc {
            height: 80px;
            font-size: 0.9rem;
            color: #6b7280;
            overflow: hidden;
            margin-bottom: 20px;
            line-height: 1.5;
        }
    </style>
    """, unsafe_allow_html=True)

    template_cols = st.columns(len(TEMPLATES))

    for idx, (template_key, template_data) in enumerate(TEMPLATES.items()):
        with template_cols[idx]:
            is_selected = st.session_state['selected_template'] == template_key
            with st.container(border=True):
                st.markdown(f"<div class='template-card-header'><h4>{template_data['name']}</h4></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='template-card-desc'>{template_data['description']}</div>", unsafe_allow_html=True)
                col_btn_1, col_btn_2 = st.columns([2, 1])
                with col_btn_1:
                    if st.button(
                        "Выбрать" if not is_selected else "Выбрано",
                        key=f"sel_{template_key}",
                        type="primary" if is_selected else "secondary",
                        use_container_width=True,
                        disabled=is_selected
                    ):
                        st.session_state['selected_template'] = template_key
                        st.rerun()
                with col_btn_2:
                    if st.button("Превью", key=f"prev_{template_key}", help="Предпросмотр макета", use_container_width=True):
                        show_template_preview(template_key)

    st.divider()

    # Настройки генерации
    col_settings_1, col_settings_2 = st.columns(2)

    with col_settings_1:
        allow_text_edits = st.checkbox(
            "Разрешить ИИ редактировать текст",
            value=True,
            help="Если включено, ИИ может улучшать формулировки и структуру. Если выключено, текст будет вставлен 'как есть'."
        )
        tone_option = st.selectbox(
            "Тональность текста",
            ["Неформальная", "Строгая", "Академическая"],
            help="Влияет на лексику и стиль изложения (работает, если разрешено редактирование текста)."
        )

    with col_settings_2:
        if st.session_state['selected_template'] == 'data_culture':
            accent_color = st.selectbox(
                "Акцентный цвет",
                ["#001A57", "#DFFF00"],
                format_func=lambda x: "🔵 Классический синий" if x == "#001A57" else "🟢 Лайм (#DFFF00)",
                help="Основной цвет заголовков и элементов дизайна"
            )
        else:
            accent_color = "#001A57"

        st.write("Ширина карточки")
        is_full_width = st.toggle("На всю ширину (100%)", value=False)
        if is_full_width:
            width_css = "100%"
        else:
            width_val = st.slider("Ширина (px)", min_value=600, max_value=1200, value=800, step=50, label_visibility="collapsed")
            width_css = f"{width_val}px"

    user_text = st.text_area(
        "Введите текст объявления:",
        height=250,
        placeholder="Вставьте сюда текст письма или новости..."
    )

    if st.button("Сформировать HTML", type="primary"):
        if not user_text.strip():
            st.warning("Введите текст для генерации")
        else:
            with st.spinner("Генерация карточки..."):
                try:
                    client = get_nebius_client()
                    html_code = generate_hse_html(client, user_text, accent_color, allow_text_edits, width_css, tone_option, st.session_state['selected_template'])
                    st.session_state['generated_html'] = html_code
                    st.success("Карточка успешно создана!")
                except Exception as e:
                    st.error(f"Ошибка: {e}")

    if 'generated_html' in st.session_state:
        html_code = st.session_state['generated_html']
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("HTML-код")
            with st.container(height=800):
                st.code(html_code, language="html")
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.download_button(
                    label="Скачать HTML",
                    data=html_code.encode("utf-8"),
                    file_name="hse_card.html",
                    mime="text/html",
                    use_container_width=True
                )
            with btn_col2:
                escaped_html = html.escape(html_code)
                components.html(
                    f"""
                    <style>
                    .copy-container {{
                        display: flex;
                        align-items: center;
                        height: 38px;
                        margin-top: -8px;
                    }}
                    .copy-btn {{
                        background-color: #5A9DF8;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 0.5rem 1rem;
                        font-size: 14px;
                        font-weight: 500;
                        cursor: pointer;
                        width: 100%;
                        transition: all 0.2s ease;
                        height: 38px;
                    }}
                    .copy-btn:hover {{
                        background-color: #4a8de0;
                    }}
                    </style>
                    <div class="copy-container">
                        <textarea id="html-content" style="position: absolute; left: -9999px;">{escaped_html}</textarea>
                        <button class="copy-btn" onclick="
                            var content = document.getElementById('html-content').value;
                            navigator.clipboard.writeText(content).then(function() {{
                                alert('HTML скопирован в буфер обмена!');
                            }}, function(err) {{
                                alert('Ошибка копирования: ' + err);
                            }});
                        ">Скопировать HTML</button>
                    </div>
                    """,
                    height=38
                )

        with col2:
            st.subheader("Предпросмотр")
            safe_html = html.escape(html_code, quote=True)
            preview_html = f"""
            <div style="
                width: 100%;
                height: 800px;
                overflow: auto;
                border: 1px solid #333;
                border-radius: 12px;
                background: white;
                padding: 0;
                box-sizing: border-box;
            ">
                <iframe
                    srcdoc="{safe_html}"
                    style="width: 100%; height: 100%; border: none; display: block;"
                    sandbox="allow-same-origin"
                ></iframe>
            </div>
            """
            components.html(preview_html, height=850, scrolling=False)
            st.info(
                "💡 **Совет:** Для рассылки через обычный почтовый клиент (Outlook, Apple Mail) "
                "рекомендуется копировать верстку прямо из окна предпросмотра (выделить всё -> копировать), "
                "а не использовать исходный HTML-код. После вставки в письмо текст можно будет отредактировать."
            )

# =============================================================================
# ВКЛАДКА: ОБЛОЖКИ
# =============================================================================

with tab_covers:
    st.markdown("### 🖼 Генератор обложек")
    st.markdown("Создайте обложку для курса или мероприятия в фирменном стиле.")

    cover_mode = st.radio(
        "Режим генерации",
        ["Шаблон", "ИИ-генерация"],
        horizontal=True,
        help="Шаблон — мгновенная подстановка в готовый макет. ИИ — генерация через DeepSeek."
    )

    st.markdown("#### Логотипы на обложке")
    logo_cols = st.columns(4)
    selected_logos = []
    with logo_cols[0]:
        if st.checkbox("ВШЭ", value=False, key="cover_logo_hse"):
            selected_logos.append("hse")
    with logo_cols[1]:
        if st.checkbox("ФКН", value=False, key="cover_logo_fcs"):
            selected_logos.append("fcs")
    with logo_cols[2]:
        if st.checkbox("Data Culture", value=False, key="cover_logo_dc"):
            selected_logos.append("dc")
    with logo_cols[3]:
        if st.checkbox("Яндекс", value=False, key="cover_logo_yandex"):
            selected_logos.append("yandex")

    st.markdown("#### Настройки")
    cover_col1, cover_col2 = st.columns(2)

    with cover_col1:
        color_names = list(COVER_BRAND_COLORS.keys())
        selected_color_name = st.selectbox(
            "Цвет фона",
            color_names,
            index=0,
            key="cover_bg_color"
        )
        bg_color = COVER_BRAND_COLORS[selected_color_name]

    with cover_col2:
        cover_title = st.text_input(
            "Текст заголовка (центр)",
            placeholder="Летняя школа по анализу данных ФКН",
            key="cover_title"
        )

    cover_col3, cover_col4 = st.columns(2)
    with cover_col3:
        cover_subtitle = st.text_input(
            "Текст подзаголовка (футер)",
            placeholder="практические занятия • эксперты из индустрии • сертификат",
            key="cover_subtitle"
        )
    with cover_col4:
        cover_badge = st.text_input(
            "Текст бейджа",
            placeholder="набор открыт",
            key="cover_badge"
        )

    if st.button("Сформировать обложку", type="primary", key="generate_cover"):
        if not cover_title.strip():
            st.warning("Введите текст заголовка для обложки")
        else:
            if cover_mode == "Шаблон":
                txt_color = cover_text_color(bg_color)
                sub_color = txt_color if txt_color == "#102D69" else "rgba(255, 255, 255, 0.85)"
                accents = cover_accent_colors(bg_color)
                gradient_end = COVER_GRADIENT_ENDS.get(bg_color, bg_color)
                logos_html = render_cover_logos(selected_logos, bg_color)

                cover_html = COVER_HTML_TEMPLATE.format(
                    bg_color=bg_color,
                    bg_gradient_end=gradient_end,
                    logos_html=logos_html,
                    title_text=cover_title,
                    subtitle_text=cover_subtitle or "",
                    badge_text=cover_badge or "",
                    title_color=txt_color,
                    subtitle_color=sub_color,
                    accent_stripe=accents["accent_stripe"],
                    marker_color=accents["marker_color"],
                    marker_shadow=accents["marker_shadow"],
                    badge_bg=accents["badge_bg"],
                    badge_text_color=accents["badge_text_color"],
                    badge_border=accents["badge_border"],
                )
                st.session_state['generated_cover_html'] = cover_html
                st.success("Обложка сформирована!")

            else:
                with st.spinner("ИИ генерирует обложку..."):
                    try:
                        client = get_nebius_client()
                        logos_desc = ", ".join([COVER_LOGOS[k]["name"] for k in selected_logos]) if selected_logos else "без логотипов"
                        user_msg = (
                            f"Создай обложку со следующими параметрами:\n"
                            f"- Цвет фона: {bg_color}\n"
                            f"- Логотипы: {logos_desc}\n"
                            f"- Заголовок: {cover_title}\n"
                            f"- Подзаголовок: {cover_subtitle}\n"
                            f"- Бейдж: {cover_badge}\n"
                        )
                        if selected_logos:
                            is_dark_bg = bg_color.upper() == "#102D69"
                            svg_key = "svg_dark" if is_dark_bg else "svg"
                            logos_svg_section = ""
                            for k in selected_logos:
                                logo = COVER_LOGOS[k]
                                logos_svg_section += f"\nЛоготип {logo['name']} (inline SVG):\n{logo[svg_key]}\nВысота: {logo['height']}px, ширина: auto\n"
                            user_msg += f"\nВстрой логотипы как inline SVG (НЕ img, а прямо <svg> тег) с style=\"height:Npx;width:auto;display:block;\":\n{logos_svg_section}"

                        response = client.chat.completions.create(
                            model="deepseek-ai/DeepSeek-V4-Pro",
                            messages=[
                                {"role": "system", "content": COVER_SYSTEM_MESSAGE},
                                {"role": "user", "content": user_msg}
                            ],
                            timeout=120.0
                        )
                        raw = response.choices[0].message.content.strip()
                        if raw.startswith("```json"):
                            raw = raw[7:]
                        elif raw.startswith("```"):
                            raw = raw[3:]
                        if raw.endswith("```"):
                            raw = raw[:-3]
                        raw = raw.strip()

                        parsed = json.loads(raw)
                        if parsed.get("type") != "HTML":
                            raise ValueError("Поле 'type' должно быть 'HTML'.")
                        content = parsed.get("content")
                        if not isinstance(content, str) or not content.strip():
                            raise ValueError("Поле 'content' отсутствует или пустое.")

                        st.session_state['generated_cover_html'] = content.strip()
                        st.success("Обложка сгенерирована!")
                    except Exception as e:
                        st.error(f"Ошибка: {e}")

    if 'generated_cover_html' in st.session_state:
        cover_code = st.session_state['generated_cover_html']
        cov_col1, cov_col2 = st.columns([1, 1])

        with cov_col1:
            st.subheader("HTML-код")
            with st.container(height=800):
                st.code(cover_code, language="html")
            cov_btn1, cov_btn2 = st.columns(2)
            with cov_btn1:
                st.download_button(
                    label="Скачать HTML",
                    data=cover_code.encode("utf-8"),
                    file_name="cover.html",
                    mime="text/html",
                    use_container_width=True,
                    key="download_cover"
                )
            with cov_btn2:
                escaped_cover = html.escape(cover_code)
                components.html(
                    f"""
                    <style>
                    .copy-container {{
                        display: flex;
                        align-items: center;
                        height: 38px;
                        margin-top: -8px;
                    }}
                    .copy-btn {{
                        background-color: #5A9DF8;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 0.5rem 1rem;
                        font-size: 14px;
                        font-weight: 500;
                        cursor: pointer;
                        width: 100%;
                        transition: all 0.2s ease;
                        height: 38px;
                    }}
                    .copy-btn:hover {{
                        background-color: #4a8de0;
                    }}
                    </style>
                    <div class="copy-container">
                        <textarea id="cover-html-content" style="position: absolute; left: -9999px;">{escaped_cover}</textarea>
                        <button class="copy-btn" onclick="
                            var content = document.getElementById('cover-html-content').value;
                            navigator.clipboard.writeText(content).then(function() {{
                                alert('HTML обложки скопирован в буфер обмена!');
                            }}, function(err) {{
                                alert('Ошибка копирования: ' + err);
                            }});
                        ">Скопировать HTML</button>
                    </div>
                    """,
                    height=38
                )

        with cov_col2:
            st.subheader("Предпросмотр")
            safe_cover = html.escape(cover_code, quote=True)
            cover_preview = f"""
            <div style="
                width: 100%;
                height: 500px;
                overflow: auto;
                border: 1px solid #333;
                border-radius: 12px;
                background: white;
                padding: 0;
                box-sizing: border-box;
            ">
                <iframe
                    srcdoc="{safe_cover}"
                    style="width: 100%; height: 100%; border: none; display: block;"
                    sandbox="allow-same-origin"
                ></iframe>
            </div>
            """
            components.html(cover_preview, height=520, scrolling=False)

            png_component = _build_png_component(cover_code)
            components.html(png_component, height=50, scrolling=False)
