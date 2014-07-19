
drop PROCEDURE IF EXISTS pUpdSaleAgent;

DELIMITER //
CREATE PROCEDURE pUpdSaleAgent(
	IN  p_sale_id            int,
    IN  p_agent_id           int,
    IN  p_capture_date_time  VARCHAR(16)
)
    BEGIN
    	DECLARE v_status INT DEFAULT 0;
		DECLARE v_sale_agent_id INT DEFAULT 0;

		select 
			sale_agent_id
		into
			v_sale_agent_id
		from
			tsaleagent
		WHERE
			p_sale_id = sale_id
		and p_agent_id = agent_id;

		if v_sale_agent_id = 0 then
			insert into tsaleagent(
				sale_id,
				agent_id,
				capture_date_time
			)
			values(
				p_sale_id,
				p_agent_id,
				p_capture_date_time
			);

			set v_sale_agent_id = LAST_INSERT_ID();
		end if;

		select v_status,v_sale_agent_id;

    END //
DELIMITER ;

