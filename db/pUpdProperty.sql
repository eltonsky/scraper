
drop PROCEDURE if exists pUpdProperty;

DELIMITER //
CREATE PROCEDURE pUpdProperty(
	IN  p_ext_id                     int,
	IN  p_addr_id                    int, 
    IN  p_land_size                  VARCHAR(128), 
    IN  p_type                       VARCHAR(32),
    IN  p_capture_date_time          VARCHAR(16)
)

    BEGIN

    	DECLARE v_property_id INT DEFAULT 0;
    	DECLARE v_status INT DEFAULT 0;

		select 
			prop_id
		into
			v_property_id
		from
			tproperty
		WHERE
			p_addr_id = addr_id
		and p_type = type;
		-- don't need to check p_ext_id, because for each sale it's different

		-- insert
		IF v_property_id = 0 then

			INSERT INTO tproperty(
				ext_id,
				addr_id,
				type,
				land_size,
				capture_date_time)
	  		VALUES (
	  			p_ext_id,
	  			p_addr_id,
	  			p_type,
	  			p_land_size,
	  			p_capture_date_time
	  		);

	  		set v_property_id = LAST_INSERT_ID();
	  		set v_status = 0;

	  	ELSE
	  		set v_status = -1;

		END IF;

		select v_status,v_property_id;

    END //
DELIMITER ;