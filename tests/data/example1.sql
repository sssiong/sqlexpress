-- assume bigquery syntax

with cte1 as (
    select a.user_id
    , a.transaction_amount
    , a.transaction_timestamp
    , b.age
    , b.gender
    from `project.dataset.raw1` a
    join `project.dataset.profile` b
    on a.user_id = b.user_id
    where a.transaction_amount > 100
),

cte2 as (
    select a.user_id
    , a.transaction_amount
    , a.transaction_timestamp
    , b.age
    , b.gender
    from `project.dataset.raw2` a
    join `project.dataset.profile` b
    on a.user_id = b.user_id
    where a.transaction_amount > 100
)

select * from cte1
union all
select * from cte2
