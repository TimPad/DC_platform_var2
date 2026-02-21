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

# Шаблон для анонса вебинаров НИУ ВШЭ
WEBINAR_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Заголовок</title>
  <style type="text/css">
    body {
      margin: 0;
      padding: 0;
      font-family: Arial, Helvetica, sans-serif;
      background-color: #f5f7fa;
      color: #1a1a1a;
    }
    .container {
      max-width: 600px;
      margin: 0 auto;
      background-color: #ffffff;
    }
    .header {
      background: linear-gradient(135deg, #0033A0 0%, #0055D4 100%);
      color: white;
      text-align: center;
      padding: 40px 20px 30px;
      position: relative;
      overflow: hidden;
    }
    .header h1 {
      margin: 0;
      font-size: 28px;
      font-weight: bold;
    }
    .header .subtitle {
      font-size: 18px;
      margin: 12px 0 0;
      opacity: 0.95;
    }
    .circles {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      pointer-events: none;
    }
    .circle {
      position: absolute;
      border-radius: 50%;
      background: rgba(255,255,255,0.12);
    }
    .content {
      padding: 30px 20px;
    }
    .events-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      margin: 30px 0;
    }
    .card {
      flex: 1 1 48%;
      background-color: #f0f5ff;
      border-radius: 12px;
      padding: 24px 20px;
      box-sizing: border-box;
      min-width: 260px;
    }
    .label-online {
      display: inline-block;
      background-color: #e6f0ff;
      color: #0033A0;
      font-size: 13px;
      font-weight: bold;
      padding: 4px 10px;
      border-radius: 12px;
      margin-bottom: 12px;
    }
    .date {
      font-size: 15px;
      color: #0033A0;
      font-weight: bold;
      margin: 8px 0 12px;
    }
    .title {
      font-size: 20px;
      margin: 0 0 12px;
      line-height: 1.3;
    }
    .desc {
      font-size: 15px;
      color: #444;
      line-height: 1.45;
      margin: 0 0 16px;
    }
    .btn {
      display: inline-block;
      background-color: #0033A0;
      color: white;
      font-weight: bold;
      padding: 10px 20px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 15px;
    }
    .btn:hover {
      background-color: #002080;
    }
    .past-webinars {
      margin: 40px 0 20px;
      padding: 20px;
      background-color: #f8f9fa;
      border-radius: 12px;
    }
    .past-webinars h3 {
      margin: 0 0 16px;
      color: #0033A0;
    }
    .past-list {
      margin: 0;
      padding-left: 20px;
      line-height: 1.6;
    }
    .past-list li {
      margin-bottom: 10px;
    }
    .feedback {
      text-align: center;
      margin: 40px 0 20px;
      font-size: 15px;
      color: #444;
    }
    .stars {
      font-size: 28px;
      margin: 12px 0;
    }
    .footer {
      text-align: center;
      padding: 20px;
      font-size: 13px;
      color: #666;
      border-top: 1px solid #eee;
    }
    @media (max-width: 600px) {
      .card { flex: 1 1 100%; }
    }
  </style>
</head>
<body>

<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f5f7fa;">
  <tr><td align="center">

    <table class="container" cellpadding="0" cellspacing="0" border="0">
      <!-- Шапка -->
      <tr>
        <td class="header">
          <div class="circles">
            <div class="circle" style="width:180px;height:180px;top:-60px;left:-60px;"></div>
            <div class="circle" style="width:120px;height:120px;bottom:-40px;right:-40px;"></div>
            <div class="circle" style="width:80px;height:80px;top:40px;right:20px;"></div>
          </div>
          <h1>Вебинары НИУ ВШЭ</h1>
          <div class="subtitle">Ближайшие онлайн-мероприятия</div>
        </td>
      </tr>

      <!-- Контент -->
      <tr>
        <td class="content">

          <div style="text-align:center; margin-bottom:30px;">
            <a href="#" style="color:#0033A0; font-weight:bold; text-decoration:none;">Все мероприятия →</a>
          </div>

          <div class="events-grid">

            <!-- Карточка 1 -->
            <div class="card">
              <div class="label-online">Онлайн</div>
              <div class="date">5 февраля 12:00 (МСК)</div>
              <h3 class="title">Название вебинара</h3>
              <p class="desc">Краткое описание вебинара и его тематики.</p>
              <a href="#" class="btn">Зарегистрироваться →</a>
            </div>

            <!-- Карточка 2 -->
            <div class="card">
              <div class="label-online">Онлайн</div>
              <div class="date">12 февраля 12:00 (МСК)</div>
              <h3 class="title">Название вебинара</h3>
              <p class="desc">Краткое описание вебинара и его тематики.</p>
              <a href="#" class="btn">Зарегистрироваться →</a>
            </div>

          </div>

          <!-- Прошедшие вебинары -->
          <div class="past-webinars">
            <h3>Записи прошедших вебинаров для вас</h3>
            <ul class="past-list">
              <li>Название прошедшего вебинара 1</li>
              <li>Название прошедшего вебинара 2</li>
            </ul>
          </div>

        </td>
      </tr>

      <!-- Футер -->
      <tr>
        <td class="footer">
          © Национальный исследовательский университет «Высшая школа экономики»<br>
        </td>
      </tr>
    </table>

  </td></tr>
</table>

</body>
</html>"""

# Словарь шаблонов с метаданными для UI выбора
TEMPLATES = {
    "data_culture": {
        "name": "Горизонтальная сетка",
        "description": "Классическая вертикальная верстка с широкими информационными блоками и акцентным хедером. Подходит для длинных объявлений.",
        "icon": "",
        "html": HTML_EXAMPLE,
        "color": "#001A57",
        "preview_bg": "linear-gradient(135deg, #001a57 0%, #00256c 100%)"
    },
    "webinars": {
        "name": "Смешанная сетка",
        "description": "Компактная сетка из нескольких карточек в ряд. Идеально подходит для каталогов, анонсов мероприятий и списков событий.",
        "icon": "",
        "html": WEBINAR_TEMPLATE,
        "color": "#0033A0",
        "preview_bg": "linear-gradient(135deg, #0033A0 0%, #0055D4 100%)"
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
