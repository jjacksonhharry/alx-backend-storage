-- 101-average_weighted_score.sql

-- Create the stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_var INT;
    
    -- Declare cursor for users
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    
    -- Declare variables for weighted average calculation
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    
    -- Initialize variables
    SET total_weighted_score = 0;
    SET total_weight = 0;
    
    -- Open cursor
    OPEN user_cursor;
    
    -- Loop through users
    user_loop: LOOP
        -- Fetch next user_id
        FETCH user_cursor INTO user_id_var;
        
        -- Exit loop if no more users
        IF user_id_var IS NULL THEN
            LEAVE user_loop;
        END IF;
        
        -- Calculate weighted average score for each user
        SELECT SUM(c.score * p.weight) INTO total_weighted_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id_var;
        
        SELECT SUM(p.weight) INTO total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id_var;
        
        -- Update average_score in the users table
        UPDATE users
        SET average_score = IFNULL(total_weighted_score / NULLIF(total_weight, 0), 0)
        WHERE id = user_id_var;
    END LOOP;
    
    -- Close cursor
    CLOSE user_cursor;
    
END //

DELIMITER ;
