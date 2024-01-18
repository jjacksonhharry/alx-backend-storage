-- 2-fans.sql

-- Create a temporary table to store the results
SELECT origin, nb_fans
FROM metal_bands
ORDER BY nb_fans DESC;
