-- 4-store.sql

-- Create a trigger to decrease the quantity after inserting a new order
DELIMITER //

CREATE TRIGGER after_order_insert
AFTER INSERT ON orders FOR EACH ROW
BEGIN
    -- Decrease the quantity in the items table
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;

//

DELIMITER ;
