
drop PROCEDURE if exists pUpdAddress;

DELIMITER //
CREATE PROCEDURE pUpdAddress(
	IN  p_street_no                     VARCHAR(16), 
    IN  p_street_name                   VARCHAR(64), 
    IN  p_locality                      VARCHAR(64),
    IN  p_region                        VARCHAR(16), 
    IN  p_postcode                      VARCHAR(4),
    IN  p_capture_date_time             VARCHAR(16)
)


    BEGIN

    	DECLARE v_addr_id INT DEFAULT 0;

		select 
			addr_id
		into
			v_addr_id
		from
			taddr
		WHERE
			p_street_no = street_no
		and p_street_name = street_name
		and p_locality = locality
		and p_postcode = postcode;

		-- insert
		IF v_addr_id = 0 then
			INSERT INTO taddr(
				street_no,
				street_name,
				locality,
				region,
				postcode,
				capture_date_time)
	  		VALUES (
	  			p_street_no,
	  			p_street_name,
	  			p_locality,
	  			p_region,
	  			p_postcode,
	  			p_capture_date_time
	  		);

	  		select 0,LAST_INSERT_ID();

	  	ELSE
	  		select -1,v_addr_id;

		END IF;

    END //
DELIMITER ;