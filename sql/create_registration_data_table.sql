-- SQL скрипт для создания таблицы registration_data
-- Эта таблица содержит данные из "данные.xlsx", включая колонку "Отмена"

CREATE TABLE public.registration_data (
    id SERIAL PRIMARY KEY,
    "ФИО" TEXT,
    "Адрес электронной почты" TEXT NOT NULL,
    "Кампус" TEXT,
    "Факультет" TEXT,
    "Образовательная программа" TEXT,
    "Группа" TEXT,
    "Курс" TEXT,
    "ID дисциплины" TEXT,
    "Наименование дисциплины" TEXT,
    "Период аттестации" TEXT,
    "Дата сдачи" TEXT,
    "Сдача" TEXT,
    "ИсторияСдач" TEXT,
    "Отмена" TEXT,
    "Оценка" TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Настройка RLS (Row Level Security) если требуется
ALTER TABLE public.registration_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all read operations" ON public.registration_data
    FOR SELECT USING (true);

CREATE POLICY "Allow all insert operations" ON public.registration_data
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow all update operations" ON public.registration_data
    FOR UPDATE USING (true);

-- Создание индексов для быстрого поиска по email
CREATE INDEX IF NOT EXISTS idx_registration_data_email 
ON public.registration_data ("Адрес электронной почты");
