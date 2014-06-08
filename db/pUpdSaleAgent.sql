
drop PROCEDURE pUpdSaleAgent;

DELIMITER //
CREATE PROCEDURE pUpdSaleAgent(
	IN  p_sale_id            int,
    IN  p_agent_id           int
)
    BEGIN

    	set v_status = 0;
    	set v_sale_agent_id = 0;

		select 
			sale_agent_id
		into
			v_sale_agent_id
		from
			tSaleAgent
		WHERE
			p_sale_id = sale_id
		and p_agent_id = agent_id;

		if v_sale_agent_id == 0
			insert into tSaleAgent(
				sale_id,
				agent_id
			)
			values(
				p_sale_id,
				p_agent_id
			);

			set v_sale_agent_id = LAST_INSERT_ID();
		end if;

		select v_status,v_sale_agent_id;

    END //
DELIMITER ;

