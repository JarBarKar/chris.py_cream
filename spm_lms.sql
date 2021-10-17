--
-- Database: `spm_lms`
--
DROP DATABASE IF EXISTS `spm_lms`;
CREATE DATABASE IF NOT EXISTS `spm_lms` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `spm_lms`;

-- --------------------------------------------------------

--
-- Table structure for table `engineer`
--

DROP TABLE IF EXISTS `engineer`;
CREATE TABLE IF NOT EXISTS `engineer` (
  `EID` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `phone` int(8) NOT NULL,
  `email` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  PRIMARY KEY (`EID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `engineer`
--

INSERT INTO `engineer` (`name`, `password`, `phone`, `email`, `address`) VALUES
('Winnie', 'ILOVEHONEY', 999, "winnie@gmail.com", "81 Victoria St, Singapore 188065"),
('Mary', 'WHERESMYLAMB', 911, "mary@gmail.com", "81 Victoria St, Singapore 188065"),
('Luke', 'NOTMYFATHER', 995, "luke@gmail.com", "81 Victoria St, Singapore 188065")
;

-- --------------------------------------------------------
--
-- Table structure for table `trainer`
--

DROP TABLE IF EXISTS `trainer`;
CREATE TABLE IF NOT EXISTS `trainer` (
  `TID` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `phone` int(8) NOT NULL,
  `email` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  PRIMARY KEY (`TID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `trainer`
--

INSERT INTO `trainer` (`name`, `password`, `phone`, `email`, `address`) VALUES
('Chris', 'flat white', 888, "chris@gmail.com", "81 Victoria St, Singapore 188065"),
('Joseph', 'product manager', 123, "joseph@gmail.com", "81 Victoria St, Singapore 188065"),
('God', 'GPA 4', 444, "god@gmail.com", "81 Victoria St, Singapore 188065")
;

-- --------------------------------------------------------
--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
CREATE TABLE IF NOT EXISTS `course` (
  `CID` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `prerequisites` varchar(64) NOT NULL,
  PRIMARY KEY (`CID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`CID`,`name`, `prerequisites`) VALUES
('IS111', 'Intro to Prog', ''),
('IS112', 'Data Management', ''),
('IS113', 'WAD 1', 'IS111'),
('IS216', 'WAD 2', 'IS111, IS113')
;

-- --------------------------------------------------------

--
-- Table structure for table `graded_quiz`
--

DROP TABLE IF EXISTS `graded_quiz`;
CREATE TABLE IF NOT EXISTS `graded_quiz` (
  `CID` varchar(64) NOT NULL,
  `LID` int(10) NOT NULL,
  `SID` varchar(64) NOT NULL,
  `question` varchar(1000) NOT NULL,
  `answer` varchar(64) NOT NULL,
  `options` varchar(1000) NOT NULL,
  PRIMARY KEY (`CID`, `LID`, `SID`, `question`),
 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `graded_quiz`
--

INSERT INTO `graded_quiz` (`CID`, `LID`, `SID`, `question`, `answer`, `options`) VALUES
('SPACE CLASS', 1, 'G2', 'Is the moon round?', 'YES', 'YES|NO' ),
('SPACE CLASS', 2, 'G2', 'Is the sun round?', 'YES', 'YES|NO' ),
('SPACE CLASS', 3, 'G2', 'Which of these is not a planet ?', 'Pluto', 'EARTH|MARS|JUPITER|PLUTO|VENUS' ),
;

-- --------------------------------------------------------

--
-- Table structure for table `ungraded_quiz`
--

DROP TABLE IF EXISTS `ungraded_quiz`;
CREATE TABLE IF NOT EXISTS `ungraded_quiz` (
  `CID` varchar(64) NOT NULL,
  `LID` int(10) NOT NULL,
  `SID` varchar(64) NOT NULL,
  `question` varchar(1000) NOT NULL,
  `answer` varchar(64) NOT NULL,
  `options` varchar(1000) NOT NULL,
  PRIMARY KEY (`CID`, `LID`, `SID`, `question`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ungraded_quiz`
--

INSERT INTO `ungraded_quiz` (`CID`, `LID`, `SID`, `question`, `answer`, `options`) VALUES
('SPACE CLASS', 1, 'G2', 'Is the moon round?', 'YES', 'YES|NO' ),
('SPACE CLASS', 1, 'G2', 'Is the sun round?', 'YES', 'YES|NO' ),
('SPACE CLASS', 1, 'G2', 'Which of these is not a planet?', 'Pluto', 'EARTH|MARS|JUPITER|PLUTO|VENUS' ),
;

-- --------------------------------------------------------
--
-- Table structure for table `section`
--

DROP TABLE IF EXISTS `section`;
CREATE TABLE IF NOT EXISTS `section` (
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `vacancy` int(10) NOT NULL,
  `TID` int(10) NOT NULL, 
  constraint `section_fk1` foreign key(`CID`) references `course`(`CID`),
  constraint `section_fk2` foreign key(`TID`) references `trainer`(`TID`),
  PRIMARY KEY (`SID`, `CID`, `start`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `section`
--

INSERT INTO `section` (`SID`, `CID`, `start`, `end`, `vacancy`, `TID`) VALUES
('G1', 'IS111', 2021-04-01, 2021-06-01, 40, 001),
('G2', 'IS111', 2021-05-01, 2021-07-01, 40, 001),
('G1', 'IS112', 2021-04-01, 2021-06-01, 40, 001),
('G2', 'IS112', 2021-05-01, 2021-07-01, 40, 001),
('G1', 'IS113', 2021-04-01, 2021-06-01, 40, 001),
('G2', 'IS113', 2021-05-01, 2021-07-01, 40, 001),
('G1', 'IS216', 2021-04-01, 2021-06-01, 40, 001),
('G2', 'IS216', 2021-05-01, 2021-07-01, 40, 001)
;

-- --------------------------------------------------------

--
-- Table structure for table `academic_record`
--

DROP TABLE IF EXISTS `academic_record`;
CREATE TABLE IF NOT EXISTS `academic_record` (
  `EID` int(10) NOT NULL,
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `QID` int(10) NOT NULL, 
  `status` varchar(64) NOT NULL,
  `quiz_result` int(10) DEFAULT 00,
  constraint `academic_record_fk1` foreign key(`EID`) references `engineer`(`EID`),
  constraint `academic_record_fk2` foreign key(`SID`,`CID`) references `section`(`SID`,`CID`),
  constraint `academic_record_fk3` foreign key(`QID`) references `quiz`(`QID`),
  PRIMARY KEY (`EID`, `SID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `academic_record`
--

INSERT INTO `academic_record` (`EID`, `SID`, `CID`, `QID`, `status`) VALUES
(001, 'G1', 'IS111', 001, 'ongoing'),
(001, 'G2', 'IS112', 002, 'ongoing'),
(002, 'G1', 'IS111', 001, 'completed')
;

-- --------------------------------------------------------

--
-- Table structure for table `section_content`
--

DROP TABLE IF EXISTS `section_content`;
CREATE TABLE IF NOT EXISTS `section_content` (
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `QID` int(10) NOT NULL, 
  `content_type` varchar(64) NOT NULL,
  `content_name` varchar(64) NOT NULL,
  `link` varchar(64) NOT NULL,
  constraint `section_content_fk1` foreign key(`SID`,`CID`) references `section`(`SID`,`CID`),
  constraint `section_content_fk2` foreign key(`QID`) references `quiz`(`QID`),
  PRIMARY KEY (`SID`, `CID`, `content_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `section_content`
--

INSERT INTO `section_content` (`SID`, `CID`, `QID`, `content_type`, `content_name`, `link`) VALUES
('G1', 'IS111', 001, 'pdf', 'Lesson 1 slides', 'abd.com/shared/fuie894'),
('G1', 'IS111', 001, 'pdf', 'Lesson 2 slides', 'abd.com/shared/fuie895'),
('G1', 'IS111', 001, 'pdf', 'Lesson 3 slides', 'abd.com/shared/fuie896')
;

-- --------------------------------------------------------

--
-- Table structure for table `enrollment`
--

DROP TABLE IF EXISTS `enrollment`;
CREATE TABLE IF NOT EXISTS `enrollment` (
  `EID` int(64) NOT NULL,
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  constraint `enrollment_fk1` foreign key(`EID`) references `engineer`(`EID`),
  constraint `enrollment_fk2` foreign key(`SID`,`CID`) references `section`(`SID`,`CID`),
  PRIMARY KEY (`EID`, `SID`, `CID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `enrollment`
--

INSERT INTO `enrollment` (`EID`,`SID`, `CID`) VALUES
(001, 'G1', 'IS113'),
(001, 'G2', 'IS216')
;

-- --------------------------------------------------------

--
-- Table structure for table `lesson`
--

DROP TABLE IF EXISTS `lesson`;
CREATE TABLE IF NOT EXISTS `lesson` (
  `LID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `SID` varchar(64) NOT NULL, 
  constraint `lesson_fk1` foreign key(`CID`,`SID`) references `section`(`CID`,`SID`),
  PRIMARY KEY (`LID`, `CID`, `SID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `lesson`
--

INSERT INTO `lesson` (`LID`,`CID`,`SID`) VALUES
('1', 'IS111', 'G1'),
('2', 'IS111', 'G1'),
('1', 'IS112', 'G2')
;

-- --------------------------------------------------------



