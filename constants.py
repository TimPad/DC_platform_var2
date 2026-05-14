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

# Шаблон для рассылок ФКН ВШЭ
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
        "description": "Шаблон в фирменном стиле и логотипом Data culture ФКН ВШЭ.",
        "icon": "",
        "html": HTML_EXAMPLE,
        "color": "#001A57",
        "preview_bg": "linear-gradient(135deg, #001a57 0%, #00256c 100%)"
    },
    "fcs": {
        "name": "ФКН",
        "description": "Шаблон в фирменном стиле и логотипом ФКН ВШЭ: тёмно-синий хедер, структурированные блоки, блоки предупреждений и CTA-кнопка.",
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

# =============================================================================
# COVER (ОБЛОЖКИ) CONSTANTS
# =============================================================================

COVER_BRAND_COLORS = {
    "Тёмно-синий (#102D69)": "#102D69",
    "Лаванда (#DFC7F2)": "#DFC7F2",
    "Флуоресцентный (#DCFF05)": "#DCFF05",
    "Белый (#FFFFFF)": "#FFFFFF",
}

COVER_GRADIENT_ENDS = {
    "#102D69": "#1a3a7a",
    "#DFC7F2": "#e8d4f7",
    "#DCFF05": "#e5ff3d",
    "#FFFFFF": "#f0f0f5",
}

COVER_LOGO_FCS_SVG = '''<svg width="740" height="141" viewBox="0 0 740 141" fill="none" xmlns="http://www.w3.org/2000/svg">
<path fill-rule="evenodd" clip-rule="evenodd" d="M0.5 70.709C0.5 31.972 31.9026 0.569336 70.6397 0.569336H232.003C270.74 0.569336 302.143 31.972 302.143 70.709C302.143 109.446 270.74 140.849 232.003 140.849H70.6397C31.9027 140.849 0.5 109.446 0.5 70.709ZM178.041 61.9416H226.262V77.2846H178.041V61.9416ZM125.436 61.9416H77.2153V77.2846H125.436V61.9416ZM540 5.35554H629.681V60.9646H648.552V5.35554H738.233V136.059H648.552V84.8335H629.681V136.059H540V5.35554ZM401.613 6.44291H310.111V137.146H401.613V87.2122L443.258 137.146H524.75V104.683L496.959 73.2648L524.75 41.1189V6.44291H443.258L401.613 58.8988V6.44291Z" fill="#102D69"/>
</svg>'''

COVER_LOGO_HSE_SVG = '''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 51.02 51.02" style="enable-background:new 0 0 51.02 51.02;" xml:space="preserve">
<style type="text/css">.st0{fill:#FFFFFF;}.st1{fill:#002F87;}</style>
<g><ellipse transform="matrix(0.2011 -0.9796 0.9796 0.2011 -4.6085 45.373)" class="st0" cx="25.51" cy="25.51" rx="25.51" ry="25.51"/>
<g><path class="st1" d="M19.75,7.78c1.18-0.39,1.73-1.57,1.37-2.65c-0.36-1.1-1.47-1.73-2.66-1.34c-1.18,0.39-1.73,1.57-1.37,2.65 C17.45,7.54,18.57,8.17,19.75,7.78z M18.66,4.42c0.77-0.25,1.51,0.2,1.76,0.95c0.12,0.38,0.1,0.77-0.05,1.09 c-0.15,0.32-0.42,0.58-0.81,0.71c-0.77,0.25-1.51-0.2-1.76-0.95c-0.2-0.63,0.01-1.26,0.52-1.6C18.43,4.54,18.53,4.46,18.66,4.42z"/>
<path class="st1" d="M14.91,10.08l-0.87-1.43l0.42-0.26l1.19,0.46c0.6,0.24,1.19,0.32,1.61-0.15l-0.32-0.53 c-0.2,0.22-0.52,0.21-0.98,0.05l-1.3-0.47l0.43-2.45l-0.72,0.41l-0.31,2.15l-0.35,0.22l-0.88-1.44l-0.58,0.41l2.09,3.42 L14.91,10.08z"/>
<path class="st1" d="M28.2,6.03L28.2,6.03c0.32,0.04,0.63,0.09,0.95,0.15c0.31,0.06,0.63,0.13,0.94,0.2v0L30.3,7.4l0.75,0.21 l-1-4.4L29.4,3.1l-2.53,3.73l0.76,0.07L28.2,6.03z M29.55,4l0.39,1.71c-0.23-0.05-0.45-0.1-0.68-0.14 c-0.23-0.04-0.45-0.08-0.68-0.12L29.55,4z"/>
<path class="st1" d="M44.02,22.61l1.65-0.15l0.02,0c0.06,0.38,0.1,0.77,0.14,1.15c0.04,0.38,0.06,0.77,0.08,1.16l-0.02,0 l-1.65,0.15l0.02,0.71l4-0.38l-0.03-0.71l-1.68,0.16l-0.01,0c-0.02-0.39-0.04-0.77-0.08-1.16c-0.04-0.38-0.08-0.77-0.14-1.15 l0.01,0l1.69-0.16l-0.11-0.7l-4,0.38L44.02,22.61z"/>
<path class="st1" d="M44.26,16.32c-1.08,0.4-1.66,1.54-1.23,2.71c0.43,1.17,1.64,1.66,2.71,1.26c1.08-0.4,1.66-1.54,1.23-2.71 C46.53,16.41,45.33,15.92,44.26,16.32z M46.35,17.8c0.28,0.75-0.13,1.52-0.87,1.79c-0.07,0.03-0.14,0.02-0.2,0.04 c-0.69,0.16-1.37-0.13-1.62-0.82c-0.18-0.47-0.08-0.95,0.2-1.3c0.04-0.06,0.1-0.11,0.15-0.16c0.01-0.01,0.02-0.03,0.03-0.04 c0.03-0.03,0.07-0.05,0.11-0.08c0.04-0.03,0.08-0.06,0.12-0.09c0,0,0,0,0.01,0c0.08-0.05,0.16-0.09,0.25-0.12 c0.37-0.14,0.76-0.13,1.09,0C45.94,17.16,46.21,17.42,46.35,17.8z"/>
<path class="st1" d="M30.9,22.16c0.88-1.02,1.25-2.26,1.25-3.44c0-0.95-0.26-2.85-1.93-4.16c-1.15-0.89-2.16-1.31-4.59-1.31H24.4 c-0.04,0-0.07,0-0.12,0h-5.06v23.91h14.45v-4.59c0-4.39-1.42-7.34-5.09-8.64C29.73,23.45,30.44,22.72,30.9,22.16z M28.03,21.7 c-0.66,0.82-1.73,1.58-3.25,1.58c-0.01,0-0.02,0-0.03,0v1.19c4.06,0,5.65,2.7,5.65,7.64v3.72h0h-2.61v-7.98h-3.01v7.99h-2.3V14.44 l2.37,0c0.89,0,2.23,0.2,3.18,1.38c0.49,0.6,0.8,1.39,0.9,2.19h-4.15v1.18h4.18C28.93,19.95,28.77,20.8,28.03,21.7z"/>
<path class="st1" d="M40.6,14.41l1.4-0.92l0.27,0.41l-0.42,1.2c-0.22,0.61-0.28,1.2,0.2,1.61l0.52-0.34 c-0.22-0.19-0.22-0.51-0.08-0.97l0.42-1.32l2.46,0.35l-0.44-0.71l-2.16-0.24l-0.23-0.34l1.41-0.93l-0.43-0.57l-3.35,2.2 L40.6,14.41z"/>
<path class="st1" d="M9.77,15.43c0.96-1.5,2.13-2.85,3.47-4.02l-0.5-0.44l-2.58-2.23C9.99,8.9,9.81,9.06,9.65,9.23l2.58,2.22 c-0.39,0.37-0.76,0.75-1.12,1.15l-2.56-2.21c-0.16,0.18-0.31,0.36-0.47,0.54l2.56,2.21c-0.34,0.4-0.66,0.82-0.96,1.26L7.1,12.18 c-0.14,0.19-0.27,0.39-0.41,0.58l2.58,2.23L9.77,15.43z"/>
<path class="st1" d="M41.02,11.53c0.77-0.84,0.76-2.14-0.16-2.98C40.3,8.04,39.63,7.88,39,8.02l0.16,0.71 c0.43-0.11,0.89-0.02,1.26,0.31c0.51,0.47,0.57,1.16,0.23,1.72c-0.3-0.31-0.61-0.61-0.93-0.89c-0.13-0.12-0.27-0.24-0.4-0.36 l-0.41,0.48c0.13,0.11,0.26,0.23,0.39,0.34c0.32,0.29,0.63,0.59,0.93,0.9c-0.53,0.39-1.24,0.4-1.76-0.07 c-0.38-0.34-0.51-0.81-0.42-1.26l-0.71-0.1c-0.09,0.65,0.13,1.34,0.7,1.85C38.96,12.49,40.24,12.38,41.02,11.53z"/>
<path class="st1" d="M34.51,7.74c0.4,0.2,0.89,0.04,1.09-0.36c0.2-0.4,0.04-0.89-0.36-1.09c-0.4-0.2-0.89-0.04-1.09,0.36 C33.95,7.05,34.11,7.54,34.51,7.74z"/>
<path class="st1" d="M23.67,3.86l-0.03-0.39c0.07-0.01,0.14-0.01,0.2-0.02c0.4-0.03,0.8-0.05,1.2-0.06l0.26,3.39l0.71-0.05 L25.75,3.4L25.7,2.76c-0.38,0-0.77,0-1.15,0.02L23.03,2.9c-0.03,0-0.07,0.01-0.1,0.01l0.05,0.63l0.01,0.16 c0.18,2.42-0.18,2.71-0.59,2.74c-0.09,0.01-0.18,0-0.23-0.02l-0.02,0.59c0.11,0.02,0.34,0.04,0.5,0.03 C23.43,6.98,23.86,6.43,23.67,3.86z"/>
<polygon class="st1" points="32.32,42.96 31.09,46.46 30.19,43.65 29.5,43.81 30.74,47.65 31.41,47.48 32.62,44.01 33.52,46.8 34.17,46.54 32.94,42.71"/>
<path class="st1" d="M25.52,45.47c-0.45,0-0.81,0.36-0.81,0.81c0,0.45,0.36,0.81,0.81,0.81c0.45,0,0.81-0.36,0.81-0.81 C26.33,45.84,25.97,45.47,25.52,45.47z"/>
<path class="st1" d="M18.53,44.12c-0.16,0.54,0.08,0.89,0.49,1.18c-0.33,0.07-0.67,0.24-0.81,0.71c-0.08,0.27-0.05,0.51,0.07,0.73 c0.16,0.29,0.47,0.54,0.91,0.67l1.48,0.38l1.12-3.87l-1.52-0.44C19.42,43.22,18.74,43.42,18.53,44.12z M19.47,46.8 c-0.44-0.13-0.63-0.39-0.54-0.69c0.02-0.07,0.05-0.13,0.08-0.18c0,0,0.01,0,0.01-0.01c0.03-0.05,0.07-0.08,0.12-0.11 c0.1-0.06,0.22-0.09,0.37-0.08c0.1,0,0.2,0.02,0.31,0.05l0.66,0.19L20.18,47L19.47,46.8z M19.84,45.16 C19.3,45,19.1,44.73,19.19,44.4c0.08-0.27,0.29-0.4,0.58-0.38c0.1,0,0.21,0.02,0.32,0.06l0.86,0.25l-0.31,1.07L19.84,45.16z"/>
<path class="st1" d="M36.22,40.88l0.88,1.43l-0.42,0.26l-1.19-0.45c-0.6-0.24-1.19-0.31-1.61,0.16l0.33,0.53 c0.2-0.22,0.52-0.21,0.98-0.05l1.31,0.46l-0.41,2.45l0.72-0.42l0.3-2.16l0.35-0.22l0.89,1.43l0.58-0.41l-2.11-3.41L36.22,40.88z"/>
<path class="st1" d="M46.35,27.06c-1.14-0.2-2.22,0.49-2.43,1.72c-0.22,1.23,0.57,2.26,1.7,2.46c1.14,0.2,2.22-0.49,2.43-1.72 C48.26,28.29,47.47,27.25,46.35,27.06z M47.4,29.39c-0.03,0.2-0.11,0.38-0.21,0.53c-0.3,0.45-0.87,0.68-1.45,0.58 c-0.69-0.12-1.18-0.65-1.2-1.31c0-0.09,0-0.19,0.02-0.29c0.03-0.2,0.11-0.38,0.21-0.53c0.3-0.45,0.87-0.68,1.45-0.58 C47.01,27.93,47.54,28.6,47.4,29.39z"/>
<path class="st1" d="M42.98,32.28l1.42,0.81c0.48,0.27,1.05,0.58,1.52,0.84l-0.01,0.01c-0.51-0.12-3.47-0.48-3.47-0.48L42.18,34 c0,0,2.04,2.24,2.43,2.58L44.6,36.6c-0.5-0.25-1.07-0.5-1.55-0.71l-1.52-0.66l-0.4,0.64l3.76,1.57l0.51-0.87 c0,0-1.89-2.06-2.24-2.35l0.01-0.02c0.45,0.1,3.2,0.4,3.2,0.4l0.39-0.95l-3.52-2.07L42.98,32.28z"/>
<polygon class="st1" points="40.05,37.32 40.71,40.97 38.54,38.97 38.03,39.45 41,42.18 41.5,41.69 40.84,38.08 43,40.06 43.44,39.52 40.47,36.79"/>
<rect x="11.21" y="41.93" transform="matrix(0.5751 -0.8181 0.8181 0.5751 -28.9676 28.7894)" class="st1" width="4.05" height="0.71"/>
<path class="st1" d="M10.07,36.1c-1.01-1.47-1.79-3.07-2.34-4.77l-0.6,0.29l-3.06,1.5c0.08,0.22,0.16,0.44,0.25,0.67l3.05-1.51 c0.19,0.5,0.39,1,0.62,1.48l-3.04,1.49c0.1,0.22,0.21,0.43,0.31,0.64L8.3,34.4c0.24,0.47,0.5,0.93,0.78,1.38l-3.04,1.51 c0.12,0.2,0.25,0.4,0.38,0.6l3.06-1.5L10.07,36.1z"/>
<path class="st1" d="M7.29,29.82l-1.01-0.25h0c-0.07-0.31-0.12-0.63-0.17-0.94C6.05,28.32,6.01,28,5.98,27.68l0,0l0.88-0.55 l-0.05-0.78l-3.8,2.43l0.1,0.65l4.37,1.12L7.29,29.82z M5.38,28.05c0.03,0.23,0.06,0.46,0.1,0.69c0.04,0.23,0.08,0.45,0.12,0.68 l-1.7-0.43L5.38,28.05z"/>
<path class="st1" d="M4.02,25.02c0.69,0.06,1.08-0.36,1.22-0.69l0.71,0.61c0.19,0.17,0.32,0.49,0.24,0.71l0.61-0.01 c0.15-0.33,0.07-0.81-0.41-1.21l-0.95-0.8l0.04-0.5l1.45,0.13l0.1-0.72l-4.01-0.32c-0.04,0.22-0.13,1.11-0.14,1.23 C2.78,24.56,3.32,24.97,4.02,25.02z M3.61,22.99l1.2,0.1l-0.04,0.46c-0.03,0.41-0.27,0.76-0.69,0.72 c-0.32-0.03-0.57-0.22-0.53-0.8C3.57,23.34,3.58,23.18,3.61,22.99z"/>
<path class="st1" d="M6.19,18.61c0.45,0.04,0.84-0.28,0.89-0.73c0.04-0.45-0.28-0.84-0.73-0.89c-0.45-0.04-0.84,0.28-0.89,0.73 C5.41,18.17,5.74,18.56,6.19,18.61z"/>
<path class="st1" d="M11.82,38.15c-0.52-0.56-1.21-0.77-1.85-0.68l0.1,0.71c0.45-0.09,0.92,0.03,1.26,0.41 c0.55,0.59,0.46,1.46-0.12,1.99c-0.59,0.54-1.44,0.57-1.99-0.02c-0.34-0.36-0.43-0.83-0.32-1.26l-0.71-0.15 c-0.13,0.62,0.04,1.3,0.54,1.84c0.85,0.91,2.15,0.91,2.98,0.14C12.56,40.34,12.66,39.07,11.82,38.15z"/>
<path class="st1" d="M14.69,42.37c-0.41,0.7-0.11,1.4,0.67,1.87l0.55,0.33l-0.74,1.26l0.61,0.36l2.06-3.49L16.68,42 C15.87,41.53,15.1,41.67,14.69,42.37z M16.22,44.03l-0.53-0.31c-0.46-0.27-0.61-0.62-0.4-0.98c0.12-0.2,0.27-0.31,0.45-0.34 c0.18-0.03,0.39,0.03,0.62,0.16l0.54,0.32L16.22,44.03z"/>
</g></g>
</svg>'''

COVER_LOGO_DC_SVG = '''<svg width="348" height="229" viewBox="0 60 348 229" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(0,60)">
    <path d="M237.001 135.495V100.331L347.26 41.7236V76.888L271.105 116.894V118.932L347.26 158.938V194.103L237.001 135.495Z" fill="#102D69"/>
    <path d="M0 228.824L82.3092 0H116.412L34.1032 228.824H0Z" fill="#102D69"/>
    <path d="M88.9137 158.498L180.82 118.932V116.894L88.9137 76.4479V41.2835L214.923 100.331V135.495L88.9137 193.663V158.498Z" fill="#102D69"/>
  </g>
</svg>'''

COVER_LOGOS = {
    "hse": {"name": "ВШЭ", "svg": COVER_LOGO_HSE_SVG, "height": 40},
    "fcs": {"name": "ФКН", "svg": COVER_LOGO_FCS_SVG, "height": 32},
    "dc":  {"name": "Data Culture", "svg": COVER_LOGO_DC_SVG, "height": 32},
}

COVER_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title_text}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #f8f9fa;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 24px;
    }}
    .course-cover {{
      position: relative;
      width: 100%;
      max-width: 800px;
      aspect-ratio: 16 / 9;
      background: linear-gradient(135deg, {bg_color} 0%, {bg_gradient_end} 100%);
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(16, 45, 105, 0.25);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .bg-shape {{
      position: absolute;
      top: -10%;
      right: -5%;
      width: 45%;
      aspect-ratio: 1;
      background: #DFC7F2;
      border-radius: 50%;
      opacity: 0.35;
      filter: blur(40px);
      z-index: 1;
    }}
    .accent-stripe {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 6px;
      background: {accent_stripe};
      z-index: 2;
    }}
    .marker-dot {{
      position: absolute;
      top: 29px;
      right: 29px;
      width: 16px;
      height: 16px;
      background: {marker_shadow};
      border-radius: 50%;
      z-index: 3;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .marker-dot::before {{
      content: '';
      width: 10px;
      height: 10px;
      background: {marker_color};
      border-radius: 50%;
      display: block;
    }}
    .header {{
      position: relative;
      z-index: 4;
      padding: 32px 40px 0;
      display: flex;
      align-items: flex-start;
      justify-content: flex-start;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .logo-wrapper {{
      background: #ffffff;
      padding: 10px;
      border-radius: 12px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 1px solid rgba(255, 255, 255, 0.8);
    }}
    .logo {{
      display: block;
      width: auto;
    }}
    .content {{
      position: relative;
      z-index: 4;
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 40px;
      text-align: center;
    }}
    .title {{
      color: {title_color};
      font-size: clamp(28px, 5vw, 44px);
      line-height: 1.2;
      font-weight: 700;
      letter-spacing: -0.02em;
      text-transform: none;
    }}
    .footer {{
      position: relative;
      z-index: 4;
      padding: 0 40px 32px;
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
    }}
    .subtitle {{
      color: {subtitle_color};
      font-size: 14px;
      line-height: 1.5;
      max-width: 60%;
    }}
    .badge {{
      background: {badge_bg};
      color: {badge_text_color};
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.02em;
      border: 1px solid {badge_border};
    }}
    @media (max-width: 600px) {{
      .course-cover {{
        aspect-ratio: 4 / 3;
        border-radius: 20px;
      }}
      .header, .footer {{
        padding-left: 24px;
        padding-right: 24px;
      }}
      .content {{
        padding: 0 24px;
      }}
      .subtitle {{
        max-width: 100%;
        font-size: 13px;
      }}
      .marker-dot {{
        top: 17px;
        right: 17px;
        width: 14px;
        height: 14px;
      }}
      .marker-dot::before {{
        width: 8px;
        height: 8px;
      }}
    }}
    @media (prefers-color-scheme: dark) {{
      body {{
        background: #0f1420;
      }}
    }}
  </style>
</head>
<body>
  <article class="course-cover" role="img" aria-label="Обложка: {title_text}">
    <div class="bg-shape" aria-hidden="true"></div>
    <div class="accent-stripe" aria-hidden="true"></div>
    <div class="marker-dot" aria-hidden="true"></div>
    <header class="header">
      {logos_html}
    </header>
    <main class="content">
      <h1 class="title">{title_text}</h1>
    </main>
    <footer class="footer">
      <p class="subtitle">{subtitle_text}</p>
      <span class="badge">{badge_text}</span>
    </footer>
  </article>
</body>
</html>'''

COVER_SYSTEM_MESSAGE = (
    "Вы — эксперт по дизайну обложек для образовательных курсов и мероприятий. "
    "Ваша задача — создать HTML-код обложки в фирменном стиле НИУ ВШЭ.\n\n"
    "БРЕНД-ПРАВИЛА (из официального брендбука):\n"
    "- Основной цвет: тёмно-синий #0F2D69 / #102D69. Дополнительные: лаванда #DFC7F2, флуоресцентный #DCFF05\n"
    "- Лаванду и флуоресцентный НЕЛЬЗЯ использовать для текста\n"
    "- Шрифт: system-ui, -apple-system, sans-serif\n"
    "- Если заголовок — одно предложение, используйте нижний регистр\n"
    "- Минимальный контраст текста к фону: WCAG AA 4.5:1, предпочтительно AAA 7:1\n"
    "- Композиция: два слоя — 1) спокойный, округлый, мягкий, 2) тёмный, острый, направленный\n"
    "- Декоративные маркеры на пересечениях осей\n\n"
    "ПРАВИЛА ЛОГОТИПОВ:\n"
    "- Логотипы размещаются в белых контейнерах (padding: 10px, border-radius: 12px)\n"
    "- Порядок: сначала ВШЭ, затем партнёры (ФКН, DC и др.)\n"
    "- Все логотипы должны быть СОРАЗМЕРНЫ — визуально одинакового масштаба\n"
    "- Квадратные лого (ВШЭ) — height: 40px; широкие (ФКН, ~5:1) — height: 24px; DC — height: 36px\n"
    "- Охранная зона: вокруг логотипа не должно быть других элементов на расстоянии минимум 1/2 высоты лого\n"
    "- Позиция: верхний левый угол (основная рекомендация), gap: 16px между лого\n"
    "- Нельзя искажать пропорции, менять цвета или добавлять элементы к логотипу\n\n"
    "СТРУКТУРА ОБЛОЖКИ:\n"
    "- Формат 16:9, max-width: 800px, border-radius: 24px\n"
    "- Фоновая фигура (лавандовый круг, blur, opacity 0.35)\n"
    "- Акцентная полоса внизу (градиент)\n"
    "- Маркер-точка (верхний правый угол)\n"
    "- Хедер: логотипы в белых контейнерах\n"
    "- Центр: крупный заголовок\n"
    "- Футер: подзаголовок + бейдж\n"
    "- Адаптивность (media query для < 600px)\n\n"
    "Верните ТОЛЬКО JSON: {\"type\": \"HTML\", \"content\": \"<!DOCTYPE html>...\"}\n"
    "HTML должен быть полностью самодостаточный (inline стили, встроенные SVG-логотипы)."
)
