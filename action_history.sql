CREATE TABLE `history` (
	`Id_operation` INT NOT NULL AUTO_INCREMENT,
	`time` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`computed_class` VARCHAR,
    'user_id', INT NOT NULL
	PRIMARY KEY (`Id_operation`)
);