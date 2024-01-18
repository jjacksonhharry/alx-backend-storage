-- 100-average_weighted_score.sql

-- Create the stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    
    -- Initialize variables
    SET total_weighted_score = 0;
    SET total_weight = 0;
    
    -- Calculate weighted average score
    SELECT SUM(c.score * p.weight) INTO total_weighted_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    SELECT SUM(p.weight) INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Update average_score in the users table
    UPDATE users
    SET average_score = IFNULL(total_weighted_score / NULLIF(total_weight, 0), 0)
    WHERE id = user_id;
END //

DELIMITER ;
