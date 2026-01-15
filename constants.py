"""
DataCulture Platform - Constants
"""

LOGO_URL = "https://raw.githubusercontent.com/TimPad/html/main/DC_green.svg"
LOGO_URL_BLACK = "https://raw.githubusercontent.com/TimPad/DC_platform_var2/main/icons/DC_black.svg"
LOGO_URL_PNG = "https://raw.githubusercontent.com/TimPad/DC_platform_var2/main/dc.png"

HTML_EXAMPLE = f"""<div style="
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    max-width: 860px;
    margin: 40px auto;
    container-type: inline-size;">
  
  <!-- Хедер -->
  <header style="
    background: linear-gradient(135deg, #001a57 0%, #00256c 100%);
    color: #ffffff;
    padding: 40px 32px 32px;
    text-align: center;
    border-radius: 20px 20px 0 0;
    overflow: hidden;">
    <img src="{LOGO_URL}"
         alt="Логотип Data Culture"
         style="height: 56px; width: auto; max-width: 240px; margin-bottom: 20px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">
    <h1 style="margin: 0 0 12px; font-size: clamp(1.8rem, 5vw, 2.5rem); font-weight: 800; line-height: 1.2; letter-spacing: -0.02em;">
      ЗАГОЛОВОК ОБЪЯВЛЕНИЯ
    </h1>
    <p style="margin: 0; font-size: 1.15rem; opacity: 0.95; line-height: 1.5; max-width: 640px; margin-left: auto; margin-right: auto;">
      Краткое введение или контекст, которое сразу цепляет внимание.
    </p>
  </header>

  <!-- Основная подложка #F5F5F7 -->
  <div style="background: #F5F5F7; padding: 32px; border-radius: 0 0 20px 20px;">

    <!-- Карточка 1: Вступление -->
    <section style="background:#fff; border-radius:16px; padding:28px 32px; margin-bottom:24px; box-shadow:0 4px 16px rgba(0,27,82,0.06); border:1px solid #e2e8f5;">
      <p style="margin:0; color:#1f2937; font-size:1.06rem; line-height:1.7;">
        Основной текст объявления с чёткой структурой и достаточными отступами для комфортного чтения.
      </p>
    </section>

    <!-- Карточка 2: Подзаголовок + список -->
    <section style="background:#fff; border-radius:16px; padding:28px 32px 32px; margin-bottom:24px; box-shadow:0 4px 16px rgba(0,27,82,0.06); border:1px solid #e2e8f5;">
      <h2 style="margin:0 0 20px; color:#001a57; font-size:1.5rem; font-weight:700;">Подзаголовок</h2>
      <ul style="margin:0; padding-left:34px; list-style:none;">
        <li style="position:relative; margin-bottom:14px; line-height:1.68;">
          <span style="position:absolute; left:-34px; top:0.5em; width:10px; height:10px; border:2.5px solid #00256c; border-radius:50%; background:transparent; transform:translateY(-50%);"></span>
          Пункт списка — чистый, профессиональный и идеально выровненный
        </li>
        <li style="position:relative; margin-bottom:14px; line-height:1.68;">
          <span style="position:absolute; left:-34px; top:0.5em; width:10px; height:10px; border:2.5px solid #00256c; border-radius:50%; background:transparent; transform:translateY(-50%);"></span>
          Ещё один пункт — выглядит дорого и современно
        </li>
        <li style="position:relative; line-height:1.68;">
          <span style="position:absolute; left:-34px; top:0.5em; width:10px; height:10px; border:2.5px solid #00256c; border-radius:50%; background:transparent; transform:translateY(-50%);"></span>
          Последний пункт без лишнего отступа снизу
        </li>
      </ul>
    </section>

    <!-- Карточка 3: Инфо-блок -->
    <section style="background:linear-gradient(135deg,#f8faff 0%,#f0f4ff 100%); border:1px solid #dbe4ff; border-radius:16px; padding:24px 32px; margin-bottom:24px; box-shadow:0 4px 16px rgba(0,50,140,0.06);">
      <p style="margin:0; color:#1e40af; font-size:1.02rem;">
        <strong>Информация: Важная информация</strong><br>
        Этот блок привлекает внимание мягким градиентом и лёгкой тенью.
      </p>
    </section>

    <!-- Карточка 4: Предупреждение -->
    <aside style="background:#fffbeb; border:1px solid #fcd34d; border-left:6px solid #f59e0b; border-radius:16px; padding:24px 32px; margin-bottom:24px; box-shadow:0 4px 16px rgba(245,158,11,0.12);">
      <p style="margin:0; font-weight:700; color:#92400e; font-size:1.05rem;">
        Предупреждение: Внимание! Важное уточнение, которое нельзя пропустить.
      </p>
    </aside>

    <!-- Карточка 5: Финальный мотивационный блок -->
    <aside style="background:linear-gradient(135deg,#f0fdf4 0%,#ecfdf5 100%); border:1px solid #86efac; border-radius:16px; padding:32px; text-align:center; font-size:1.15rem; box-shadow:0 4px 20px rgba(34,197,94,0.14);">
      <p style="margin:0; color:#166534;">
        <strong>Удачи в проекте!</strong> Ракета<br>
        <span style="font-size:0.95em; opacity:0.9;">Команда Data Culture всегда с вами</span>
      </p>
    </aside>

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
# LOTTIE ANIMATIONS
# =============================================================================
LOTTIE_LOADING_URL = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"  # Coding/Processing
LOTTIE_SUCCESS_URL = "https://assets9.lottiefiles.com/packages/lf20_jbrw3hcz.json"  # Checkmark
LOTTIE_EMPTY_URL = "https://assets9.lottiefiles.com/packages/lf20_sif17h.json"     # Empty Box

# =============================================================================
# STUDENT DATA CONSTANTS
# =============================================================================

# Possible variations of column names in input files for student lists
STUDENT_REQUIRED_COLUMNS = {
    'ФИО': ['фио', 'фio', 'имя', 'name'],
    'Корпоративная почта': ['адрес электронной почты', 'корпоративная почта', 'email', 'почта', 'e-mail'],
    'Филиал (кампус)': ['филиал', 'кампус', 'campus'],
    'Факультет': ['факультет', 'faculty'],
    'Образовательная программа': ['образовательная программа', 'программа', 'educational program'],
    'Версия образовательной программы': ['версия образовательной программы', 'версия программы', 'program version', 'version'],
    'Группа': ['группа', 'group'],
    'Курс': ['курс', 'course'],
    'Уровень образования': ['уровень образования', 'уровень', 'level', 'образование']
}

# Mapping from Supabase column names to internal DataFrame column names
STUDENT_DB_TO_DF_MAPPING = {
    'корпоративная_почта': 'Адрес электронной почты',
    'фио': 'ФИО',
    'филиал_кампус': 'Филиал (кампус)',
    'факультет': 'Факультет',
    'образовательная_программа': 'Образовательная программа',
    'версия_образовательной_программы': 'Версия образовательной программы',
    'группа': 'Группа',
    'курс': 'Курс',
    'уровень_образования': 'Уровень образования'
}
