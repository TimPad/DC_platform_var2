"""
Внешняя оценка (Проекты) одной командой: выгрузка из edu.hse.ru → обработка → Supabase.

Делает то же, что вкладка «Для 3 курса (Проекты)» на странице 4, но для всех курсов сразу:
  1. Скачивает оценки курсов (scripts/download_moodle_grades.py) — или берёт готовые файлы из --from-dir.
  2. Склеивает файлы курсов в одну таблицу (logic.external_assessment.combine_grade_exports).
  3. Считает итоговые оценки (process_project_assessment), убирает дубликаты, находит новые записи.
  4. Сохраняет новые записи в peresdachi и обновляет final_grades.
  5. Кладёт Projects_All_*.xlsx и Projects_New_*.xlsx рядом с выгрузкой — для заявки на загрузку оценок.

Нужен .streamlit/secrets.toml с доступом к Supabase (как для локального запуска приложения).

Запуск из корня проекта:
    python scripts/sync_external_assessment.py --dry-run          # всё, кроме записи в Supabase
    python scripts/sync_external_assessment.py                    # полный цикл
    python scripts/sync_external_assessment.py --headless         # без окна браузера (сессия ЛК активна)
    python scripts/sync_external_assessment.py --from-dir grades_export/2026-11-14   # без скачивания
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)  # st.secrets ищет .streamlit/secrets.toml в текущей папке

# Вне `streamlit run` Streamlit пишет предупреждения про отсутствие runtime — они безвредны.
from streamlit.logger import set_log_level  # noqa: E402

set_log_level(logging.ERROR)

import pandas as pd  # noqa: E402

from download_moodle_grades import COURSE_IDS, default_out_dir, download_courses  # noqa: E402
from logic.external_assessment import (  # noqa: E402
    combine_grade_exports,
    deduplicate_and_split,
    process_project_assessment,
    save_to_supabase,
    update_final_grades,
)
from logic.student_management import load_students_from_supabase  # noqa: E402

STUDENT_COURSES = ["Курс 2", "Курс 3", "Курс 4"]  # как на странице 4
GRADE_FILE_SUFFIXES = {".csv", ".xlsx", ".xls"}
SECRETS_PATHS = [PROJECT_ROOT / ".streamlit" / "secrets.toml", Path.home() / ".streamlit" / "secrets.toml"]


def read_grade_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp1251")


def find_grade_files(folder: Path) -> list[Path]:
    return sorted(
        p for p in folder.iterdir()
        if p.suffix.lower() in GRADE_FILE_SUFFIXES and not p.name.startswith(("Projects_", "~$"))
    )


def write_xlsx(df: pd.DataFrame, path: Path) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Выгрузка и обработка внешней оценки (Проекты)")
    parser.add_argument("course_ids", nargs="*", help="ID курсов (по умолчанию — все из download_moodle_grades)")
    parser.add_argument("--from-dir", type=Path, help="Не скачивать, взять CSV/XLSX из этой папки")
    parser.add_argument("--out", type=Path, help="Папка для выгрузки и результатов")
    parser.add_argument("--dry-run", action="store_true", help="Посчитать и сохранить XLSX, но не писать в Supabase")
    parser.add_argument("--headless", action="store_true", help="Скачивать без окна браузера")
    parser.add_argument("--channel", default=None, help="'chrome' — использовать установленный Google Chrome")
    args = parser.parse_args()

    if not any(p.exists() for p in SECRETS_PATHS):
        print("Не найден .streamlit/secrets.toml с доступом к Supabase — без него оценки не обработать.")
        return 2

    # 1. Файлы с оценками
    if args.from_dir:
        out_dir = args.out or args.from_dir
        files = find_grade_files(args.from_dir)
        failed_courses: list[str] = []
    else:
        out_dir = args.out or default_out_dir()
        course_ids = args.course_ids or COURSE_IDS
        files, failed_courses = download_courses(course_ids, out_dir, headless=args.headless, channel=args.channel)
    if not files:
        print("Нет файлов с оценками для обработки.")
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    # 2. Склейка
    combined = combine_grade_exports([read_grade_file(path) for path in files])
    print(f"\nФайлов: {len(files)}, студентов после склейки: {len(combined)}")

    # 3. Обработка — та же логика, что на странице 4
    students_df = load_students_from_supabase(filters={"курс": STUDENT_COURSES})
    if students_df.empty:
        print("Список студентов в Supabase пуст — обработка остановлена.")
        return 1
    result_df, logs = process_project_assessment(combined, students_df)
    for message in logs:
        print(f"  {message}")
    if result_df.empty:
        print("Нет строк с оценками и за задание, и за тест — сохранять нечего.")
        return 0 if not failed_courses else 1

    split = deduplicate_and_split(result_df)
    print(
        f"Итоговых оценок: {split['total_count']}, новых для peresdachi: {split['new_count']}"
        + (f", удалено дубликатов: {split['duplicates_removed']}" if split["duplicates_removed"] else "")
    )

    stamp = datetime.now().strftime("%d-%m-%Y")
    all_path = out_dir / f"Projects_All_{stamp}.xlsx"
    new_path = out_dir / f"Projects_New_{stamp}.xlsx"
    write_xlsx(split["result_df"], all_path)
    write_xlsx(split["display_new_records"], new_path)
    print(f"Сохранено: {all_path}\nСохранено: {new_path}")

    # 4. Запись в Supabase
    exit_code = 0 if not failed_courses else 1
    if args.dry_run:
        print("\n--dry-run: в Supabase ничего не записано.")
    else:
        save_success, save_msg = True, "Новых записей нет"
        if not split["display_new_records"].empty:
            save_success, save_msg = save_to_supabase(split["display_new_records"])
        print(f"peresdachi: {save_msg}")
        if save_success:
            fg_success, fg_updated, fg_msg = update_final_grades(split["result_df"])
            print(f"final_grades: {fg_msg} ({fg_updated})")
            if not fg_success:
                exit_code = 1
        else:
            exit_code = 1

    if failed_courses:
        print("Не скачались курсы:", ", ".join(failed_courses))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
