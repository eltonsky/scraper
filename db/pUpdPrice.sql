
drop PROCEDURE IF EXISTS pUpdPrice;

DELIMITER //
CREATE PROCEDURE pUpdPrice(
	IN  p_sale_id                 int,
    IN  p_price                   VARCHAR(32),
    IN  p_price_type              VARCHAR(16),
    OUT o_status                  int,
    OUT o_price_id                int

)
    BEGIN

    	set o_status = 0;
    	set o_price_id = 0;

		select 
			price_id
		into
			o_price_id
		from
			tprice
		WHERE
			p_sale_id = sale_id
		and p_price = price
		and p_price_type = type;

		if o_price_id = 0 then
			insert into tprice(
				sale_id,
				price,
				type
			)
			values(
				p_sale_id,
				p_price,
				p_price_type
			);

			set o_price_id = LAST_INSERT_ID();
		end if;

    END //
DELIMITER ;

