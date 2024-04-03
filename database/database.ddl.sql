CREATE DATABASE CS4417;

USE CS4417;

CREATE TABLE user (
	id	int PRIMARY KEY AUTO_INCREMENT,
    username varchar(32),
    password_hash varchar(32),
    first_name varchar(32),
    last_name varchar(32)
);

