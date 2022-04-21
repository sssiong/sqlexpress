-- test union & subqueries

SELECT user_id, age
FROM `project.dataset.raw5`
JOIN ( -- subquery in "join"
    SELECT user_id FROM `project.dataset.raw6`
)

UNION ALL

SELECT user_id, age
FROM `project.dataset.raw7`
WHERE user_id IN ( -- subquery in "where"
    SELECT user_id FROM `project.dataset.raw8`
)