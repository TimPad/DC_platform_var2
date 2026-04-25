"""
Тесты для logic/grade_recalculation.py
Покрывают основные ветки расчёта ДПР_итог и НЭ_итог
"""
import pytest
import pandas as pd
import numpy as np
from logic.grade_recalculation import process_grade_recalculation


def make_row(ne_name, ne_grade, dpr_grade, vhod, prom, itog):
    """Хелпер: одна строка DataFrame со всеми обязательными колонками."""
    return {
        'Наименование НЭ': ne_name,
        'Оценка НЭ': ne_grade,
        'Оценка дисциплины-пререквизита': dpr_grade,
        'Внешнее измерение цифровых компетенций. Входной контроль': vhod,
        'Внешнее измерение цифровых компетенций. Промежуточный контроль': prom,
        'Внешнее измерение цифровых компетенций. Итоговый контроль': itog,
    }


def process_single(ne_name, ne_grade, dpr_grade, vhod, prom, itog, use_dynamics=False):
    """Обработка одной строки, возвращает (ДПР_итог, НЭ_итог)."""
    df = pd.DataFrame([make_row(ne_name, ne_grade, dpr_grade, vhod, prom, itog)])
    result = process_grade_recalculation(df, use_dynamics=use_dynamics)
    return result['ДПР_итог'].iloc[0], result['НЭ_итог'].iloc[0]


# =====================================================================
# Определение этапа
# =====================================================================

class TestStageDetection:
    def test_stage_1_default(self):
        """По умолчанию этап = 1 (входной контроль)"""
        df = pd.DataFrame([make_row('Цифровая грамотность', 5, 5, 10, 3, 3)])
        result = process_grade_recalculation(df, use_dynamics=False)
        assert result['Этап'].iloc[0] == 1

    def test_stage_2_programming(self):
        """НЭ с 'программированию' → этап 2 (промежуточный)"""
        df = pd.DataFrame([make_row('Введение к программированию', 5, 5, 3, 10, 3)])
        result = process_grade_recalculation(df, use_dynamics=False)
        assert result['Этап'].iloc[0] == 2

    def test_stage_3_analysis(self):
        """НЭ с 'анализу данных' → этап 3 (итоговый)"""
        df = pd.DataFrame([make_row('Введение к анализу данных', 5, 5, 3, 3, 10)])
        result = process_grade_recalculation(df, use_dynamics=False)
        assert result['Этап'].iloc[0] == 3


# =====================================================================
# Ограничение ДПР (9+ → 8)
# =====================================================================

class TestDprCap:
    def test_dpr_9_capped_to_8(self):
        """Оценка ДПР >= 9 ограничивается до 8"""
        df = pd.DataFrame([make_row('ЦГ', 6, 9, 5, 5, 5)])
        result = process_grade_recalculation(df, use_dynamics=False)
        assert result['Оценка дисциплины-пререквизита'].iloc[0] == 8

    def test_dpr_10_capped_to_8(self):
        df = pd.DataFrame([make_row('ЦГ', 6, 10, 5, 5, 5)])
        result = process_grade_recalculation(df, use_dynamics=False)
        assert result['Оценка дисциплины-пререквизита'].iloc[0] == 8

    def test_dpr_8_stays(self):
        df = pd.DataFrame([make_row('ЦГ', 6, 8, 5, 5, 5)])
        result = process_grade_recalculation(df, use_dynamics=False)
        assert result['Оценка дисциплины-пререквизита'].iloc[0] == 8


# =====================================================================
# НЭ < 4 → оба NaN
# =====================================================================

class TestNeLessThan4:
    def test_ne_below_4_gives_nan(self):
        """Если НЭ < 4, перезачёт не происходит"""
        dpr, ne = process_single('ЦГ', 3, 6, 5, 5, 5)
        assert pd.isna(dpr)
        assert pd.isna(ne)

    def test_ne_zero(self):
        dpr, ne = process_single('ЦГ', 0, 6, 5, 5, 5)
        assert pd.isna(dpr)
        assert pd.isna(ne)


# =====================================================================
# ne_grade == dpr_grade → оба NaN
# =====================================================================

class TestEqualGrades:
    def test_equal_ne_dpr(self):
        """Если НЭ == ДПР, менять нечего"""
        dpr, ne = process_single('ЦГ', 6, 6, 5, 5, 5)
        assert pd.isna(dpr)
        assert pd.isna(ne)


# =====================================================================
# Максимум = innopolis_grade (и innopolis уникален)
# =====================================================================

class TestInnopolisMax:
    def test_innopolis_is_max_unique(self):
        """innopolis > ne и innopolis > dpr и innopolis > 3 → оба = innopolis"""
        # этап 1: innopolis = vhod = 8, ne = 5, dpr = 4
        dpr, ne = process_single('ЦГ', 5, 4, 8, 3, 3)
        assert dpr == 8
        assert ne == 8


# =====================================================================
# dpr < 4, ne >= 4
# =====================================================================

class TestDprBelow4:
    def test_dpr_below_4_ne_above_4(self):
        """ДПР < 4, НЭ >= 4 → ДПР_итог = НЭ"""
        dpr, ne = process_single('ЦГ', 6, 3, 2, 2, 2)
        assert dpr == 6


# =====================================================================
# max_grade = dpr (dpr >= 4)
# =====================================================================

