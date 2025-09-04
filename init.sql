CREATE DATABASE IF NOT EXISTS `mercury-database`;
USE `mercury-database`;

CREATE TABLE IF NOT EXISTS members (
    id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    messages_count INT DEFAULT 0,
    warnings INT DEFAULT 0
);
