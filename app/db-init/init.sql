-- Initialize database schema
USE onlinesystem;

-- Create Manager table
CREATE TABLE IF NOT EXISTS Manager (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    username VARCHAR(120) UNIQUE NOT NULL,
    domain VARCHAR(120) NOT NULL,
    idno VARCHAR(120) UNIQUE NOT NULL,
    pword VARCHAR(500) NOT NULL
);

-- Create Security table
CREATE TABLE IF NOT EXISTS Security (
    id INT UNIQUE,
    name VARCHAR(120) NOT NULL,
    username VARCHAR(120) UNIQUE NOT NULL,
    domain VARCHAR(120) NOT NULL,
    idno VARCHAR(120) PRIMARY KEY NOT NULL,
    pword VARCHAR(120) NOT NULL
);

-- Create Duty table
CREATE TABLE IF NOT EXISTS Duty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ddate VARCHAR(120) NOT NULL,
    idno VARCHAR(120) NOT NULL,
    stime VARCHAR(120) NOT NULL,
    etime VARCHAR(120) NOT NULL
);

-- Create Absence table
CREATE TABLE IF NOT EXISTS Absence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idno VARCHAR(120) UNIQUE NOT NULL,
    sdate VARCHAR(120) NOT NULL,
    edate VARCHAR(120) NOT NULL,
    reason VARCHAR(120) NOT NULL,
    status VARCHAR(120) NOT NULL,
    timestamp VARCHAR(120) NOT NULL
);

-- Create Contact table
CREATE TABLE IF NOT EXISTS Contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    email VARCHAR(20) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    msg VARCHAR(120) NOT NULL
);
