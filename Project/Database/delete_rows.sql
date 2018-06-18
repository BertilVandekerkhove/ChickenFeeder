CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_rows`(IN amountToDelete INT)
BEGIN
	DECLARE amount INT;
    DECLARE rowsToDelete INT;

    SET amount = (SELECT MAX(feedingTimeID) FROM feedingtimes);
    SET rowsToDelete = amount-amountToDelete;

    WHILE amount != rowsToDelete DO
    BEGIN
		delete from feedingtimes where feedingTimeID = amount;
		delete from feeder where feedingTimeID = amount;
        SET amount = amount -1;
    END;
	END WHILE;
END