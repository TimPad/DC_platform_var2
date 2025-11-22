"""
Модуль 2: Генератор HTML-карточек
AI-генерация рассылок в фирменном стиле ВШЭ
"""

import streamlit as st
import json
import html
import streamlit.components.v1 as components
from utils import icon, apply_custom_css, get_nebius_client
from constants import LOGO_URL, HTML_EXAMPLE, SYSTEM_MESSAGE

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

def generate_hse_html(client, user_text: str) -> str:
    """
    Генерация HTML-карточки через Nebius API
    
    Args:
        client: OpenAI клиент
        user_text: Текст объявления
        
    Returns:
        HTML-код карточки
    """
    response = client.chat.completions.create(
        model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
        # response_format={"type": "json_object"}, # Removed to match user example
        messages=[
            {
                "role": "system", 
                "content": SYSTEM_MESSAGE
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
                html_code = generate_hse_html(client, user_text)
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
