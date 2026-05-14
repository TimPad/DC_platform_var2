"""
DataCulture Platform - Constants
"""

LOGO_URL = "https://raw.githubusercontent.com/TimPad/html/main/DC_green.svg"
LOGO_URL_BLACK = "https://raw.githubusercontent.com/TimPad/DC_platform_var2/main/icons/DC_black.svg"
LOGO_URL_PNG = "https://raw.githubusercontent.com/TimPad/DC_platform_var2/main/dc.png"
LOGO_URL_FCS = "https://raw.githubusercontent.com/TimPad/DC_platform_var2/main/fcs.svg"

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

# Шаблон для рассылок ФКС ВШЭ
FCS_TEMPLATE = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="ru">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="x-apple-disable-message-reformatting" />
  <title>{email_title}</title>
  <!--[if mso]>
  <style>
    table { border-collapse: collapse; }
    td, th { font-family: Arial, sans-serif !important; }
  </style>
  <![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  
  <!-- Outer wrapper -->
  <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#f8f9fa" role="presentation">
    <tr>
      <td align="center" style="padding: 24px 16px;">
        
        <!-- Main card container -->
        <table border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: separate; border-radius: 16px; overflow: hidden; background-color: #ffffff; box-shadow: 0 4px 20px rgba(16,45,105,0.08); min-width: 320px; max-width: 600px;" role="presentation">
          
          <!-- HEADER LAYER (Layer 2: accent background) -->
          <tr>
            <td bgcolor="#102D69" style="padding: 40px 32px 32px; position: relative;">
              
              <!-- Decorative marker (Layer 2 element) -->
              <div style="position: absolute; top: 24px; right: 32px; width: 8px; height: 8px; background: #DCFF05; border-radius: 50%;"></div>
              
              <!-- Logo with guard zone -->
              <table border="0" cellpadding="0" cellspacing="0" role="presentation">
                <tr>
                  <td style="padding-bottom: 24px;">
                    <a href="{logo_link}" target="_blank">
                      <img src="{fkn_logo_url}" alt="ФКН ВШЭ" width="56" style="display: block; width: 56px; height: auto; border: 0; border-radius: 8px; background: #ffffff; padding: 4px;" />
                    </a>
                  </td>
                </tr>
              </table>
              
              <!-- Header text (Layer 1: calm, rounded) -->
              <h1 style="color: #ffffff; font-size: 24px; line-height: 32px; font-weight: 700; margin: 0 0 12px 0; letter-spacing: -0.02em;">
                {header_title}
              </h1>
              <p style="color: rgba(255,255,255,0.92); font-size: 16px; line-height: 24px; margin: 0; font-weight: 400;">
                {header_subtitle}
              </p>
              
              <!-- Bottom accent bar -->
              <div style="height: 4px; background: linear-gradient(90deg, #DCFF05 0%, #DFC7F2 100%); margin: 24px -32px -32px; border-radius: 0 0 16px 16px;"></div>
            </td>
          </tr>

          <!-- CONTENT LAYER (Layer 1: light, soft, rounded) -->
          <tr>
            <td style="padding: 32px;">
              
              <!-- Content Block 1: Primary info -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                <tr>
                  <td style="padding-bottom: 24px; font-size: 16px; line-height: 26px; color: #102D69;">
                    {primary_content}
                  </td>
                </tr>
              </table>

              <!-- Content Block 2: List with accent -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#F9FAFB" style="border-radius: 12px; border: 1px solid #e5e7eb;" role="presentation">
                <tr>
                  <td style="padding: 20px 24px;">
                    <h2 style="color: #102D69; font-size: 18px; font-weight: 600; margin: 0 0 16px 0;">
                      {list_title}
                    </h2>
                    <ul style="margin: 0; padding-left: 20px; color: #374151; font-size: 15px; line-height: 24px;">
                      <li style="margin-bottom: 8px;">{list_item_1}</li>
                      <li style="margin-bottom: 8px;">{list_item_2}</li>
                      <li>{list_item_3}</li>
                    </ul>
                  </td>
                </tr>
              </table>
              <div style="height: 24px; font-size: 0; line-height: 0;">&nbsp;</div>

              <!-- Alert Block: Warning (Fluorescent accent) -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#FFFBEB" style="border-radius: 12px; border-left: 4px solid #DCFF05;" role="presentation">
                <tr>
                  <td style="padding: 16px 20px; font-size: 15px; line-height: 24px; color: #92400E;">
                    <strong style="color: #102D69;">внимание:</strong> {warning_text}
                  </td>
                </tr>
              </table>
              <div style="height: 24px; font-size: 0; line-height: 0;">&nbsp;</div>

              <!-- Alert Block: Critical (Lavender accent) -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#F5F3FF" style="border-radius: 12px; border-left: 4px solid #DFC7F2;" role="presentation">
                <tr>
                  <td style="padding: 16px 20px; font-size: 15px; line-height: 24px; color: #5B21B6;">
                    <strong style="color: #102D69;">важно:</strong> {critical_text}
                  </td>
                </tr>
              </table>
              <div style="height: 32px; font-size: 0; line-height: 0;">&nbsp;</div>

              <!-- CTA Button (Optional) -->
              {cta_block}
              
            </td>
          </tr>

          <!-- FOOTER (Brand closure) -->
          <tr>
            <td bgcolor="#102D69" style="padding: 24px 32px; text-align: center;">
              <p style="color: rgba(255,255,255,0.85); font-size: 14px; line-height: 20px; margin: 0 0 12px 0;">
                {footer_text}
              </p>
              <!-- Social/Links row -->
              <table border="0" cellpadding="0" cellspacing="0" align="center" role="presentation">
                <tr>
                  <td style="padding: 0 8px;">
                    <a href="{link_1}" style="color: #DCFF05; text-decoration: none; font-size: 13px; font-weight: 500;">{link_1_text}</a>
                  </td>
                  <td style="padding: 0 8px;">
                    <a href="{link_2}" style="color: #DCFF05; text-decoration: none; font-size: 13px; font-weight: 500;">{link_2_text}</a>
                  </td>
                </tr>
              </table>
              
              <!-- Decorative marker for balance -->
              <div style="margin-top: 20px; width: 6px; height: 6px; background: #DFC7F2; border-radius: 50%; display: inline-block;"></div>
            </td>
          </tr>
          
        </table>
        
        <!-- Email client safe spacing -->
        <div style="height: 40px; font-size: 0; line-height: 0;">&nbsp;</div>
        
      </td>
    </tr>
  </table>
  
  <!-- Preheader text (hidden but visible in inbox preview) -->
  <div style="display: none; max-height: 0; overflow: hidden; mso-hide: all;">
    {preheader_text}
  </div>
  
</body>
</html>"""

# Словарь шаблонов с метаданными для UI выбора
TEMPLATES = {
    "data_culture": {
        "name": "Data Culture",
        "description": "Классическая вертикальная верстка с широкими информационными блоками и акцентным хедером. Подходит для длинных объявлений.",
        "icon": "",
        "html": HTML_EXAMPLE,
        "color": "#001A57",
        "preview_bg": "linear-gradient(135deg, #001a57 0%, #00256c 100%)"
    },
    "fcs": {
        "name": "ФКН",
        "description": "Официальный email-шаблон в фирменном стиле ФКС ВШЭ: тёмно-синий хедер, структурированные блоки, блоки предупреждений и CTA-кнопка.",
        "icon": "",
        "html": FCS_TEMPLATE.replace("{fkn_logo_url}", LOGO_URL_FCS),
        "color": "#102D69",
        "preview_bg": "linear-gradient(135deg, #102D69 0%, #1a3f8f 100%)"
    }
}

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

# =============================================================================
# EXTERNAL ASSESSMENT & DATABASE CONSTANTS
# =============================================================================

# Database Tables
DB_TABLE_STUDENT_IO = 'student_io'
DB_TABLE_PERESDACHI = 'peresdachi'
DB_TABLE_FINAL_GRADES = 'final_grades'
DB_TABLE_STUDENTS = 'students'
DB_TABLE_REGISTRATION_DATA = 'registration_data'

# Common Column Names
COL_EMAIL = 'Адрес электронной почты'
COL_DISCIPLINE = 'Наименование дисциплины'
COL_GRADE = 'Оценка'
COL_CAMPUS = 'Кампус'
COL_CAMPUS_OLD = 'Филиал (кампус)'
COL_FIO = 'ФИО'
COL_FACULTY = 'Факультет'
COL_PROGRAM = 'Образовательная программа'
COL_PROGRAM_VERSION = 'Версия образовательной программы'
COL_GROUP = 'Группа'
COL_COURSE = 'Курс'
COL_EDU_LEVEL = 'Уровень образования'
COL_ID_DISCIPLINE = 'ID дисциплины'
COL_PERIOD = 'Период аттестации'
COL_CANCEL = 'Отмена'

# Discipline Names
DISCIPLINE_INPUT = 'Внешнее измерение цифровых компетенций. Входной контроль'
DISCIPLINE_MID = 'Внешнее измерение цифровых компетенций. Промежуточный контроль'
DISCIPLINE_FINAL = 'Внешнее измерение цифровых компетенций. Итоговый контроль'

# Test Column Names
TEST_COL_INPUT = 'Тест:Входное тестирование (Значение)'
TEST_COL_MID = 'Тест:Промежуточное тестирование (Значение)'
TEST_COL_FINAL = 'Тест:Итоговое тестирование (Значение)'

# Project Column Names
PROJECT_COL_HUMANITIES = "Задание:Гуманитарные науки (Значение)"
PROJECT_COL_SOCIO_ECON = "Задание:Социально-экономические науки (Значение)"
PROJECT_COL_NATURAL = "Задание:Естественные науки (Значение)"
PROJECT_COL_GENERAL = "Задание:Общее: интерактивная история (Значение)"
PROJECT_COL_EXTENDED = "Задание:Интерактивная история: Расширенная версия (Значение)"

PROJECT_COLUMNS = [
    PROJECT_COL_HUMANITIES,
    PROJECT_COL_SOCIO_ECON,
    PROJECT_COL_NATURAL,
    PROJECT_COL_GENERAL,
    PROJECT_COL_EXTENDED
]

# =============================================================================
# COMMON PATTERNS
# =============================================================================

HSE_EMAIL_DOMAIN = '@edu.hse.ru'

# Stage detection keywords for grade recalculation
STAGE_KEYWORD_ANALYSIS = 'анализу данных'
STAGE_KEYWORD_PROGRAMMING = 'программированию'
