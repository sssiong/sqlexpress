-- test multiple scenarios below

SeLeCt a.user_id                                  -- mix upper & lower case
, round(a.amount, 3) aS amount_round              -- single brackets
, round(ceil(a.amount, 2), 3) As amount_ceil      -- double brackets
, eXtRaCt(hOuR fRoM b.create_time) aS create_hour -- not "from" keyword
fRoM `project.dataset.raw3` as a                  -- "as"
lEfT jOiN `project.dataset.raw4` b                -- "join" (without "as")
On a.user_id = b.user_id
wHeRe a.amount > 100
oRdEr By user_id, amount_round