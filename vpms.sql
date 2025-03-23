-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 22, 2025 at 04:24 PM
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
  `name` varchar(70) NOT NULL,
  `role` enum('parking','entrance','exit') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `camera`
--

INSERT INTO `camera` (`id`, `source`, `name`, `role`) VALUES
(1, 'parking.mp4', 'ที่จอดรถ', 'parking'),
(2, 'entrance.mp4', 'ทางเข้า', 'entrance'),
(3, 'exit.mp4', 'ทางออก', 'exit');

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

--
-- Dumping data for table `parking_space`
--

INSERT INTO `parking_space` (`id`, `name`, `status`, `x`, `y`, `source`) VALUES
(1, 'A', 'available', 93, 239, 'parking.mp4'),
(2, 'A', 'available', 263, 257, 'parking.mp4'),
(3, 'A', 'available', 446, 277, 'parking.mp4'),
(4, 'A', 'available', 649, 302, 'parking.mp4'),
(5, 'A', 'available', 891, 335, 'parking.mp4'),
(6, 'A', 'available', 1116, 358, 'parking.mp4');

-- --------------------------------------------------------

--
-- Table structure for table `parking_stat`
--

CREATE TABLE `parking_stat` (
  `id` int(11) NOT NULL,
  `plate_number` varchar(50) NOT NULL,
  `image_entrance` varchar(100) DEFAULT NULL,
  `image_exit` varchar(100) DEFAULT NULL,
  `datetime_entrance` datetime DEFAULT NULL,
  `datetime_exit` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parking_stat`
--

INSERT INTO `parking_stat` (`id`, `plate_number`, `image_entrance`, `image_exit`, `datetime_entrance`, `datetime_exit`) VALUES
(1, 'อม6736', 'อม6736 2025-03-21 07-00-07.jpg', NULL, '2025-03-21 07:00:07', NULL),
(2, '', '2025-03-21 07-25-33.jpg', NULL, '2025-03-21 07:25:33', NULL),
(3, 'น', 'น 2025-03-21 07-35-54.jpg', NULL, '2025-03-21 07:35:54', NULL),
(4, '21', '21 2025-03-21 07-37-36.jpg', NULL, '2025-03-21 07:37:36', NULL),
(5, '', '2025-03-21 07-38-03.jpg', NULL, '2025-03-21 07:38:03', NULL),
(6, '99', '99 2025-03-21 07-38-17.jpg', NULL, '2025-03-21 07:38:17', NULL),
(7, '', '2025-03-21 07-47-54.jpg', NULL, '2025-03-21 07:47:54', NULL),
(8, '', '2025-03-21 07-48-14.jpg', NULL, '2025-03-21 07:48:14', NULL),
(9, 'กสร', 'กสร 2025-03-21 07-51-21.jpg', NULL, '2025-03-21 07:51:21', NULL),
(10, '', '2025-03-21 07-55-53.jpg', NULL, '2025-03-21 07:55:53', NULL),
(11, '', '2025-03-21 07-57-08.jpg', NULL, '2025-03-21 07:57:08', NULL),
(12, '', '2025-03-21 07-59-51.jpg', NULL, '2025-03-21 07:59:51', NULL),
(13, '', '2025-03-21 08-00-49.jpg', NULL, '2025-03-21 08:00:49', NULL),
(14, 'จ8', 'จ8 2025-03-21 08-06-36.jpg', NULL, '2025-03-21 08:06:36', NULL),
(15, '', '2025-03-21 08-10-57.jpg', NULL, '2025-03-21 08:10:57', NULL),
(16, 'ทร', 'ทร 2025-03-21 08-14-32.jpg', NULL, '2025-03-21 08:18:32', NULL),
(17, '', '2025-03-21 08-16-51.jpg', NULL, '2025-03-21 08:16:51', NULL),
(18, '', '2025-03-21 10-20-34.jpg', NULL, '2025-03-21 10:20:34', NULL),
(19, '', '2025-03-21 12-01-39.jpg', NULL, '2025-03-21 12:01:39', NULL),
(20, '', '2025-03-21 12-02-03.jpg', NULL, '2025-03-21 12:02:03', NULL),
(21, 'ถอ4085', 'ถอ4085 2025-03-21 12-02-00.jpg', NULL, '2025-03-21 12:02:00', NULL),
(22, '', '2025-03-21 12-07-05.jpg', NULL, '2025-03-21 12:07:50', NULL),
(23, '', '2025-03-21 13-45-29.jpg', NULL, '2025-03-21 13:45:29', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(256) NOT NULL,
  `role` enum('user','admin') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `role`) VALUES
(1, 'Admin', 'scrypt:32768:8:1$PrnBptfWqkDn2uCI$b0ccaa67d287948f2e0b755aeacd036969b117b5fa783c21db632ef88d8e74366b3c80ce4ea61b3608e02227fdc6483c3cd69a38a39970908de2427f9db55f54', 'admin');

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
(1, 'parking/ที่จอดรถ 2025-03-20 07-00-00.mp4'),
(2, 'parking/ที่จอดรถ 2025-03-20 07-02-11.mp4'),
(3, 'parking/ที่จอดรถ 2025-03-20 07-05-12.mp4'),
(4, 'parking/ที่จอดรถ 2025-03-20 07-08-03.mp4'),
(5, 'parking/ที่จอดรถ 2025-03-20 07-10-53.mp4'),
(6, 'parking/ที่จอดรถ 2025-03-20 07-13-41.mp4'),
(7, 'parking/ที่จอดรถ 2025-03-20 07-16-37.mp4'),
(8, 'parking/ที่จอดรถ 2025-03-20 07-19-21.mp4'),
(9, 'parking/ที่จอดรถ 2025-03-20 07-22-09.mp4'),
(10, 'parking/ที่จอดรถ 2025-03-20 07-24-57.mp4'),
(11, 'parking/ที่จอดรถ 2025-03-20 07-27-40.mp4'),
(12, 'parking/ที่จอดรถ 2025-03-20 07-30-24.mp4'),
(13, 'parking/ที่จอดรถ 2025-03-20 07-33-06.mp4'),
(14, 'parking/ที่จอดรถ 2025-03-20 07-35-52.mp4'),
(15, 'parking/ที่จอดรถ 2025-03-20 07-38-37.mp4'),
(16, 'parking/ที่จอดรถ 2025-03-20 07-41-17.mp4'),
(17, 'parking/ที่จอดรถ 2025-03-20 07-44-02.mp4'),
(18, 'parking/ที่จอดรถ 2025-03-20 07-46-47.mp4'),
(19, 'parking/ที่จอดรถ 2025-03-20 07-49-28.mp4'),
(20, 'parking/ที่จอดรถ 2025-03-20 07-52-15.mp4'),
(21, 'parking/ที่จอดรถ 2025-03-20 07-55-05.mp4'),
(22, 'parking/ที่จอดรถ 2025-03-20 07-57-48.mp4'),
(23, 'parking/ที่จอดรถ 2025-03-20 09-00-54.mp4'),
(24, 'parking/ที่จอดรถ 2025-03-20 09-04-12.mp4'),
(25, 'parking/ที่จอดรถ 2025-03-20 09-08-29.mp4'),
(26, 'parking/ที่จอดรถ 2025-03-20 09-12-39.mp4'),
(27, 'parking/ที่จอดรถ 2025-03-20 09-16-39.mp4'),
(28, 'parking/ที่จอดรถ 2025-03-20 09-20-41.mp4'),
(29, 'parking/ที่จอดรถ 2025-03-20 09-24-48.mp4'),
(30, 'parking/ที่จอดรถ 2025-03-20 09-28-54.mp4'),
(31, 'parking/ที่จอดรถ 2025-03-20 09-32-57.mp4'),
(32, 'parking/ที่จอดรถ 2025-03-20 09-41-06.mp4'),
(33, 'parking/ที่จอดรถ 2025-03-20 09-45-32.mp4'),
(34, 'parking/ที่จอดรถ 2025-03-20 09-49-39.mp4'),
(35, 'parking/ที่จอดรถ 2025-03-20 09-53-43.mp4'),
(36, 'parking/ที่จอดรถ 2025-03-20 09-57-41.mp4'),
(37, 'parking/ที่จอดรถ 2025-03-20 15-49-04.mp4'),
(38, 'parking/ที่จอดรถ 2025-03-20 16-28-39.mp4'),
(39, 'parking/ที่จอดรถ 2025-03-20 16-31-09.mp4'),
(40, 'parking/ที่จอดรถ 2025-03-20 16-33-37.mp4'),
(41, 'parking/ที่จอดรถ 2025-03-20 16-36-06.mp4'),
(42, 'parking/ที่จอดรถ 2025-03-20 16-38-37.mp4'),
(43, 'parking/ที่จอดรถ 2025-03-20 16-41-06.mp4'),
(44, 'exit/ทางออก 2025-03-21 10-43-48.mp4'),
(45, 'exit/ทางออก 2025-03-21 10-49-25.mp4'),
(46, 'exit/ทางออก 2025-03-21 10-55-07.mp4'),
(47, 'exit/ทางออก 2025-03-21 10-59-47.mp4'),
(48, 'exit/ทางออก 2025-03-21 11-04-18.mp4'),
(49, 'exit/ทางออก 2025-03-21 11-08-23.mp4'),
(50, 'exit/ทางออก 2025-03-21 11-12-50.mp4'),
(51, 'exit/ทางออก 2025-03-21 11-17-24.mp4'),
(52, 'exit/ทางออก 2025-03-21 11-21-53.mp4'),
(53, 'exit/ทางออก 2025-03-21 11-26-23.mp4'),
(54, 'exit/ทางออก 2025-03-21 11-31-14.mp4'),
(55, 'exit/ทางออก 2025-03-21 11-34-27.mp4'),
(56, 'exit/ทางออก 2025-03-21 11-39-14.mp4'),
(57, 'exit/ทางออก 2025-03-21 11-44-04.mp4'),
(58, 'exit/ทางออก 2025-03-21 11-48-23.mp4'),
(59, 'exit/ทางออก 2025-03-21 11-52-45.mp4'),
(60, 'exit/ทางออก 2025-03-21 11-57-31.mp4'),
(61, 'exit/ทางออก 2025-03-21 12-02-01.mp4'),
(62, 'exit/ทางออก 2025-03-21 12-06-07.mp4'),
(63, 'exit/ทางออก 2025-03-21 12-11-01.mp4'),
(64, 'exit/ทางออก 2025-03-21 12-15-26.mp4'),
(65, 'exit/ทางออก 2025-03-21 12-19-12.mp4'),
(66, 'exit/ทางออก 2025-03-21 12-23-23.mp4'),
(67, 'exit/ทางออก 2025-03-21 12-27-31.mp4'),
(68, 'exit/ทางออก 2025-03-21 15-17-17.mp4'),
(69, 'exit/ทางออก 2025-03-21 15-22-24.mp4'),
(70, 'exit/ทางออก 2025-03-21 15-27-05.mp4'),
(71, 'exit/ทางออก 2025-03-21 15-31-56.mp4'),
(72, 'exit/ทางออก 2025-03-21 15-36-57.mp4'),
(73, 'exit/ทางออก 2025-03-21 15-41-33.mp4'),
(74, 'exit/ทางออก 2025-03-21 15-46-20.mp4'),
(75, 'exit/ทางออก 2025-03-21 15-51-00.mp4'),
(76, 'exit/ทางออก 2025-03-21 15-55-23.mp4'),
(77, 'exit/ทางออก 2025-03-21 16-00-03.mp4'),
(78, 'exit/ทางออก 2025-03-21 16-04-58.mp4'),
(79, 'exit/ทางออก 2025-03-21 16-09-44.mp4'),
(80, 'exit/ทางออก 2025-03-21 16-14-24.mp4'),
(81, 'exit/ทางออก 2025-03-21 16-19-11.mp4'),
(82, 'exit/ทางออก 2025-03-21 16-23-45.mp4'),
(83, 'entrance/ทางเข้า 2025-03-21 07-00-00.mp4'),
(84, 'entrance/ทางเข้า 2025-03-21 07-03-34.mp4'),
(85, 'entrance/ทางเข้า 2025-03-21 07-07-15.mp4'),
(86, 'entrance/ทางเข้า 2025-03-21 07-10-50.mp4'),
(87, 'entrance/ทางเข้า 2025-03-21 07-14-24.mp4'),
(88, 'entrance/ทางเข้า 2025-03-21 07-18-02.mp4'),
(89, 'entrance/ทางเข้า 2025-03-21 07-21-29.mp4'),
(90, 'entrance/ทางเข้า 2025-03-21 07-23-22.mp4'),
(91, 'entrance/ทางเข้า 2025-03-21 07-26-41.mp4'),
(92, 'entrance/ทางเข้า 2025-03-21 07-30-23.mp4'),
(93, 'entrance/ทางเข้า 2025-03-21 07-33-49.mp4'),
(94, 'entrance/ทางเข้า 2025-03-21 07-37-24.mp4'),
(95, 'entrance/ทางเข้า 2025-03-21 07-40-44.mp4'),
(96, 'entrance/ทางเข้า 2025-03-21 07-44-29.mp4'),
(97, 'entrance/ทางเข้า 2025-03-21 07-48-01.mp4'),
(98, 'entrance/ทางเข้า 2025-03-21 07-51-33.mp4'),
(99, 'entrance/ทางเข้า 2025-03-21 07-55-17.mp4'),
(100, 'entrance/ทางเข้า 2025-03-21 07-58-46.mp4'),
(101, 'entrance/ทางเข้า 2025-03-21 08-02-16.mp4'),
(102, 'entrance/ทางเข้า 2025-03-21 08-05-46.mp4'),
(103, 'entrance/ทางเข้า 2025-03-21 08-09-16.mp4'),
(104, 'entrance/ทางเข้า 2025-03-21 08-12-33.mp4'),
(105, 'entrance/ทางเข้า 2025-03-21 08-17-18.mp4'),
(106, 'entrance/ทางเข้า 2025-03-21 08-22-32.mp4'),
(107, 'entrance/ทางเข้า 2025-03-21 10-12-45.mp4'),
(108, 'entrance/ทางเข้า 2025-03-21 10-17-49.mp4'),
(109, 'entrance/ทางเข้า 2025-03-21 12-02-09.mp4'),
(110, 'entrance/ทางเข้า 2025-03-21 12-07-03.mp4'),
(111, 'entrance/ทางเข้า 2025-03-21 13-10-17.mp4'),
(112, 'entrance/ทางเข้า 2025-03-21 13-15-38.mp4'),
(113, 'entrance/ทางเข้า 2025-03-21 13-21-05.mp4'),
(114, 'entrance/ทางเข้า 2025-03-21 13-26-33.mp4'),
(115, 'entrance/ทางเข้า 2025-03-21 13-32-19.mp4'),
(116, 'entrance/ทางเข้า 2025-03-21 13-37-53.mp4'),
(117, 'entrance/ทางเข้า 2025-03-21 13-43-17.mp4'),
(118, 'entrance/ทางเข้า 2025-03-21 13-48-40.mp4');

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
-- Indexes for table `parking_stat`
--
ALTER TABLE `parking_stat`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `parking_space`
--
ALTER TABLE `parking_space`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `parking_stat`
--
ALTER TABLE `parking_stat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `video`
--
ALTER TABLE `video`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=119;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `parking_space`
--
ALTER TABLE `parking_space`
  ADD CONSTRAINT `source_fk` FOREIGN KEY (`source`) REFERENCES `camera` (`source`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
