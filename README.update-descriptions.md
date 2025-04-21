
Use this query against the peertube postgres database to make sure the filename is part of the title
(API search would not find it in descriptions):

```sql
UPDATE video
SET name =
    CASE
        WHEN video.name LIKE '%' || subquery.filename || '%' THEN video.name
        ELSE video.name || ' - ' || subquery.filename
    END
FROM (
    SELECT
        id,
        -- Extract the filename using the corrected regex
        CASE
            WHEN regexp_match(description, '^([\w]+\.(mp4|mkv|avi|mov|flv|wmv))', 'i') IS NOT NULL
            THEN (regexp_match(description, '^([\w]+\.(mp4|mkv|avi|mov|flv|wmv))', 'i'))[1]
            ELSE NULL
        END AS filename
    FROM video
) AS subquery
WHERE video.id = subquery.id
  AND subquery.filename IS NOT NULL; -- Only update rows with valid filenames
```

connection:

```bash
rngadam in 🌐 nixos02 in ~
❯ sudo su - postgres

[postgres@nixos02:~]$ psql
psql (16.6)
Type "help" for help.
postgres=# \c peertube_local
You are now connected to database "peertube_local" as user "postgres".
```

on peut aussi utiliser la correspondance entre uuid et nom de fichier:

```
SELECT
    uuid,
    (regexp_match(description, '^([\w]+\.(mp4|mkv|avi|mov|flv|wmv))', 'i'))[1] AS filename
FROM video
WHERE regexp_match(description, '^([\w]+\.(mp4|mkv|avi|mov|flv|wmv))', 'i') IS NOT NULL;
peertube_local=# \COPY (
    SELECT
        uuid,
        (regexp_match(description, '^([\w]+\.(mp4|mkv|avi|mov|flv|wmv))', 'i'))[1] AS filename
    FROM video
    WHERE regexp_match(description, '^([\w]+\.(mp4|mkv|avi|mov|flv|wmv))', 'i') IS NOT NULL
) TO '/tmp/output.csv' WITH CSV HEADER;
```
