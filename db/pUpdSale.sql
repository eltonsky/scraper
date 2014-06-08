
drop PROCEDURE pUpdSale;

DELIMITER //
CREATE PROCEDURE pUpdSale(
	IN  p_prop_id                 int,
	IN  p_agency_id               int, 
    IN  p_status                  VARCHAR(128), 
    IN  p_price                   VARCHAR(32),
    IN  p_price_type              VARCHAR(16)
)

    BEGIN

    	DECLARE exit handler for sqlexception
		BEGIN
		  ROLLBACK;
		  select -1,v_sale_id,v_price_id;
		END;

    	DECLARE v_sale_id INT DEFAULT 0;
    	DECLARE v_status INT DEFAULT 0;
    	DECLARE v_price_id INT DEFAULT 0;
    	DECLARE v_default_status VARCHAR(32) DEFAULT 'LIMITED';

		select 
			sale_id
		into
			v_sale_id
		from
			tSale
		WHERE
			p_prop_id = prop_id
		and p_agency_id = agency_id;

		-- In REA each sale has a different ext_id.

		-- insert
		IF v_sale_id = 0 then

			if p_status is null or p_status ='' then
				set p_status = v_default_status;
			end if;

			START TRANSACTION;

			INSERT INTO tSale(
				prop_id,
				agency_id,
				status)
	  		VALUES (
	  			p_prop_id,
	  			p_agency_id,
	  			p_status
	  		);

	  		set v_sale_id = LAST_INSERT_ID();
	  		if v_sale_id > 0 then
	  			set v_status = 0;
	  		end if;

	  		-- insert price
	  		Call pUpdPrice(v_sale_id,p_price,p_price_type,v_status,v_price_id);

	  		if v_sale_id > 0 and v_price_id > 0 then:
	  			COMMIT;
	  		ELSE
	  			ROLLBACK;
	  		end if;

	  	ELSE
			-- insert price
	  		Call pUpdPrice(v_sale_id,p_price,p_price_type,v_status,v_price_id);	  		

		END IF;

		select v_status,v_property_id,v_price_id;

    END //
DELIMITER ;

