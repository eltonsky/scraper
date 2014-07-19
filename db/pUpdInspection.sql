
drop PROCEDURE IF EXISTS pUpdInspection;

DELIMITER //
CREATE PROCEDURE pUpdInspection(
	IN  p_sale_id                 int,
    IN  p_start                   VARCHAR(32),
    IN  p_end                     VARCHAR(32),
    IN  p_capture_date_time       VARCHAR(16)
)

    BEGIN
    	DECLARE v_inspect_id INT DEFAULT 0;

    	DECLARE exit handler for sqlexception
		BEGIN
		  select -1,v_inspect_id;
		END;

		select 
			inspection_id
		into
			v_inspect_id
		from
			tinspection
		WHERE
			p_sale_id = sale_id
		and p_start = start
		and p_end = end;

		-- insert
		IF v_inspect_id = 0 then

			INSERT INTO tinspection(
				sale_id,
				start,
				end,
				capture_date_time)
	  		VALUES (
	  			p_sale_id,
	  			p_start,
	  			p_end,
	  			p_capture_date_time
	  		);

	  		set v_inspect_id = LAST_INSERT_ID();

		END IF;

		select 0,v_inspect_id;

    END //
DELIMITER ;

