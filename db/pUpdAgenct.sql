
drop PROCEDURE pUpdAgent;

DELIMITER //
CREATE PROCEDURE pUpdAgent(
	IN  p_agency_id              int,
    IN  p_name                   VARCHAR(32),
    IN  p_phone                  VARCHAR(32)
)
    BEGIN

    	set v_status = 0;
    	set v_agent_id = 0;

		select 
			agent_id
		into
			v_agent_id
		from
			tAgent
		WHERE
			p_name = name
		and p_agency_id = agency_id;

		if v_agent_id == 0
			insert into tAgent(
				name,
				phone,
				agency_id
			)
			values(
				p_name,
				p_phone,
				p_agency_id
			);

			set v_agent_id = LAST_INSERT_ID();
		end if;

		select v_status,v_agent_id;

    END //
DELIMITER ;

