UPDATE full_names AS fn
SET status = sn.status
FROM short_names AS sn
WHERE sn.name = split_part(fn.name, '.', 1);