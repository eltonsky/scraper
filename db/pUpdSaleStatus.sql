
drop PROCEDURE IF EXISTS pUpdSaleStatus;

DELIMITER //
CREATE PROCEDURE pUpdSaleStatus(
	IN  p_sale_id                 int,
    IN  p_status                   VARCHAR(32),
    IN  p_capture_date_time       VARCHAR(16),
    OUT o_sale_status_id          int

)
    BEGIN

    	set o_sale_status_id = 0;

		select 
			sale_status_id
		into
			o_sale_status_id
		from
			tsalestatus
		WHERE
			p_sale_id = sale_id
		and p_status = status;

		if o_sale_status_id = 0 then
			insert into tsalestatus(
				sale_id,
				status,
				capture_date_time
			)
			values(
				p_sale_id,
				p_status,
				p_capture_date_time
			);

			set o_sale_status_id = LAST_INSERT_ID();
		end if;

    END //
DELIMITER ;

