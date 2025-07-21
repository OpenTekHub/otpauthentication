-- Database setup for OTP-based authentication
CREATE DATABASE IF NOT EXISTS harish;

USE harish;

-- Users table for OTP authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    otp VARCHAR(6),
    otp_expires_at TIMESTAMP NULL,
    otp_verified BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Index for faster phone number lookups
CREATE INDEX idx_phone_number ON users(phone_number);
CREATE INDEX idx_otp_expires ON users(otp_expires_at);

-- Optional: Table for storing OTP attempts (for rate limiting)
CREATE TABLE IF NOT EXISTS otp_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(15) NOT NULL,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT FALSE,
    ip_address VARCHAR(45),
    INDEX idx_phone_attempts (phone_number),
    INDEX idx_attempt_time (attempt_time)
);
