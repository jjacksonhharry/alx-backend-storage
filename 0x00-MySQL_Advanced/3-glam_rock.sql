-- 3-glam_rock.sql

-- Create a temporary table to store the results
CREATE TEMPORARY TABLE IF NOT EXISTS glam_rock_bands AS (
    SELECT
        band_name,
        IFNULL(
            IF(split IS NOT NULL AND formed IS NOT NULL, 2022 - SPLIT(formed, '-', 1), NULL),
            IF(split IS NULL AND formed IS NOT NULL, 2022 - formed, NULL)
        ) AS lifespan
    FROM metal_bands
    WHERE style LIKE '%Glam rock%'
);

-- Select the results from the temporary table, ordering by lifespan in descending order
SELECT band_name, lifespan
FROM glam_rock_bands
ORDER BY lifespan DESC;
