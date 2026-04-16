"""
Модуль 2: Генератор HTML-карточек
AI-генерация рассылок в фирменном стиле ВШЭ
"""

import streamlit as st
import json
import html
import streamlit.components.v1 as components
from utils import icon, apply_custom_css, get_nebius_client
from constants import LOGO_URL, LOGO_URL_BLACK, LOGO_URL_PNG, HTML_EXAMPLE, SYSTEM_MESSAGE, TEMPLATES, WEBINAR_TEMPLATE

# Применяем кастомные стили
apply_custom_css()

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

def generate_hse_html(client, user_text: str, style_mode: str, accent_color: str, allow_text_edits: bool, width_css: str, tone: str, template_key: str = "data_culture") -> str:
    """
    Генерация HTML-карточки через Nebius API
    
    Args:
        client: OpenAI клиент
        user_text: Текст объявления
        style_mode: "Для сайта" или "Для почты"
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

    # Логика для режима "Для почты" (ранее "Чистый HTML")
    if style_mode == "Для почты":
        # Улучшенный шаблон для писем
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
    else:
        # Логика для HTML с Inline CSS (Modern)
        # Внедряем ширину в контейнер примера
        max_width_val = width_css
        current_html_example = current_html_example.replace("max-width: 860px;", f"max-width: {max_width_val};")

        # ВСЕГДА заменяем логотип на правильный (PNG для синего, Black для лайма)
        current_html_example = current_html_example.replace(LOGO_URL, current_logo_url)

        if accent_color.upper() != "#001A57":
            current_html_example = current_html_example.replace("#001a57", accent_color)
            current_html_example = current_html_example.replace("#00256c", accent_color)
            if is_light_color:
                # Если фон светлый, текст на нем делаем черным
                current_html_example = current_html_example.replace("color: #ffffff;", "color: #000000;")
        
        system_msg = (
            "Вы — эксперт по оформлению официальных рассылок НИУ ВШЭ. "
            "Ваша задача — преобразовать входной текст объявления в HTML-карточку. "
            "В шапке обязательно должен быть логотип по ссылке: " + current_logo_url + ". "
            "Используйте структуру и CSS-стили из приведённого ниже примера. "
            f"Ширина карточки должна быть: {max_width_val} "
            f"{color_instruction}\n"
            "ВАЖНО: Для предупреждений (attention) используйте ЖЕЛТЫЙ блок (background: #FFFBEB, color: #92400E, border-left: 4px solid #F59E0B).\n"
            "ВАЖНО: Для критической информации (important/danger) используйте КРАСНЫЙ блок (background: #FEF2F2, color: #991B1B, border-left: 4px solid #EF4444).\n"
            "Для обычной информации используйте нейтральный или зеленый блок. "
            "Не добавляйте пояснений, комментариев или лишних тегов. "
            f"{text_instruction}\n"
            "Верните ТОЛЬКО корректный JSON в формате: {\"type\": \"HTML\", \"content\": \"<div>...</div>\"}.\n\n"
            "Пример корректного вывода:\n"
            + str({"type": "HTML", "content": current_html_example})
        )
    
    # Специальная логика для шаблона вебинаров
    if template_key == "webinars":
        webinar_system_msg = (
            "Вы — эксперт по оформлению email-рассылок для анонсов вебинаров НИУ ВШЭ. "
            "Ваша задача — преобразовать входной текст с информацией о вебинарах в HTML-рассылку. "
            "ИСПОЛЬЗУЙТЕ ТОЧНУЮ СТРУКТУРУ из приведённого ниже шаблона!\n\n"
            "ТРЕБОВАНИЯ:\n"
            "1. СОХРАНЯЙТЕ структуру шаблона: header → content → events-grid → past-webinars → feedback → footer.\n"
            "2. Каждый вебинар оформляйте как отдельную карточку (.card) внутри .events-grid.\n"
            "3. В каждой карточке должны быть: метка 'Онлайн', дата/время, название, описание, кнопка регистрации.\n"
            "4. Если в тексте указаны прошедшие вебинары или записи — добавьте их в секцию .past-webinars.\n"
            "5. Заголовок и подзаголовок в header адаптируйте под контент пользователя.\n"
            "6. НЕ добавляйте лишних комментариев — только HTML-код.\n"
            f"{text_instruction}\n"
            "Верните ТОЛЬКО корректный JSON в формате: {\"type\": \"HTML\", \"content\": \"<!DOCTYPE html>...\"}.\n\n"
            "ШАБЛОН:\n"
            + str({"type": "HTML", "content": current_html_example})
        )
        system_msg = webinar_system_msg

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3.2-fast",
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

# Проверка наличия API ключа выполняется внутри get_nebius_client() при вызове
# Но для UI можем проверить наличие в env или secrets, чтобы предупредить юзера заранее, 
# хотя это не строго обязательно, так как get_nebius_client упадет с понятной ошибкой.
# Оставим упрощенную проверку или уберем блокировку, полагаясь на try/except при генерации.

# Убираем блокирующий код, так как ключ теперь может быть в os.environ
pass

# =============================================================================
# ВЫБОР ШАБЛОНА
# =============================================================================

st.markdown("### 🎨 Выберите макет")

# Инициализация выбранного шаблона в session_state
if 'selected_template' not in st.session_state:
    st.session_state['selected_template'] = 'data_culture'

@st.dialog("Предпросмотр макета", width="large")
def show_template_preview(template_key):
    template_data = TEMPLATES[template_key]
    st.markdown(f"### {template_data['name']}")
    st.info(template_data['description'])
    
    # Экранируем HTML и оборачиваем в iframe
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

# Стили для выравнивания высоты карточек
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

# Отрисовка компактных карточек выбора
template_cols = st.columns(len(TEMPLATES))

for idx, (template_key, template_data) in enumerate(TEMPLATES.items()):
    with template_cols[idx]:
        is_selected = st.session_state['selected_template'] == template_key
        
        # Создаем визуальную карточку через st.container с border
        with st.container(border=True):
            # Заголовок с фиксированный высотой для выравнивания
            st.markdown(f"<div class='template-card-header'><h4>{template_data['name']}</h4></div>", unsafe_allow_html=True)
            
            # Описание с фиксированный высотой
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
                # Кнопка без эмоджи, используем текст или иконку из utils если нужно
                if st.button("Превью", key=f"prev_{template_key}", help="Предпросмотр макета", use_container_width=True):
                    show_template_preview(template_key)

st.divider()

# =============================================================================
# НАСТРОЙКИ ГЕНЕРАЦИИ
# =============================================================================

col_settings_1, col_settings_2 = st.columns(2)

with col_settings_1:
    style_mode = st.radio(
        "Режим верстки",
        ["Для сайта", "Для почты"],
        help="Выберите 'Для почты' для создания Email-safe верстки (таблицы + инлайн стили), которая корректно отображается в Outlook и других почтовых клиентах."
    )
    
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
    # Выбор цвета теперь доступен всегда
    accent_color = st.selectbox(
        "Акцентный цвет",
        ["#001A57", "#DFFF00"],
        format_func=lambda x: "🔵 Классический синий" if x == "#001A57" else "🟢 Лайм (#DFFF00)",
        help="Основной цвет заголовков и элементов дизайна"
    )
    
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
                html_code = generate_hse_html(client, user_text, style_mode, accent_color, allow_text_edits, width_css, tone_option, st.session_state['selected_template'])
                # Сохраняем в session_state чтобы не потерять при обновлении
                st.session_state['generated_html'] = html_code
                st.success("Карточка успешно создана!")
            except Exception as e:
                st.error(f"Ошибка: {e}")

# Отображение результата, если HTML уже сгенерирован
if 'generated_html' in st.session_state:
    html_code = st.session_state['generated_html']
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("HTML-код")
        st.code(html_code, language="html")
        
        # Кнопки скачивания и копирования
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
            # Кнопка копирования с выравниванием
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

        # Экранируем HTML и оборачиваем в scrollable div
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
                style="
                    width: 100%;
                    height: 100%;
                    border: none;
                    display: block;
                "
                sandbox="allow-same-origin allow-scripts"
            ></iframe>
        </div>
        """

        components.html(preview_html, height=850, scrolling=False)
        
        st.info(
            "💡 **Совет:** Для рассылки через обычный почтовый клиент (Outlook, Apple Mail) "
            "рекомендуется копировать верстку прямо из окна предпросмотра (выделить всё -> копировать), "
            "а не использовать исходный HTML-код. После вставки в письмо текст можно будет отредактировать."
        )
