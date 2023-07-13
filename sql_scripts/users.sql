CREATE TABLE `Users` (
	`Id` INT NOT NULL AUTO_INCREMENT,
	`Username` VARCHAR(25),
	`psswd` VARCHAR,
	PRIMARY KEY (`Id`)
);

INSERT INTO Users ('Username','psswd') VALUES ('admin','admin');