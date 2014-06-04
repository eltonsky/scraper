
drop PROCEDURE pUpdProperty;

DELIMITER //
CREATE PROCEDURE pUpdProperty(
	IN  p_ext_id                     int,
	IN  p_addr_id                    int, 
    IN  p_land_size                  VARCHAR(128), 
    IN  p_type                       VARCHAR(32)
)


    BEGIN

    	DECLARE v_property_id INT DEFAULT 0;

		select 
			prop_id
		into
			v_property_id
		from
			tProperty
		WHERE
			p_addr_id = addr_id
		and p_ext_id = ext_id;

		-- insert
		IF v_property_id = 0 then
			INSERT INTO tProperty(
				ext_id,
				addr_id,
				type,
				land_size)
	  		VALUES (
	  			p_ext_id,
	  			p_addr_id,
	  			p_type,
	  			p_land_size
	  		);

	  		select 0,LAST_INSERT_ID();

	  	ELSE
	  		select -1,v_property_id;

		END IF;

    END //
DELIMITER ;