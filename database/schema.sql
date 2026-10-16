CREATE DATABASE IF NOT EXISTS eldercare_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE eldercare_db;

CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    appointment_at DATETIME NOT NULL,
    location VARCHAR(255),
    preparation_notes TEXT,
    status ENUM('scheduled', 'completed', 'cancelled')
        NOT NULL DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);