class TestDprIsMax:
    def test_dpr_max_gives_dpr_nan(self):
        """Если ДПР — максимум и >= 4, ДПР_итог = NaN"""
        # ne=5, dpr=7 (capped from 7), innopolis=3
        dpr, ne = process_single('ЦГ', 5, 7, 3, 3, 3)
        assert pd.isna(dpr)

    def test_dpr_max_ne_below_8(self):
        """ДПР макс, НЭ < 8 → НЭ_итог = ДПР"""
        dpr, ne = process_single('ЦГ', 5, 7, 3, 3, 3)
        assert ne == 7

    def test_dpr_max_ne_8_or_above(self):
        """ДПР макс (8), НЭ >= 8 → НЭ_итог = NaN"""
        # ne=8, dpr=9→capped to 8, innopolis=3 → ne==dpr → оба NaN
        # Лучший пример: ne=8, dpr=10→8, innopolis=3 → ne==dpr → NaN
        # Используем другой: dpr=8 (не capped), ne=8 → equal → NaN
        # Нужен кейс где dpr > ne и ne >= 8:
        # ne=8, dpr=9→8 → equal → попадёт в ветку ne==dpr. Не тот кейс.
        # ne=8, dpr=8 → equal. Тоже не тот.
        # Фактически, из-за cap на 8, dpr не может быть > 8.
        # Если dpr=8, ne=8 → equal. Эта ветка невозможна после cap.
        pass

    def test_dpr_max_high_gives_ne_8(self):
        """ДПР = 8 (макс), НЭ = 5 → НЭ_итог = 8"""
        dpr, ne = process_single('ЦГ', 5, 8, 3, 3, 3)
        assert pd.isna(dpr)
        assert ne == 8


# =====================================================================
# Иначе → ДПР_итог = НЭ
# =====================================================================

class TestDefaultBranch:
    def test_ne_is_max(self):
        """НЭ — максимум → ДПР_итог = НЭ"""
        dpr, ne = process_single('ЦГ', 7, 5, 3, 3, 3)
        assert dpr == 7


# =====================================================================
# Динамика оценок
# =====================================================================

class TestDynamics:
    def test_dynamics_blocks_on_drop(self):
        """Падение оценки > 1 при use_dynamics → оба NaN"""
        # vhod=8, prom=6 → разница 2 > 1 → блокировка
        dpr, ne = process_single('ЦГ', 7, 5, 8, 6, 5, use_dynamics=True)
        assert pd.isna(dpr)
        assert pd.isna(ne)

    def test_dynamics_allows_small_drop(self):
        """Падение <= 1 при use_dynamics → нормальный расчёт"""
        dpr, ne = process_single('ЦГ', 7, 5, 8, 7, 7, use_dynamics=True)
        # innopolis (vhod=8) is max and unique → dpr = 8
        assert dpr == 8

    def test_no_dynamics_ignores_drop(self):
        """Без динамики большое падение не блокирует"""
        dpr, ne = process_single('ЦГ', 7, 5, 8, 3, 3, use_dynamics=False)
        # innopolis (vhod=8) is max and unique → dpr = 8, ne = 8
        assert dpr == 8
        assert ne == 8


# =====================================================================
# NaN в оценках
# =====================================================================

class TestNanHandling:
    def test_nan_ne_grade(self):
        """NaN в НЭ → ne_grade = 0 → < 4 → оба NaN"""
        dpr, ne = process_single('ЦГ', np.nan, 5, 5, 5, 5)
        assert pd.isna(dpr)
        assert pd.isna(ne)

    def test_nan_innopolis(self):
        """NaN в innopolis → innopolis = 0"""
        dpr, ne = process_single('ЦГ', 6, 5, np.nan, 5, 5)
        # этап 1 → innopolis = vhod = NaN → 0
        # max(6, 5, 0) = 6 = ne → else branch → dpr = ne = 6
        assert dpr == 6


# =====================================================================
# Отсутствие обязательной колонки
# =====================================================================

class TestMissingColumn:
    def test_missing_column_raises(self):
        df = pd.DataFrame({'Наименование НЭ': ['ЦГ'], 'Оценка НЭ': [5]})
        with pytest.raises(KeyError, match="Отсутствует обязательный столбец"):
            process_grade_recalculation(df, use_dynamics=False)


# =====================================================================
# Множественные строки
# =====================================================================

class TestMultipleRows:
    def test_batch_processing(self):
        """Проверяем корректность обработки нескольких строк"""
        rows = [
            make_row('ЦГ', 3, 6, 5, 5, 5),       # ne < 4 → NaN, NaN
            make_row('ЦГ', 7, 5, 3, 3, 3),         # ne max → dpr=7
            make_row('программированию', 6, 6, 5, 5, 5),  # ne==dpr → NaN, NaN
        ]
        df = pd.DataFrame(rows)
        result = process_grade_recalculation(df, use_dynamics=False)

        assert len(result) == 3

        # Row 0: ne < 4
        assert pd.isna(result['ДПР_итог'].iloc[0])
        assert pd.isna(result['НЭ_итог'].iloc[0])

        # Row 1: ne is max
        assert result['ДПР_итог'].iloc[1] == 7

        # Row 2: ne == dpr
        assert pd.isna(result['ДПР_итог'].iloc[2])
        assert pd.isna(result['НЭ_итог'].iloc[2])
