CREATE DATABASE [IF NOT EXISTS] garage;

USE garage;

CREATE TABLE [IF NOT EXISTS] customer_details (
	customer_id INT NO NULL AUTO_INCREMENT,
	first_name VARCHAR(30),
	last_name VARCHAR(30),
	car_num VARCHAR(8),
	car_color VARCHAR(20),
	car_brand VARCHAR(20),
	car_model VARCHAR(15),
	phone VARCHAR(15)
	prb_desc TEXT,
	status TINYINT(1) DEFAULT 0,
	PRIMARY KEY (customer_id)
);

CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON garage.customer_details to 'username'@'localhost';
