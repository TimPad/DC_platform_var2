-- Удаляем из аналитики по ЦГ студентов, которых нет в общей таблице
DELETE FROM course_cg
WHERE корпоративная_почта NOT IN (
    SELECT корпоративная_почта FROM students
);

-- Удаляем из аналитики по Питону студентов, которых нет в общей таблице
DELETE FROM course_python
WHERE корпоративная_почта NOT IN (
    SELECT корпоративная_почта FROM students
);

-- Удаляем из аналитики по Андану студентов, которых нет в общей таблице
DELETE FROM course_analysis
WHERE корпоративная_почта NOT IN (
    SELECT корпоративная_почта FROM students
);
