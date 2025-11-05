-- SQL скрипт для создания таблицы peresdachi в Supabase
-- Выполните этот скрипт в SQL Editor в Supabase Dashboard

CREATE TABLE IF NOT EXISTS peresdachi (
    id BIGSERIAL PRIMARY KEY,
    "ФИО" TEXT,
    "Адрес электронной почты" TEXT,
    "Кампус" TEXT,
    "Факультет" TEXT,
    "Образовательная программа" TEXT,
    "Группа" TEXT,
    "Курс" TEXT,
    "ID дисциплины" TEXT,
    "Наименование дисциплины" TEXT,
    "Период аттестации" TEXT,
    "Оценка" TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Создание индексов для ускорения поиска
CREATE INDEX IF NOT EXISTS idx_peresdachi_email ON peresdachi("Адрес электронной почты");
CREATE INDEX IF NOT EXISTS idx_peresdachi_discipline ON peresdachi("Наименование дисциплины");
CREATE INDEX IF NOT EXISTS idx_peresdachi_fio ON peresdachi("ФИО");

-- Добавление комментария к таблице
COMMENT ON TABLE peresdachi IS 'Таблица для хранения данных о пересдачах внешней оценки';
