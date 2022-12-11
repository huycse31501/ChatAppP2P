CREATE SCHEMA chatapp;
use chatapp;

CREATE TABLE `User`(
	username  char(20) NOT NULL,
    password char(20) NOT NULL,
	isonline bool NOT NULL,
    address char(20),
    PRIMARY KEY(username)
);

CREATE TABLE `Fuser`(
	username  char(20) NOT NULL,
    fusername char(20) NOT NULL,
    PRIMARY KEY(username, fusername),
    FOREIGN KEY (username) references `User`(username) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (fusername) references `User`(username) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO USER (username, password, isonline) VALUES ("a1","1", False);
INSERT INTO USER (username, password, isonline) VALUES ("a2","1", False);
INSERT INTO USER (username, password, isonline) VALUES ("a3","1", False);
INSERT INTO USER (username, password, isonline) VALUES ("a4","1", False);
INSERT INTO USER (username, password, isonline) VALUES ("a5","1", False);
INSERT INTO USER (username, password, isonline) VALUES ("a6","1", False);

DROP TABLE USER;
DROP TABLE FUSER;

INSERT INTO FUSER (username, fusername) VALUES ("a1","a2");
INSERT INTO FUSER (username, fusername) VALUES ("a2","a1");
INSERT INTO FUSER (username, fusername) VALUES ("a1","a3");


SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE FUSER;
TRUNCATE USER;
SET FOREIGN_KEY_CHECKS = 1;
SELECT fusername FROM FUSER WHERE username = "a1";
UPDATE FUSER SET fusername = "a4" WHERE username = "a1"
