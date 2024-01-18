-- 9-index_name_score.sql

-- Create an index on the first letter of the name and the score columns
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);
