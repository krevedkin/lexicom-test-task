CREATE TABLE short_names
(
    name   VARCHAR,
    status INT
);

CREATE TABLE full_names
(
    name   VARCHAR,
    status INT
);


INSERT INTO short_names (name, status)
SELECT 'file' || g AS name,
       (random() > 0.5) ::int AS status
FROM generate_series(1, 700000) AS g;

INSERT INTO full_names (name)
SELECT 'file' || g || CASE
                          WHEN random() < 0.33 THEN '.txt'
                          WHEN random() < 0.66 THEN '.csv'
                          ELSE '.mp3'
    END AS name
FROM generate_series(1, 500000) AS g;