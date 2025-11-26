"""
Модуль 2: Генератор HTML-карточек
AI-генерация рассылок в фирменном стиле ВШЭ
"""

import streamlit as st
import json
import html
import streamlit.components.v1 as components
from utils import icon, apply_custom_css, get_nebius_client
from constants import LOGO_URL, LOGO_URL_BLACK, HTML_EXAMPLE, SYSTEM_MESSAGE

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

def generate_hse_html(client, user_text: str, style_mode: str, accent_color: str) -> str:
    """
    Генерация HTML-карточки через Nebius API
    
    Args:
        client: OpenAI клиент
        user_text: Текст объявления
        style_mode: "HTML с CSS" или "Чистый HTML"
        accent_color: HEX код основного цвета
        
    Returns:
        HTML-код карточки
    """
    
def generate_hse_html(client, user_text: str, style_mode: str, accent_color: str) -> str:
    """
    Генерация HTML-карточки через Nebius API
    
    Args:
        client: OpenAI клиент
        user_text: Текст объявления
        style_mode: "HTML с CSS" или "Чистый HTML"
        accent_color: HEX код основного цвета
        
    Returns:
        HTML-код карточки
    """
    
def generate_hse_html(client, user_text: str, style_mode: str, accent_color: str) -> str:
    """
    Генерация HTML-карточки через Nebius API
    
    Args:
        client: OpenAI клиент
        user_text: Текст объявления
        style_mode: "HTML с CSS" или "Чистый HTML"
        accent_color: HEX код основного цвета
        
    Returns:
        HTML-код карточки
    """
    
    # Базовый пример
    current_html_example = HTML_EXAMPLE
    
    # Определяем цвет текста для хедера (белый или черный)
    is_light_color = False
    if accent_color.upper() == "#DFFF00":
        is_light_color = True
    header_text_color = "#000000" if is_light_color else "#ffffff"
    
    # Выбираем логотип
    current_logo_url = LOGO_URL_BLACK if is_light_color else LOGO_URL

    # Логика для чистого HTML (теперь это Email-Safe HTML: Таблицы + Inline CSS)
    if style_mode == "Чистый HTML":
        # Шаблон на основе примера пользователя
        pure_html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Заголовок</title>
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, Helvetica, sans-serif; color: #1f2937; line-height: 1.5;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff">
    <tr>
      <td align="center" style="padding: 40px 16px;">
        <!-- Основной контейнер -->
        <table width="860" cellpadding="0" cellspacing="0" border="0" style="border-collapse: collapse;">
          <!-- Хедер -->
          <tr>
            <td bgcolor="{accent_color}" style="padding: 40px 32px 32px; text-align: center; border-top-left-radius: 0; border-top-right-radius: 0;">
              <img src="{current_logo_url}" alt="Логотип Data Culture" width="57" height="57" style="display: block; margin: 0 auto 20px;">
              <h1 style="margin: 0 0 12px; font-size: 24px; font-weight: bold; color: {header_text_color}; line-height: 1.2; letter-spacing: -0.02em;">
                ЗАГОЛОВОК ОБЪЯВЛЕНИЯ
              </h1>
              <p style="margin: 0; font-size: 18px; color: {header_text_color}; opacity: 0.9; line-height: 1.5;">
                Краткое введение
              </p>
            </td>
          </tr>

          <!-- Основная подложка -->
          <tr>
            <td bgcolor="#F5F5F7" style="padding: 32px;">
              <!-- Карточка 1: Текст -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="margin-bottom: 24px; border: 1px solid #e2e8f5;">
                <tr>
                  <td style="padding: 28px 32px; font-size: 17px; color: #1f2937;">
                    Текст объявления...
                  </td>
                </tr>
              </table>

              <!-- Карточка 2: Список (если есть) -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="margin-bottom: 24px; border: 1px solid #e2e8f5;">
                <tr>
                  <td style="padding: 28px 32px 32px; font-size: 17px; color: #1f2937;">
                    <h2 style="margin: 0 0 20px; font-size: 22px; font-weight: bold; color: {accent_color};">
                      Подзаголовок
                    </h2>
                    <table cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td width="12" valign="top" style="padding-right: 10px;">•</td>
                        <td style="padding-bottom: 14px; line-height: 1.68;">Пункт списка</td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <!-- Карточка 3: Инфо-блок (если есть) -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f0f4ff" style="margin-bottom: 24px; border: 1px solid #dbe4ff;">
                <tr>
                  <td style="padding: 24px 32px; font-size: 16px; color: #1e40af;">
                    <strong>Важная информация:</strong><br>
                    Текст информации.
                  </td>
                </tr>
              </table>

              <!-- Карточка 4: Финальный блок -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ecfdf5" style="border: 1px solid #86efac;">
                <tr>
                  <td style="padding: 32px; font-size: 18px; text-align: center; color: #166534;">
                    <strong>Удачи в работе!</strong><br>
                    <span style="font-size: 15px; opacity: 0.9;">Команда Data Culture всегда с вами</span>
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
            "Вы — эксперт по верстке HTML-писем. "
            "Ваша задача: Преобразовать текст в HTML-карточку, СТРОГО следуя предоставленному шаблону. "
            "ШАБЛОН (используйте эту структуру, меняя только текст):\n"
            f"{pure_html_template}\n\n"
            "ТРЕБОВАНИЯ:"
            "1. Используйте ТОЛЬКО табличную верстку (как в шаблоне)."
            "2. Используйте ТОЛЬКО инлайн-стили (как в шаблоне)."
            "3. Логотип: используйте ссылку " + current_logo_url + " (в шаблоне она уже подставлена)."
            f"4. Цвета: Основной цвет {accent_color}, Текст заголовка {header_text_color}."
            "5. Контент: Разбейте входной текст на логические блоки (вступление, списки, важное) и поместите их в соответствующие карточки-таблицы."
            "Верните JSON: {\"type\": \"HTML\", \"content\": \"<!DOCTYPE html><html>...</html>\"}."
        )
    else:
        # Логика для HTML с Inline CSS (Modern)
        # Если выбран не стандартный синий цвет, делаем замену в примере
        if accent_color.upper() != "#001A57":
            # Заменяем основные синие цвета на выбранный акцент
            current_html_example = current_html_example.replace("#001a57", accent_color)
            current_html_example = current_html_example.replace("#00256c", accent_color)
            
            # Если цвет светлый, меняем цвет текста в хедере
            if is_light_color:
                current_html_example = current_html_example.replace("color: #ffffff;", f"color: {header_text_color};")
                # И меняем логотип на черный
                current_html_example = current_html_example.replace(LOGO_URL, current_logo_url)
        
        system_msg = (
            "Вы — эксперт по оформлению официальных рассылок НИУ ВШЭ. "
            "Ваша задача — преобразовать входной текст объявления в HTML-карточку. "
            "В шапке обязательно должен быть логотип по ссылке: " + current_logo_url + ". "
            "Используйте структуру и CSS-стили из приведённого ниже примера. "
            "Не добавляйте пояснений, комментариев или лишних тегов. "
            "Верните ТОЛЬКО корректный JSON в формате: {\"type\": \"HTML\", \"content\": \"<div>...</div>\"}.\n\n"
            "Пример корректного вывода:\n"
            + str({"type": "HTML", "content": current_html_example})
        )

    response = client.chat.completions.create(
        model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
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

# Проверка наличия API ключа
try:
    has_api_key = "NEBIUS_API_KEY" in st.secrets
except FileNotFoundError:
    has_api_key = False

if not has_api_key:
    st.error("NEBIUS_API_KEY не настроен. Обратитесь к администратору.")
    st.info("Создайте файл `.streamlit/secrets.toml` с вашим API ключом")
    st.stop()

col_settings_1, col_settings_2 = st.columns(2)

with col_settings_1:
    style_mode = st.radio(
        "Режим верстки",
        ["HTML с CSS", "Чистый HTML"],
        help="Выберите 'Чистый HTML' для создания Email-safe верстки (таблицы + инлайн стили), которая корректно отображается в Outlook и других почтовых клиентах."
    )

with col_settings_2:
    # Выбор цвета теперь доступен всегда
    accent_color = st.selectbox(
        "Акцентный цвет",
        ["#001A57", "#DFFF00"],
        format_func=lambda x: "🔵 Классический синий" if x == "#001A57" else "🟢 Лайм (#DFFF00)",
        help="Основной цвет заголовков и элементов дизайна"
    )

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
                html_code = generate_hse_html(client, user_text, style_mode, accent_color)
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
