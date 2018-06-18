DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_or_update_time`(IN ID INT, IN feedTime TIME, IN dayID INT)
BEGIN
	IF dayID = 0 THEN SET dayID = NULL;
    END IF;

	SELECT feederID INTO @feederID FROM feeder ORDER BY feederID DESC LIMIT 1;
    if @feederID IS NULL THEN
		SELECT COUNT(*) INTO @feederID from feeder;
	END IF;

	IF EXISTS (select * from feeder where feedingTimeID = ID) THEN
		SELECT COUNT(*) INTO @teller from feedingtimes where feedingtimes.feedingTime = feedTime and feedingtimes.dayID = dayID;
        IF @teller = 0 THEN
			update feedingtimes set feedingTime = feedTime where feedingTimeID = ID;
		ELSE
			delete from feedingtimes where feedingTimeID = ID;
      delete from feeder where feedingTimeID = ID;
		END IF;
	ELSE
    SELECT COUNT(*) INTO @teller from feedingtimes where feedingtimes.feedingTime = feedTime and feedingtimes.dayID = dayID;
    IF @teller = 0 THEN
		insert into feeder values (@feederID+1,ID,NULL,NULL);
	IF @teller = 0 THEN
		insert into feedingtimes values(ID,feedTime,1,dayID);
	END IF;
    END IF;
	END IF;
END$$
DELIMITER ;
