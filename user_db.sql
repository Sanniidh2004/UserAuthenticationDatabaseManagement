CREATE DATABASE user_auth_db;
USE user_auth_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    roll_no VARCHAR(50),
    address TEXT
);

CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    subject VARCHAR(50),
    marks INT,
    grade VARCHAR(2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO grades (user_id, subject, marks, grade)
VALUES
(1, 'Application Development Lab', 89, 'E'),
(1, 'Software Engineering', 92, 'O'),
(1, 'Computer Networks', 84, 'E'),
(1, 'VLSI Circuits & Designs', 79, 'A'),
(1, 'Microprocessors & Embedded Systems', 88, 'E');

DESC users;

SELECT * FROM users; 
SELECT * FROM grades;

SELECT user, host, plugin
FROM mysql.user
WHERE user = 'root';

ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password
BY 'sanni123';

FLUSH PRIVILEGES;
