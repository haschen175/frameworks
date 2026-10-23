-- Список мероприятий
SELECT
    id,
    title,
    event_date,
    min_score
FROM events
ORDER BY title;

-- Список пользователей
SELECT
    id,
    full_name,
    email,
    role
FROM users
ORDER BY full_name;

-- Фильтр: мероприятия с проходным баллом не ниже 70
SELECT
    id,
    title,
    min_score
FROM events
WHERE min_score >= 70
ORDER BY min_score;

-- Фильтр: действующие сертификаты
SELECT
    id,
    number,
    event_id,
    user_id,
    issued_at
FROM certificates
WHERE is_revoked = 0
ORDER BY issued_at;

-- JOIN: сертификат, мероприятие, участник и балл
SELECT
    certificates.id,
    certificates.number,
    certificates.issued_at,
    certificates.is_revoked,
    events.title AS event_title,
    users.full_name AS user_name,
    results.score AS score
FROM certificates
JOIN events ON certificates.event_id = events.id
JOIN users ON certificates.user_id = users.id
JOIN results ON certificates.result_id = results.id
ORDER BY certificates.id;

-- JOIN: результаты участия с ФИО и названием мероприятия
SELECT
    results.id,
    results.score,
    results.passed,
    users.full_name AS user_name,
    events.title AS event_title
FROM results
JOIN users ON results.user_id = users.id
JOIN events ON results.event_id = events.id
ORDER BY results.id;

-- Агрегат: число действующих сертификатов
SELECT
    COUNT(*) AS active_certificates
FROM certificates
WHERE is_revoked = 0;

-- Агрегат: средний балл зачтённых результатов
SELECT
    ROUND(AVG(score), 1) AS average_score
FROM results
WHERE passed = 1;

-- GROUP BY: действующие сертификаты по мероприятиям
SELECT
    events.title AS event_title,
    COUNT(certificates.id) AS certificates_count
FROM events
LEFT JOIN certificates
    ON events.id = certificates.event_id
    AND certificates.is_revoked = 0
GROUP BY events.id, events.title
ORDER BY certificates_count DESC;

-- GROUP BY: число зачётов по мероприятиям
SELECT
    events.title AS event_title,
    COUNT(results.id) AS passed_count
FROM events
LEFT JOIN results
    ON events.id = results.event_id
    AND results.passed = 1
GROUP BY events.id, events.title
ORDER BY passed_count DESC;

-- HAVING: мероприятия, по которым выдано больше одного сертификата
SELECT
    events.title AS event_title,
    COUNT(certificates.id) AS certificates_count
FROM events
JOIN certificates ON events.id = certificates.event_id
GROUP BY events.id, events.title
HAVING COUNT(certificates.id) > 1
ORDER BY certificates_count DESC;

-- Подзапрос: мероприятия без действующего сертификата в выбранный день
-- В приложении дата передаётся параметром ?
SELECT
    id,
    title,
    event_date,
    min_score
FROM events
WHERE id NOT IN (
    SELECT event_id
    FROM certificates
    WHERE substr(issued_at, 1, 10) = '2026-10-15'
        AND is_revoked = 0
)
ORDER BY title;

-- Сортировка с ограничением выборки
SELECT
    id,
    title,
    event_date
FROM events
ORDER BY event_date
LIMIT 1 OFFSET 1;
