-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 07, 2021 at 07:53 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.4.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cricket`
--

-- --------------------------------------------------------

--
-- Table structure for table `country`
--

CREATE TABLE `country` (
  `code` int(11) NOT NULL,
  `name` varchar(35) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `country`
--

INSERT INTO `country` (`code`, `name`) VALUES
(61, 'AUSTRALIA'),
(64, 'NEW ZELAND'),
(91, 'INDIA');

-- --------------------------------------------------------

--
-- Table structure for table `match`
--

CREATE TABLE `match` (
  `id` int(11) NOT NULL,
  `match_date` date NOT NULL,
  `winner` int(11) NOT NULL,
  `loser` int(11) NOT NULL,
  `man_of_the_match` int(11) NOT NULL,
  `bowler_of_the_match` int(11) NOT NULL,
  `best_fielder` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `match`
--

INSERT INTO `match` (`id`, `match_date`, `winner`, `loser`, `man_of_the_match`, `bowler_of_the_match`, `best_fielder`) VALUES
(1, '2021-02-02', 3, 4, 1, 2, 1),
(2, '2021-03-09', 3, 5, 1, 2, 2),
(3, '2021-04-06', 5, 4, 6, 7, 7);

-- --------------------------------------------------------

--
-- Table structure for table `player`
--

CREATE TABLE `player` (
  `id` int(11) NOT NULL,
  `full_name` varchar(50) NOT NULL,
  `age` int(11) NOT NULL,
  `playing_role` varchar(40) NOT NULL,
  `team_id` int(11) NOT NULL,
  `country_code` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `player`
--

INSERT INTO `player` (`id`, `full_name`, `age`, `playing_role`, `team_id`, `country_code`) VALUES
(1, 'Virat Kohli', 32, 'Batsman', 3, 91),
(2, 'M. S. Dhoni', 39, 'WK-Batsman', 3, 91),
(4, 'Aaron Finch', 34, 'Batsman', 4, 61),
(5, 'Glenn Maxwell', 32, 'Batting Allrounder', 4, 61),
(6, 'Trent Boult', 31, 'Bowler', 5, 64),
(7, 'James Neesham', 30, 'Batting Allrounder', 5, 64);

-- --------------------------------------------------------

--
-- Table structure for table `team`
--

CREATE TABLE `team` (
  `id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `matches_played` int(11) NOT NULL DEFAULT 0,
  `wins` int(11) NOT NULL DEFAULT 0,
  `losses` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `team`
--

INSERT INTO `team` (`id`, `name`, `matches_played`, `wins`, `losses`) VALUES
(3, 'Team India', 0, 0, 0),
(4, 'Team Australia', 0, 0, 0),
(5, 'Team New Zeland', 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `venue`
--

CREATE TABLE `venue` (
  `id` int(11) NOT NULL,
  `name` varchar(35) NOT NULL,
  `country_code` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `venue`
--

INSERT INTO `venue` (`id`, `name`, `country_code`) VALUES
(1, 'Eden Gardens', 91),
(2, 'The Gabba', 61);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `country`
--
ALTER TABLE `country`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `match`
--
ALTER TABLE `match`
  ADD PRIMARY KEY (`id`),
  ADD KEY `winner` (`winner`),
  ADD KEY `loser` (`loser`),
  ADD KEY `man_of_the_match` (`man_of_the_match`),
  ADD KEY `bowler_of_the_match` (`bowler_of_the_match`),
  ADD KEY `best_fielder` (`best_fielder`);

--
-- Indexes for table `player`
--
ALTER TABLE `player`
  ADD PRIMARY KEY (`id`),
  ADD KEY `country_code` (`country_code`),
  ADD KEY `team_id` (`team_id`);

--
-- Indexes for table `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `venue`
--
ALTER TABLE `venue`
  ADD PRIMARY KEY (`id`),
  ADD KEY `country_code` (`country_code`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `country`
--
ALTER TABLE `country`
  MODIFY `code` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- AUTO_INCREMENT for table `match`
--
ALTER TABLE `match`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `player`
--
ALTER TABLE `player`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `team`
--
ALTER TABLE `team`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `venue`
--
ALTER TABLE `venue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `match`
--
ALTER TABLE `match`
  ADD CONSTRAINT `match_ibfk_1` FOREIGN KEY (`winner`) REFERENCES `team` (`id`),
  ADD CONSTRAINT `match_ibfk_2` FOREIGN KEY (`loser`) REFERENCES `team` (`id`),
  ADD CONSTRAINT `match_ibfk_3` FOREIGN KEY (`man_of_the_match`) REFERENCES `player` (`id`),
  ADD CONSTRAINT `match_ibfk_4` FOREIGN KEY (`bowler_of_the_match`) REFERENCES `player` (`id`),
  ADD CONSTRAINT `match_ibfk_5` FOREIGN KEY (`best_fielder`) REFERENCES `player` (`id`);

--
-- Constraints for table `player`
--
ALTER TABLE `player`
  ADD CONSTRAINT `player_ibfk_1` FOREIGN KEY (`country_code`) REFERENCES `country` (`code`),
  ADD CONSTRAINT `player_ibfk_2` FOREIGN KEY (`team_id`) REFERENCES `team` (`id`);

--
-- Constraints for table `venue`
--
ALTER TABLE `venue`
  ADD CONSTRAINT `venue_ibfk_1` FOREIGN KEY (`country_code`) REFERENCES `country` (`code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
