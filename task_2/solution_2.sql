WITH matched_names AS (
    SELECT
        fn.name AS full_name,
        sn.status AS status
    FROM
        full_names AS fn
    JOIN
        short_names AS sn
    ON
        sn.name = split_part(fn.name, '.', 1)
)
UPDATE full_names AS fn
SET status = mn.status
FROM matched_names AS mn
WHERE fn.name = mn.full_name;

