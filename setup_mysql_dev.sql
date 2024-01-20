-- Create the database
CREATE DATABASE IF NOT EXISTS hbnb_dev;
USE hbnb_dev;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create listings table
CREATE TABLE IF NOT EXISTS listings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    listing_id INT,
    user_id INT,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Add any additional tables or relationships as needed

-- Insert sample data (optional)
INSERT INTO users (username, email, password) VALUES
    ('john_doe', 'john@example.com', 'hashed_password'),
    ('jane_doe', 'jane@example.com', 'hashed_password');

INSERT INTO listings (title, description, price, user_id) VALUES
    ('Cozy Apartment', 'A cozy place in the city center.', 100.00, 1),
    ('Beach House', 'Beautiful house near the beach.', 150.00, 2);

INSERT INTO bookings (listing_id, user_id, check_in_date, check_out_date) VALUES
    (1, 2, '2023-01-15', '2023-01-20'),
    (2, 1, '2023-02-10', '2023-02-15');
