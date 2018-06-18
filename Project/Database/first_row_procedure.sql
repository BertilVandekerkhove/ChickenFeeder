DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_or_update_first_rows`(IN ID INT, IN feedTime TIME, IN dayID INT)
BEGIN
	IF dayID = 0 THEN SET dayID = NULL;
    END IF;

	SELECT COUNT(*) INTO @feederID from feeder;

	IF EXISTS (select * from feeder where feedingTimeID = ID) THEN
		update feedingtimes set feedingTime = feedTime where feedingTimeID = ID;
	ELSE
		insert into feeder values (@feederID+1,ID,NULL,NULL);
		insert into feedingtimes values(ID,feedTime,1,dayID);
	END IF;
END$$
DELIMITER ;