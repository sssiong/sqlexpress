-- test cte with output tables from earlier examples

with cte1 as (
    select user_id
    , amount_round
    , amount_ceil
    , create_hour
    from `project.dataset.example2`
    where create_hour > 20
),

cte2 as (
    select user_id, age
    from `project.dataset.example3`
    where age > 18
)

select a.*
, b.*
from cte1 a join cte2 as b
on a.user_id = b.user_id