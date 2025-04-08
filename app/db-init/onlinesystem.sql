-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 08, 2025 at 12:23 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `onlinesystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `absence`
--

CREATE TABLE `absence` (
  `id` int(11) NOT NULL,
  `idno` int(11) NOT NULL,
  `sdate` varchar(10) NOT NULL,
  `edate` varchar(11) NOT NULL,
  `reason` varchar(1000) NOT NULL,
  `status` varchar(100) NOT NULL,
  `timestamp` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(25) NOT NULL,
  `msg` varchar(10000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `duty`
--

CREATE TABLE `duty` (
  `id` int(100) NOT NULL,
  `ddate` varchar(10) NOT NULL,
  `didno` varchar(10) NOT NULL,
  `stime` varchar(10) NOT NULL,
  `etime` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Manager`
--

CREATE TABLE `Manager` (
  `id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `domain` varchar(100) NOT NULL,
  `idno` varchar(100) NOT NULL,
  `pword` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Manager`
--

INSERT INTO `Manager` (`id`, `name`, `username`, `domain`, `idno`, `pword`) VALUES
(1, 'ABC', 'ABC', 'Manager', '00000', '00000'),
(2, 'PK', 'prk@123', 'Manager', '01236', '$2b$12$/A.Aj2xQuEul7KUe32Sr1e8CbSCBp09ZlCgxiKdhIjNbDJEiQJI9y');

-- --------------------------------------------------------

--
-- Table structure for table `security`
--

CREATE TABLE `security` (
  `id` int(11) NOT NULL,
  `name` int(11) NOT NULL,
  `username` int(11) NOT NULL,
  `domain` int(11) NOT NULL,
  `idno` int(11) NOT NULL,
  `pword` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Manager`
--
ALTER TABLE `Manager`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Manager`
--
ALTER TABLE `Manager`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
