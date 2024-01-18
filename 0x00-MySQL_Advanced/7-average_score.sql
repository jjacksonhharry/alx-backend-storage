-- 7-average_score.sql

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE v_total_score FLOAT;
    DECLARE v_total_projects INT;
    DECLARE v_average_score FLOAT;

    -- Compute the total score and total projects for the user
    SELECT SUM(score), COUNT(DISTINCT project_id)
    INTO v_total_score, v_total_projects
    FROM corrections
    WHERE user_id = p_user_id;

    -- Compute the average score
    IF v_total_projects > 0 THEN
        SET v_average_score = v_total_score / v_total_projects;
    ELSE
        SET v_average_score = 0;
    END IF;

    -- Update the average_score in the users table
    UPDATE users
    SET average_score = v_average_score
    WHERE id = p_user_id;
END;

//

DELIMITER ;
