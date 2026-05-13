-- Миграция: добавление колонки "Отмена" в таблицу peresdachi
-- Выполните этот скрипт в SQL Editor в Supabase Dashboard
-- если таблица peresdachi уже существует без этой колонки

ALTER TABLE peresdachi
ADD COLUMN IF NOT EXISTS "Отмена" TEXT;
