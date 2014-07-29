-- this is used to populate tsalestatus from tsale.

drop procedure if exists pRestoreSS;

DELIMITER //

create procedure pRestoreSS()
begin
    DECLARE done int default false;
    DECLARE v_sale_id int;
    DECLARE v_status varchar(120);
    DECLARE v_capture_date_time VARCHAR(16);

    DECLARE cur1 cursor for SELECT SALE_ID,STATUS, capture_date_time FROM tsale;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    open cur1;

    myloop: loop
        fetch cur1 into v_sale_id,v_status,v_capture_date_time;
        if done then
            leave myloop;
        end if;

        select v_sale_id,v_status;
        insert into tsalestatus (sale_id,status,capture_date_time) values (v_sale_id,v_status,v_capture_date_time);

    end loop;

    close cur1;
end //

delimiter ;

call pRestoreSS();