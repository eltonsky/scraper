
drop PROCEDURE IF EXISTS pUpdSale;

DELIMITER //
CREATE PROCEDURE pUpdSale(
	IN  p_prop_id                 int,
	IN  p_agency_id               int, 
    IN  p_status                  VARCHAR(128), 
    IN  p_price                   VARCHAR(32),
    IN  p_price_type              VARCHAR(16),
    IN  p_bed                     int,
    IN  p_bath                    int,
    IN  p_car_spaces              int,
    IN  p_land_size               VARCHAR(128),
    IN  p_capture_date_time       VARCHAR(16)
)

whole_proc:BEGIN

    	DECLARE v_sale_id INT DEFAULT 0;
    	DECLARE v_status INT DEFAULT 0;
    	DECLARE v_price_id INT DEFAULT 0;
    	DECLARE v_default_status VARCHAR(32) DEFAULT 'LIMITED';
    	DECLARE v_sale_status_id INT DEFAULT 0;

    	DECLARE exit handler for sqlexception
		BEGIN
		  ROLLBACK;
		  select -1,v_sale_id,v_price_id;
		END;

		select 
			sale_id
		into
			v_sale_id
		from
			tsale
		WHERE
			p_prop_id = prop_id
		and p_agency_id = agency_id;


		START TRANSACTION;

		-- insert
		IF v_sale_id = 0 then

			if p_status is null or p_status ='' then
				set p_status = v_default_status;
			end if;

			INSERT INTO tsale(
				prop_id,
				agency_id,
				status,
				capture_date_time)
	  		VALUES (
	  			p_prop_id,
	  			p_agency_id,
	  			p_status,
	  			p_capture_date_time
	  		);

	  		set v_sale_id = LAST_INSERT_ID();
	  		-- if v_sale_id > 0 then
	  		-- 	set v_status = 0;
	  		-- end if;

	  	ELSE

	  		UPDATE tsale
	  		set status = p_status
	  		where sale_id = v_sale_id;

		END IF;

		-- insert sale status
		Call pUpdSaleStatus(v_sale_id,p_status,p_capture_date_time, v_sale_status_id);
		if v_sale_status_id <= 0 then
			ROLLBACK;
			select -2,v_sale_id;
			LEAVE whole_proc;
		end if; 


  		-- insert features
  		Call pUpdFeatures(v_sale_id, p_bed, p_bath, p_car_spaces, p_land_size, v_status);
  		if v_status < 0 then
  			ROLLBACK;
  			select -3,v_sale_id;
  			LEAVE whole_proc;
  		end if;

  		-- insert price
  		Call pUpdPrice(v_sale_id,p_price,p_price_type,p_capture_date_time,v_status,v_price_id);

  		if v_sale_id > 0 and v_price_id > 0 then
  			COMMIT;
  		ELSE
  			ROLLBACK;
  			select -4,v_sale_id;
  			LEAVE whole_proc;
  		end if;

		select v_status,v_sale_id,v_price_id;

    END //
DELIMITER ;

