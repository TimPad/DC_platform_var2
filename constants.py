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
<style type="text/css">
	.st0{fill-rule:evenodd;clip-rule:evenodd;fill:#002F87;}
	.st1{fill:#FFFFFF;}
</style>
<g>

		<ellipse transform="matrix(0.6669 -0.7451 0.7451 0.6669 -10.5121 27.507)" class="st0" cx="25.51" cy="25.51" rx="24.87" ry="24.87"/>
	<path class="st1" d="M25.51,0C11.44,0,0,11.44,0,25.51c0,14.07,11.44,25.51,25.51,25.51c14.07,0,25.51-11.44,25.51-25.51
		C51.02,11.44,39.58,0,25.51,0z M25.51,50.7c-13.89,0-25.19-11.3-25.19-25.19c0-13.89,11.3-25.19,25.19-25.19
		c13.89,0,25.19,11.3,25.19,25.19C50.7,39.4,39.4,50.7,25.51,50.7z M25.51,0.32c-13.89,0-25.19,11.3-25.19,25.19
		c0,13.89,11.3,25.19,25.19,25.19c13.89,0,25.19-11.3,25.19-25.19C50.7,11.62,39.4,0.32,25.51,0.32z M25.51,50.38
		c-13.73,0-24.87-11.13-24.87-24.87S11.78,0.65,25.51,0.65c13.73,0,24.87,11.13,24.87,24.87S39.24,50.38,25.51,50.38z M28.5,23.97
		c1.13-0.46,1.82-1.18,2.27-1.72c0.86-0.99,1.21-2.2,1.21-3.35c0-0.93-0.26-2.78-1.88-4.06c-1.12-0.86-2.11-1.28-4.47-1.28h-1.2
		c-0.04,0-0.07,0-0.12,0h-4.94v23.3h14.09v-4.47C33.46,28.11,32.08,25.23,28.5,23.97z M30.27,35.58h-2.54V27.8H24.8v7.79h-2.25
		V14.72l2.31,0c0.86,0,2.17,0.19,3.1,1.34c0.48,0.58,0.78,1.36,0.88,2.13H24.8v1.15h4.08c-0.03,0.74-0.18,1.57-0.91,2.45
		c-0.64,0.8-1.69,1.54-3.17,1.54c-0.01,0-0.02,0-0.03,0v1.16c3.96,0,5.5,2.63,5.5,7.45V35.58z M20.81,47.22l-1.45-0.37
		c-0.43-0.13-0.73-0.37-0.89-0.65c-0.12-0.22-0.15-0.45-0.07-0.71c0.13-0.46,0.46-0.62,0.79-0.69c-0.4-0.28-0.64-0.63-0.48-1.15
		c0.2-0.68,0.86-0.88,1.71-0.63l1.49,0.43L20.81,47.22z M19.97,45.27c-0.43-0.12-0.76-0.04-0.87,0.32c-0.09,0.3,0.1,0.55,0.53,0.68
		l0.69,0.2l0.29-1.01L19.97,45.27z M20.24,43.6c-0.46-0.13-0.78-0.03-0.89,0.32c-0.09,0.32,0.11,0.58,0.63,0.74l0.79,0.23l0.3-1.04
		L20.24,43.6z M16.9,41.59c-0.79-0.46-1.54-0.33-1.94,0.36c-0.4,0.69-0.11,1.37,0.65,1.82l0.54,0.32l-0.72,1.23l0.59,0.35l2-3.41
		L16.9,41.59z M15.94,43.26c-0.45-0.27-0.6-0.61-0.39-0.96c0.23-0.38,0.6-0.43,1.04-0.17l0.53,0.31l-0.66,1.12L15.94,43.26z
		 M14.4,40.05l-2.27,3.23l0.56,0.4l2.27-3.23L14.4,40.05z M7.39,23.33L5.98,23.2l-0.04,0.48l0.93,0.78c0.46,0.39,0.55,0.85,0.4,1.18
		l-0.6,0.01c0.08-0.21-0.05-0.53-0.23-0.69l-0.69-0.59c-0.14,0.32-0.51,0.72-1.19,0.67c-0.68-0.06-1.2-0.45-1.12-1.52
		c0.01-0.11,0.1-0.98,0.14-1.2l3.91,0.31L7.39,23.33z M4.11,23.53c-0.05,0.56,0.21,0.75,0.51,0.78c0.41,0.03,0.64-0.3,0.67-0.7
		l0.04-0.45l-1.17-0.1C4.14,23.24,4.12,23.4,4.11,23.53z M10.46,37.86c0.44-0.09,0.89,0.03,1.23,0.4c0.53,0.58,0.44,1.42-0.12,1.94
		c-0.57,0.53-1.4,0.55-1.94-0.02c-0.33-0.35-0.42-0.81-0.31-1.23L8.63,38.8c-0.12,0.61,0.04,1.27,0.53,1.8
		c0.82,0.89,2.09,0.89,2.91,0.13c0.82-0.76,0.92-2.01,0.1-2.9c-0.51-0.55-1.18-0.76-1.81-0.66L10.46,37.86z M3.58,28.7l0.1,0.64
		l4.26,1.09l-0.18-0.72l-0.99-0.24l0,0c-0.06-0.3-0.12-0.61-0.17-0.92c-0.05-0.31-0.09-0.62-0.13-0.93l0,0l0.86-0.53l-0.05-0.76
		L3.58,28.7z M6.1,29.31L4.45,28.9l1.44-0.92c0.03,0.22,0.06,0.45,0.1,0.67C6.02,28.87,6.06,29.09,6.1,29.31z M7.82,32.11
		C8,32.6,8.2,33.08,8.43,33.56l-2.96,1.45c0.1,0.21,0.2,0.42,0.31,0.62l2.96-1.45c0.24,0.46,0.49,0.9,0.76,1.34l-2.97,1.47
		c0.12,0.2,0.24,0.39,0.37,0.59l2.98-1.47l0.58-0.29c-0.98-1.44-1.75-3-2.29-4.65l-0.58,0.29l-2.98,1.47
		c0.08,0.22,0.16,0.43,0.24,0.65L7.82,32.11z M43.78,16.55c1.04-0.39,2.21,0.09,2.64,1.23s-0.15,2.25-1.2,2.64
		c-1.04,0.39-2.21-0.09-2.64-1.23C42.16,18.06,42.73,16.94,43.78,16.55z M44.97,19.74c0.72-0.27,1.12-1.01,0.85-1.75
		c-0.27-0.74-1.05-1.03-1.78-0.76c-0.72,0.27-1.12,1.01-0.85,1.75C43.46,19.72,44.24,20.01,44.97,19.74z M45.82,27.02
		c1.1,0.19,1.86,1.2,1.65,2.4c-0.21,1.2-1.26,1.87-2.37,1.67c-1.1-0.19-1.86-1.2-1.65-2.4C43.66,27.5,44.72,26.82,45.82,27.02z
		 M45.23,30.37c0.76,0.13,1.48-0.31,1.62-1.08c0.14-0.77-0.39-1.42-1.15-1.56c-0.76-0.13-1.48,0.31-1.62,1.08
		C43.94,29.59,44.46,30.23,45.23,30.37z M42.07,15.65l0.41-1.28l2.4,0.34l-0.43-0.69l-2.11-0.24l-0.22-0.34l1.37-0.9l-0.42-0.56
		l-3.27,2.14l0.41,0.56l1.37-0.9l0.26,0.4l-0.41,1.17c-0.22,0.6-0.27,1.17,0.2,1.57l0.5-0.33C41.92,16.41,41.92,16.1,42.07,15.65z
		 M34.94,42.32l1.27,0.45l-0.4,2.39l0.7-0.41l0.29-2.1l0.34-0.21l0.86,1.4l0.57-0.4l-2.06-3.32l-0.57,0.39l0.86,1.39l-0.41,0.25
		l-1.16-0.44c-0.59-0.23-1.16-0.3-1.57,0.16l0.32,0.51C34.18,42.15,34.49,42.16,34.94,42.32z M42.98,39.16l-0.43,0.53l-2.1-1.93
		l0.64,3.52l-0.49,0.47l-2.89-2.65l0.5-0.47l2.12,1.95l-0.65-3.55l0.41-0.52L42.98,39.16z M33.95,46.01l-0.64,0.25l-0.87-2.72
		l-1.18,3.38l-0.66,0.17l-1.2-3.74l0.66-0.16l0.88,2.74l1.2-3.41l0.61-0.25L33.95,46.01z M42.6,35.62c0.47,0.2,1.03,0.45,1.51,0.69
		l0.01-0.02c-0.37-0.34-2.36-2.52-2.36-2.52l0.26-0.53c0,0,2.89,0.35,3.38,0.46l0.01-0.01c-0.46-0.25-1.01-0.55-1.48-0.81
		l-1.39-0.79l0.25-0.67l3.43,2.01l-0.38,0.93c0,0-2.68-0.29-3.12-0.39L42.71,34c0.34,0.29,2.18,2.29,2.18,2.29l-0.5,0.85l-3.66-1.53
		l0.39-0.63L42.6,35.62z M47.65,24.57l-1.64,0.15l-0.01,0c-0.01-0.38-0.04-0.75-0.07-1.13c-0.04-0.37-0.08-0.75-0.14-1.12l0.01,0
		l1.65-0.15l-0.11-0.69L43.44,22l0.11,0.69l1.61-0.15l0.02,0c0.06,0.37,0.1,0.75,0.14,1.12c0.04,0.37,0.06,0.75,0.07,1.13l-0.02,0
		l-1.61,0.15l0.02,0.7l3.9-0.37L47.65,24.57z M40.47,8.97c-0.54-0.49-1.2-0.64-1.8-0.51l0.15,0.69c0.42-0.11,0.87-0.02,1.23,0.3
		c0.5,0.45,0.56,1.13,0.23,1.68c-0.29-0.3-0.59-0.59-0.9-0.87c-0.13-0.12-0.26-0.23-0.39-0.35l-0.4,0.47
		c0.13,0.11,0.25,0.22,0.38,0.34c0.31,0.28,0.61,0.57,0.9,0.87c-0.51,0.38-1.21,0.39-1.71-0.07c-0.37-0.33-0.5-0.79-0.41-1.23
		l-0.69-0.1c-0.09,0.63,0.13,1.3,0.68,1.8c0.9,0.82,2.14,0.7,2.9-0.13C41.37,11.06,41.36,9.79,40.47,8.97z M17.31,6.92
		c-0.34-1.06,0.18-2.21,1.34-2.58c1.15-0.38,2.24,0.24,2.59,1.31c0.34,1.06-0.18,2.21-1.34,2.58C18.74,8.61,17.65,7.99,17.31,6.92z
		 M20.55,5.87c-0.24-0.73-0.97-1.16-1.71-0.92C18.09,5.19,17.76,5.96,18,6.7c0.24,0.73,0.97,1.16,1.71,0.92
		C20.46,7.38,20.79,6.61,20.55,5.87z M16.2,8.65L14.93,8.2l0.42-2.39l-0.7,0.4l-0.31,2.1l-0.34,0.21l-0.86-1.4l-0.57,0.4l2.04,3.33
		l0.58-0.39l-0.85-1.39l0.41-0.25l1.16,0.44c0.59,0.24,1.16,0.31,1.57-0.15l-0.31-0.52C16.95,8.82,16.64,8.81,16.2,8.65z
		 M12.56,11.8c-0.38,0.36-0.74,0.73-1.09,1.12l-2.49-2.16c-0.15,0.17-0.31,0.35-0.45,0.53l2.49,2.16c-0.33,0.39-0.64,0.8-0.94,1.22
		l-2.51-2.16c-0.14,0.19-0.27,0.38-0.4,0.57l2.51,2.18l0.49,0.42c0.94-1.46,2.08-2.78,3.39-3.92l-0.49-0.42l-2.52-2.17
		c-0.17,0.16-0.34,0.31-0.5,0.48L12.56,11.8z M29.93,3.79L29.3,3.67l-2.47,3.64l0.74,0.07l0.56-0.85l0,0
		c0.31,0.04,0.62,0.09,0.92,0.15c0.31,0.06,0.61,0.12,0.91,0.19l0,0l0.21,0.99l0.73,0.21L29.93,3.79z M28.5,5.96l0.95-1.42
		l0.38,1.66c-0.22-0.05-0.44-0.09-0.66-0.14C28.95,6.03,28.72,5.99,28.5,5.96z M24.58,3.36l-1.49,0.11c-0.03,0-0.07,0.01-0.1,0.01
		l0.05,0.62l0.01,0.16c0.18,2.36-0.17,2.64-0.57,2.67c-0.08,0.01-0.18,0-0.23-0.02l-0.02,0.57c0.11,0.02,0.33,0.04,0.48,0.03
		c0.78-0.06,1.19-0.59,1-3.1l-0.03-0.38c0.07-0.01,0.13-0.01,0.2-0.02c0.39-0.03,0.78-0.05,1.17-0.06l0.25,3.31l0.69-0.05
		l-0.25-3.26L25.7,3.34C25.33,3.34,24.95,3.34,24.58,3.36z M26.31,45.76c0-0.44-0.35-0.79-0.79-0.79c-0.44,0-0.79,0.35-0.79,0.79
		c0,0.44,0.35,0.79,0.79,0.79C25.96,46.55,26.31,46.2,26.31,45.76z M6.46,18.73c0.41,0.16,0.87-0.03,1.03-0.44
		c0.16-0.41-0.03-0.87-0.44-1.03C6.64,17.1,6.18,17.3,6.02,17.7C5.86,18.11,6.05,18.57,6.46,18.73z M33.94,7.13
		c-0.2,0.39-0.04,0.87,0.35,1.06c0.39,0.2,0.87,0.04,1.06-0.35c0.2-0.39,0.04-0.87-0.35-1.06C34.61,6.58,34.13,6.74,33.94,7.13z"/>
</g>
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
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: {logo_pad};
      border: {logo_border};
      border-radius: 8px;
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
    "- Логотипы размещаются БЕЗ белой подложки, на прозрачном фоне. На тёмно-синем фоне (#102D69) к каждому логотипу добавляется тонкая белая обводка: border: 1px solid #ffffff; padding: 4px; border-radius: 8px;. На светлых фонах (#DFC7F2, #DCFF05, #FFFFFF) обводка не нужна.\n"
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
    "- Хедер: логотипы без подложки (с белой обводкой только на тёмно-синем фоне)\n"
    "- Центр: крупный заголовок\n"
    "- Футер: подзаголовок + бейдж\n"
    "- Адаптивность (media query для < 600px)\n\n"
    "Верните ТОЛЬКО JSON: {\"type\": \"HTML\", \"content\": \"<!DOCTYPE html>...\"}\n"
    "HTML должен быть полностью самодостаточный (inline стили, встроенные SVG-логотипы)."
)
