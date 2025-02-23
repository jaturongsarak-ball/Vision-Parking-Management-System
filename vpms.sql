-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 23, 2025 at 07:56 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vpms`
--

-- --------------------------------------------------------

--
-- Table structure for table `camera`
--

CREATE TABLE `camera` (
  `id` int(11) NOT NULL,
  `source` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `role` enum('parking','entrance','exit') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `camera`
--

INSERT INTO `camera` (`id`, `source`, `name`, `role`) VALUES
(29, 'http://192.168.2.48:4000/stream/parking_1.mp4', 'กล้องตัวที่ 1', 'parking'),
(31, 'http://192.168.2.48:4000/stream/parking_2.mp4', 'กล้องตัวที่ 2', 'parking'),
(32, 'http://192.168.2.48:4000/stream/parking_3.mp4', 'กล้องตัวที่ 3', 'parking');

-- --------------------------------------------------------

--
-- Table structure for table `parking_space`
--

CREATE TABLE `parking_space` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `status` enum('available','occupied') NOT NULL,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  `source` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `video`
--

CREATE TABLE `video` (
  `id` int(11) NOT NULL,
  `file_path` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `video`
--

INSERT INTO `video` (`id`, `file_path`) VALUES
(1227, 'parking/ทดสอบ 2025-02-23 12-26-54.mp4'),
(1228, 'parking/ทดสอบ 2025-02-23 12-30-28.mp4'),
(1229, 'parking/ทดสอบ 2025-02-23 12-34-33.mp4'),
(1230, 'parking/ทดสอบ 2025-02-23 13-11-03.mp4'),
(1231, 'parking/กล้องตัวที่ 2 2025-02-23 13-11-06.mp4'),
(1232, 'exit/กล้องตัวที่ 1 2025-02-23 13-11-07.mp4'),
(1233, 'parking/กล้องตัวที่ 3 2025-02-23 13-11-09.mp4'),
(1234, 'parking/กล้องตัวที่ 2 2025-02-23 13-16-06.mp4'),
(1235, 'exit/กล้องตัวที่ 1 2025-02-23 13-16-08.mp4'),
(1236, 'parking/กล้องตัวที่ 3 2025-02-23 13-16-09.mp4'),
(1237, 'parking/ทดสอบ 2025-02-23 13-15-13.mp4'),
(1238, 'parking/ทดสอบ 2025-02-23 13-22-51.mp4'),
(1239, 'parking/ทดสอบ 2025-02-23 13-25-25.mp4');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `camera`
--
ALTER TABLE `camera`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `source` (`source`,`name`);

--
-- Indexes for table `parking_space`
--
ALTER TABLE `parking_space`
  ADD PRIMARY KEY (`id`),
  ADD KEY `source_fk` (`source`);

--
-- Indexes for table `video`
--
ALTER TABLE `video`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `camera`
--
ALTER TABLE `camera`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `parking_space`
--
ALTER TABLE `parking_space`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `video`
--
ALTER TABLE `video`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1240;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `parking_space`
--
ALTER TABLE `parking_space`
  ADD CONSTRAINT `source_fk` FOREIGN KEY (`source`) REFERENCES `camera` (`source`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
