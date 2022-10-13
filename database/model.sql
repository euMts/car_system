DROP database if exists carford_car_shop_database;
create database carford_car_shop_database;

-- USE carford_car_shop_database;

CREATE TABLE users (
    `user_id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(25) NOT NULL,
    `password` varchar(255),
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE(username)
);

CREATE TABLE clients (
    `client_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `age` int NOT NULL,
    `cellphone` varchar(25) NOT NULL,
    `sale_opportunity` boolean,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`client_id`)
);

CREATE TABLE cars (
    `car_id` int NOT NULL AUTO_INCREMENT,
    `color` varchar(7) NOT NULL,
    `model` varchar(12) NOT NULL,
    `owner` int,
    `created_at` datetime NOT NULL,
    `updated_at` datetime NOT NULL,
    PRIMARY KEY (`car_id`),
    FOREIGN KEY (owner) REFERENCES Clients(client_id)
);

INSERT INTO users (username, password, created_at, updated_at) VALUES ("root", "gAAAAABjR9VN-d94rYx_swWzGKi5ExdZ1KT8xvcB3s3a275OijMhvXQ-3b2iAdAEkf__p2Phk9kH2eSSr9XNPgyxQslcOj9ynA==", "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");

INSERT INTO clients (name, age, cellphone, sale_opportunity, created_at, updated_at) VALUES ("Matheus", 20, "145214521452", 1, "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");
INSERT INTO cars (color, model, owner, created_at, updated_at) VALUES ("yellow", "sedan", 1, "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");
INSERT INTO cars (color, model, owner, created_at, updated_at) VALUES ("blue", "convertible", 1, "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");
INSERT INTO cars (color, model, owner, created_at, updated_at) VALUES ("blue", "hatch", 1, "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");
UPDATE clients SET sale_opportunity = 0 WHERE client_id = 1;

INSERT INTO clients (name, age, cellphone, sale_opportunity, created_at, updated_at) VALUES ("Joao", 30, "124596365888", 1, "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");

INSERT INTO clients (name, age, cellphone, sale_opportunity, created_at, updated_at) VALUES ("Luiz", 42, "989658964751", 1, "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");
INSERT INTO cars (color, model, owner, created_at, updated_at) VALUES ("blue", "sedan", 3, "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");
INSERT INTO cars (color, model, owner, created_at, updated_at) VALUES ("gray", "hatch", 3, "2022-10-12 18:05:35.337248", "2022-10-12 18:05:35.337248");
UPDATE clients SET sale_opportunity = 0 WHERE client_id = 3;