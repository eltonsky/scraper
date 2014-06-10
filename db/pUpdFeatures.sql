
drop PROCEDURE IF EXISTS pUpdFeatures;

DELIMITER //
CREATE PROCEDURE pUpdFeatures(
	IN  p_sale_id                 int,
    IN  p_bed                     int,
    IN  p_bath                    int,
    IN  p_car_spaces              int,
    IN  p_land_size               VARCHAR(128),
    OUT o_status                  int
)

    BEGIN

    	DECLARE v_sale_id INT DEFAULT 0;

    	set o_status  = 0;

		select 
			sale_id
		into
			v_sale_id
		from
			tfeatures
		WHERE
			p_bed = bed
		and p_bath = bath
		and p_car_spaces = car_spaces
		and p_land_size = land_size
		and p_sale_id = sale_id;

		-- insert
		IF v_sale_id = 0 then

			INSERT INTO tfeatures(
				sale_id,
				bed,
				bath,
				car_spaces,
				land_size)
	  		VALUES (
	  			p_sale_id,
	  			p_bed,
	  			p_bath,
	  			p_car_spaces,
	  			p_land_size
	  		);

	  		if ROW_COUNT() <= 0 then
	  			set o_status = -1;
	  		end if;

		END IF;

    END //
DELIMITER ;

