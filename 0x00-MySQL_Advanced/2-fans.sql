-- 2-fans.sql

-- Create a temporary table to store the results
CREATE TEMPORARY TABLE IF NOT EXISTS temp_results AS (
    SELECT origin, COUNT(*) AS nb_fans
    FROM bands
    GROUP BY origin
    ORDER BY nb_fans DESC
);

-- Select the results from the temporary table
SELECT * FROM temp_results;
