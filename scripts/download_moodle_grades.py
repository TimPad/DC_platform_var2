"""
Автоматическая выгрузка оценок из курсов edu.hse.ru (Moodle → Экспорт оценок → «Текстовый файл»).

Как работает:
  * Открывает браузер (Playwright) с постоянным профилем в ~/.hse_moodle_profile —
    cookies сохраняются между запусками, поэтому входить в ЛК нужно только когда сессия истечёт.
  * При первом запуске (или если сессия протухла) скрипт остановится и попросит
    войти в edu.hse.ru вручную в открывшемся окне. Пароль скрипт не видит и не хранит.
  * Для каждого курса открывает страницу экспорта, жмёт #id_submitbutton
    и сохраняет файл в папку вывода (по умолчанию ./grades_export/ГГГГ-ММ-ДД/).

Установка (один раз, локально — на Streamlit Cloud это не нужно):
    pip install playwright
    playwright install chromium

Запуск:
    python scripts/download_moodle_grades.py                # все курсы из COURSE_IDS, с окном браузера
    python scripts/download_moodle_grades.py --headless     # без окна (когда вход уже выполнен)
    python scripts/download_moodle_grades.py 273033 310918  # только указанные курсы
    python scripts/download_moodle_grades.py --out ~/Desktop/grades

Полученные CSV можно загружать на страницу «Внешняя оценка» (pages/4_external_assessment.py).
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

BASE_URL = "https://edu.hse.ru/grade/export/txt/index.php?id={course_id}"
SUBMIT_SELECTOR = "#id_submitbutton"

COURSE_IDS = [
    "273033",
    "310918",
    "310919",
    "310898",
    "310925",
]

PROFILE_DIR = Path.home() / ".hse_moodle_profile"
DEFAULT_OUT_DIR = Path("grades_export")

PAGE_TIMEOUT_MS = 60_000
DOWNLOAD_TIMEOUT_MS = 180_000  # большие курсы Moodle собирает долго


def safe_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|\n\r\t]+', "_", name).strip(" ._")
    return name[:150] or "grades"


def is_export_form_ready(page) -> bool:
    try:
        page.wait_for_selector(SUBMIT_SELECTOR, state="visible", timeout=5_000)
        return True
    except PlaywrightTimeout:
        return False


def ensure_logged_in(page, first_course_id: str, headless: bool) -> None:
    """Открывает первый курс; если показан вход — ждёт, пока пользователь залогинится вручную."""
    url = BASE_URL.format(course_id=first_course_id)
    page.goto(url, timeout=PAGE_TIMEOUT_MS)
    if is_export_form_ready(page):
        return

    if headless:
        sys.exit(
            "Сессия edu.hse.ru не активна. Запустите скрипт без --headless "
            "и войдите в открывшемся окне браузера."
        )

    print("\nНужно войти в edu.hse.ru.")
    print("Выполните вход в открывшемся окне браузера, затем вернитесь сюда.")
    while True:
        input("Нажмите Enter, когда вход выполнен... ")
        page.goto(url, timeout=PAGE_TIMEOUT_MS)
        if is_export_form_ready(page):
            print("Вход выполнен, сессия сохранена в профиле.\n")
            return
        print(
            f"Кнопка экспорта ({SUBMIT_SELECTOR}) не найдена. Текущий адрес: {page.url}\n"
            "Проверьте, что вход завершён и у аккаунта есть доступ к оценкам курса."
        )


def course_title(page) -> str:
    for selector in (".page-header-headings h1", "#page-header h1", "header h1"):
        el = page.query_selector(selector)
        if el:
            text = el.inner_text().strip()
            if text:
                return text
    return page.title()


def download_course(page, course_id: str, out_dir: Path) -> Path | None:
    url = BASE_URL.format(course_id=course_id)
    page.goto(url, timeout=PAGE_TIMEOUT_MS)
    if not is_export_form_ready(page):
        print(f"  [{course_id}] нет кнопки экспорта (нет доступа или сессия истекла): {page.url}")
        return None

    title = course_title(page)
    with page.expect_download(timeout=DOWNLOAD_TIMEOUT_MS) as dl_info:
        page.click(SUBMIT_SELECTOR)
    download = dl_info.value

    suffix = Path(download.suggested_filename).suffix or ".csv"
    target = out_dir / f"{course_id}_{safe_filename(title)}{suffix}"
    download.save_as(target)
    return target


def default_out_dir() -> Path:
    return DEFAULT_OUT_DIR / date.today().isoformat()


def download_courses(
    course_ids: list[str],
    out_dir: Path,
    headless: bool = False,
    channel: str | None = None,
) -> tuple[list[Path], list[str]]:
    """Скачивает выгрузки курсов. Возвращает (пути скачанных файлов, ID курсов с ошибкой)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    saved, failed = [], []
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=headless,
            channel=channel,
            accept_downloads=True,
        )
        page = context.pages[0] if context.pages else context.new_page()
        try:
            ensure_logged_in(page, course_ids[0], headless)
            for course_id in course_ids:
                print(f"Курс {course_id}...")
                try:
                    path = download_course(page, course_id, out_dir)
                except PlaywrightTimeout as exc:
                    print(f"  [{course_id}] таймаут: {exc}")
                    path = None
                if path:
                    print(f"  сохранено: {path}")
                    saved.append(path)
                else:
                    failed.append(course_id)
        finally:
            context.close()
    return saved, failed


def main() -> int:
    parser = argparse.ArgumentParser(description="Выгрузка оценок из edu.hse.ru")
    parser.add_argument("course_ids", nargs="*", help="ID курсов (по умолчанию — COURSE_IDS в скрипте)")
    parser.add_argument("--out", type=Path, default=None, help="Папка для файлов")
    parser.add_argument("--headless", action="store_true", help="Без окна браузера (нужна активная сессия)")
    parser.add_argument(
        "--channel",
        default=None,
        help="Браузер: по умолчанию Chromium из Playwright; 'chrome' — установленный Google Chrome",
    )
    args = parser.parse_args()

    course_ids = args.course_ids or COURSE_IDS
    out_dir = args.out or default_out_dir()
    ok, failed = download_courses(course_ids, out_dir, headless=args.headless, channel=args.channel)

    print(f"\nГотово: {len(ok)} из {len(course_ids)}. Папка: {out_dir.resolve()}")
    if failed:
        print("Не удалось скачать:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
