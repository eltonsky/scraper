
drop PROCEDURE IF EXISTS pUpdAgent;

DELIMITER //
CREATE PROCEDURE pUpdAgent(
	IN  p_agency_id              int,
    IN  p_name                   VARCHAR(32),
    IN  p_phone                  VARCHAR(32),
    IN  p_capture_date_time      VARCHAR(16)
)
    BEGIN
    	DECLARE v_status INT DEFAULT 0;
		DECLARE v_agent_id INT DEFAULT 0;

		select 
			agent_id
		into
			v_agent_id
		from
			tagent
		WHERE
			p_name = name
		and p_agency_id = agency_id;

		if v_agent_id = 0 then
			insert into tagent(
				name,
				phone,
				agency_id,
				capture_date_time
			)
			values(
				p_name,
				p_phone,
				p_agency_id,
				p_capture_date_time
			);

			set v_agent_id = LAST_INSERT_ID();
		end if;

		select v_status,v_agent_id;

    END //
DELIMITER ;

