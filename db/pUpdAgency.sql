
drop PROCEDURE pUpdAgency;

DELIMITER //
CREATE PROCEDURE pUpdAgency(
    IN  p_name                   VARCHAR(32)
)
    BEGIN

    	set v_status = 0;
    	set v_agency_id = 0;

		select 
			agency_id
		into
			v_agency_id
		from
			tAgency
		WHERE
			p_name = name;

		if v_agency_id == 0
			insert into tAgency(
				name
			)
			values(
				p_name
			);

			set v_agency_id = LAST_INSERT_ID();
		end if;

		select v_status,v_agency_id;

    END //
DELIMITER ;

