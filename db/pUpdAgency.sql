
drop PROCEDURE IF EXISTS pUpdAgency;

DELIMITER //
CREATE PROCEDURE pUpdAgency(
    IN  p_name                   VARCHAR(32),
    IN  p_capture_date_time      VARCHAR(16)
)
    BEGIN
    	DECLARE v_status INT DEFAULT 0;
		DECLARE v_agency_id INT DEFAULT 0;
		
		select 
			agency_id
		into
			v_agency_id
		from
			tagency
		WHERE
			p_name = name;

		if v_agency_id = 0 then
			insert into tagency(
				name,
				capture_date_time
			)
			values(
				p_name,
				p_capture_date_time
			);

			set v_agency_id = LAST_INSERT_ID();
		end if;

		select v_status,v_agency_id;

    END //
DELIMITER ;

