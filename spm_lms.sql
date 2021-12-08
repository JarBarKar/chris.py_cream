--
-- Database: `spm_lms`
--
DROP DATABASE IF EXISTS `spm_lms`;
CREATE DATABASE IF NOT EXISTS `spm_lms` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `spm_lms`;

-- --------------------------------------------------------
--
-- Setting datetime format for database
--
-- Set DateFormat YMD --indicates the general format is Year Month Day 

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
CREATE TABLE IF NOT EXISTS `employee` (
  `username` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `current_designation` varchar(64) NOT NULL,
  `department` varchar(64) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`username`, `name`, `current_designation`, `department`) VALUES
('Winnie.2021', 'Winnie', 'worker', 'sales'),
('Mary.2021', 'Mary', 'worker', 'sales'),
('Luke.2021', 'Luke', 'manager', 'sales'),
('Chris.2021', 'Chris', 'manager', 'sales'),
('Joseph.2021', 'Joseph', 'manager', 'sales'),
('God.2021', 'God', 'manager', 'sales')
;


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
  `username` varchar(64) NOT NULL,
  constraint `engineer_fk1` foreign key(`username`) references `employee`(`username`),
  PRIMARY KEY (`EID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `engineer`
--

INSERT INTO `engineer` (`name`, `password`, `phone`, `email`, `address`, `username`) VALUES
('Winnie', 'ILOVEHONEY', 999, "winnie@gmail.com", "81 Victoria St, Singapore 188065", 'Winnie.2021'),
('Mary', 'WHERESMYLAMB', 911, "mary@gmail.com", "81 Victoria St, Singapore 188065", 'Mary.2021'),
('Luke', 'NOTMYFATHER', 995, "luke@gmail.com", "81 Victoria St, Singapore 188065", 'Luke.2021')
;

-- --------------------------------------------------------
--
-- Table structure for table `trainer`
--

DROP TABLE IF EXISTS `trainer`;
CREATE TABLE IF NOT EXISTS `trainer` (
  `TID` int(10) NOT NULL,
  `name` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `phone` int(8) NOT NULL,
  `email` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  constraint `trainer_fk1` foreign key(`username`) references `employee`(`username`),
  PRIMARY KEY (`TID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `trainer`
--

INSERT INTO `trainer` (`TID`, `name`, `password`, `phone`, `email`, `address`, `username`) VALUES
(001, 'Chris', 'flat white', 888, "chris@gmail.com", "81 Victoria St, Singapore 188065", 'Chris.2021'),
(002, 'Joseph', 'product manager', 123, "joseph@gmail.com", "81 Victoria St, Singapore 188065", 'Joseph.2021'),
(003, 'God', 'GPA 4', 444, "god@gmail.com", "81 Victoria St, Singapore 188065", 'God.2021')
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
('IS113', 'WAD 1', ''),
('IS216', 'WAD 2', 'IS111, IS113')

;

-- --------------------------------------------------------
--
-- Table structure for table `section`
--

DROP TABLE IF EXISTS `section`;
CREATE TABLE IF NOT EXISTS `section` (
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `TID` int(10) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `vacancy` int(10) NOT NULL,
  constraint `section_fk1` foreign key(`CID`) references `course`(`CID`),
  constraint `section_fk2` foreign key(`TID`) references `trainer`(`TID`),
  PRIMARY KEY (`SID`, `CID`, `start`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `section`
--

INSERT INTO `section` (`SID`, `CID`, `TID`, `start`, `end`, `vacancy`) VALUES
('G1', 'IS111', 001, CAST('2021-04-01 09:15:00' AS datetime), CAST('2021-06-01 18:00:00' AS datetime), 40),
('G2', 'IS111', 001, CAST('2021-05-01 09:15:00' AS datetime), CAST('2021-07-01 18:00:00' AS datetime), 40),
('G1', 'IS112', 002, CAST('2021-04-01 09:15:00' AS datetime), CAST('2021-06-01 18:00:00' AS datetime), 40),
('G2', 'IS112', 002, CAST('2021-05-01 09:15:00' AS datetime), CAST('2021-07-01 18:00:00' AS datetime), 40),
('G1', 'IS113', 003, CAST('2021-04-01 09:15:00' AS datetime), CAST('2021-06-01 18:00:00' AS datetime), 40),
('G2', 'IS113', 003, CAST('2021-05-01 09:15:00' AS datetime), CAST('2021-07-01 18:00:00' AS datetime), 40),
('G2', 'IS216', 001, CAST('2021-05-01 09:15:00' AS datetime), CAST('2021-07-01 18:00:00' AS datetime), 40)
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
  `start` datetime NOT NULL, 
  constraint `lesson_fk1` foreign key(`SID`,`CID`, `start`) references `section`(`SID`,`CID`, `start`),
  PRIMARY KEY (`LID`, `SID`, `CID`, `start`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `lesson`
--


INSERT INTO `lesson` (`LID`,`SID`,`CID`, `start`) VALUES
('1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime)),
('2', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime)),
('3', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime)),
('1', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime)),
('2', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime)),
('3', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime))
;

-- --------------------------------------------------------

--
-- Table structure for table `quiz_questions`
--

DROP TABLE IF EXISTS `quiz_questions`;
CREATE TABLE IF NOT EXISTS `quiz_questions` (
  `LID` varchar(64) NOT NULL,
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `start` datetime NOT NULL ,
  `question` varchar(64) NOT NULL,
  `answer` varchar(64) NOT NULL,
  `options` varchar(64) NOT NULL,
  `duration` int(10) NOT NULL,
  `type` varchar(64) NOT NULL,
  constraint `quiz_questions_fk1` foreign key(`LID`,`SID`,`CID`,`start`) references `lesson`(`LID`,`SID`,`CID`,`start`),
  PRIMARY KEY (`LID`, `SID`, `CID`, `start`, `question`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --
-- -- Dumping data for table `quiz_questions`
-- --

INSERT INTO `quiz_questions` (`LID`, `SID`,  `CID`, `start`, `question`, `answer`, `options`, `duration`, `type`) VALUES
('1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Is the moon round?', 'YES', 'YES|NO',  60, 'ungraded'),
('1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Is the sun round?', 'YES', 'YES|NO',  60, 'ungraded'),
('1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Which of these is not a planet ?', 'PLUTO', 'EARTH|MARS|JUPITER|PLUTO|VENUS',  60, 'ungraded'),
('2', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Bla bla black sheep have you any ?', 'WOLF', 'FOOD|WOLF|CAT|HUMAN',  60, 'ungraded'),
('2', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Mary had a little ?', 'LAMB', 'COW|LAMP|LAMB',  60, 'ungraded'),
('2', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Do you want to pass ?', 'YES', 'YES|NO',  60, 'ungraded'),
('3', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Is Aaron a boy ?', 'YES', 'YES|NO',  30, 'graded'),
('3', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Is Ivan a boy ?', 'YES', 'YES|NO',  30, 'graded')
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
  `start` datetime NOT NULL,
  `status` varchar(64) NOT NULL,
  constraint `academic_record_fk1` foreign key(`EID`) references `engineer`(`EID`),
  constraint `academic_record_fk2` foreign key(`SID`,`CID`,`start`) references `section`(`SID`,`CID`,`start`),
  PRIMARY KEY (`EID`, `SID`, `CID`, `start`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `academic_record`
--

INSERT INTO `academic_record` (`EID`, `SID`, `CID`, `start`, `status`) VALUES
(001, 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'ongoing'),
(001, 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), 'ongoing'),
(002, 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'completed')
;

-- --------------------------------------------------------

--
-- Table structure for table `content`
--

DROP TABLE IF EXISTS `content`;
CREATE TABLE IF NOT EXISTS `content` (
  `LID` varchar(64) NOT NULL, 
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `start` datetime NOT NULL,
  `content_type` varchar(64) NOT NULL,
  `content_name` varchar(64) NOT NULL,
  `link` varchar(64) NOT NULL,
  constraint `content_fk1` foreign key(`LID`,`SID`,`CID`,`start`) references `lesson`(`LID`,`SID`,`CID`,`start`),
  PRIMARY KEY (`LID`, `SID`, `CID`, `start`, `content_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `content`
--

INSERT INTO `content` (`LID`, `SID`, `CID`, `start`, `content_type`, `content_name`, `link`) VALUES
('1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'pdf', 'Lesson 1 slides', 'https://tinyurl.com/3yr5dnus'),
('2', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'pdf', 'Lesson 2 slides', 'https://tinyurl.com/3yr5dnus'),
('3', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'pdf', 'Lesson 3 slides', 'https://tinyurl.com/3yr5dnus'),
('1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'pdf', 'Lesson 1 slides part 2', 'https://tinyurl.com/3yr5dnus'),
('1', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), 'pdf', 'Lesson 1 How to train dragons', 'https://tinyurl.com/3yr5dnus'),
('1', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), 'pdf', 'Lesson 1 How get free money', 'https://tinyurl.com/3yr5dnus'),
('1', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), 'pdf', 'Lesson 1 Reflections', 'https://tinyurl.com/3yr5dnus'),
('2', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), 'pdf', 'Lesson 2 History of Avarta', 'https://tinyurl.com/3yr5dnus'),
('2', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), 'pdf', 'Lesson 2 Why is machine learning so hard?', 'https://tinyurl.com/3yr5dnus'),
('3', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), 'pdf', 'Lesson 3 Convolution Neural Network', 'https://tinyurl.com/3yr5dnus'),
('3', 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), 'pdf', 'Lesson 3 Backward and forward propagation in neural network', 'https://tinyurl.com/3yr5dnus')
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
  `start` datetime NOT NULL,
  constraint `enrollment_fk1` foreign key(`EID`) references `engineer`(`EID`),
  constraint `enrollment_fk2` foreign key(`SID`, `CID`, `start`) references `section`(`SID`, `CID`,`start`),
  PRIMARY KEY (`EID`, `SID`, `CID`, `start`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `enrollment`
--



-- --------------------------------------------------------
--
-- Table structure for table `quiz_record`
--

DROP TABLE IF EXISTS `quiz_record`;
CREATE TABLE IF NOT EXISTS `quiz_record` (
  `EID` int(10) NOT NULL,
  `LID` varchar(64) NOT NULL,
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `start` datetime NOT NULL,
  `question` varchar(64) NOT NULL,
  `answer_given` varchar(64) NOT NULL,
  `marks` int(10) NOT NULL DEFAULT 0,
  constraint `quiz_record_fk1` foreign key(`EID`) references `engineer`(`EID`),
  -- constraint `quiz_record_fk2` foreign key(`LID`,`SID`,`CID`,`start`,`question`) references `quiz_questions`(`LID`,`SID`,`CID`,`start`,`question`),
  PRIMARY KEY (`EID`,`LID`, `SID`, `CID`, `start`,`question`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `quiz_record`
--

INSERT INTO `quiz_record` (`EID`, `LID`, `SID`, `CID`, `start`, `question`, `answer_given`, `marks`) VALUES
(001, '1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Is the moon round?', 'YES', 1),
(001, '1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Is the sun round?', 'NO', 0),
(001, '1', 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), 'Which of these is not a planet ?', 'EARTH', 0)
;

-- --------------------------------------------------------
--
-- Table structure for table `progress`
--

DROP TABLE IF EXISTS `progress`;
CREATE TABLE IF NOT EXISTS `progress` (
  `EID` int(10) NOT NULL,
  `SID` varchar(64) NOT NULL,
  `CID` varchar(64) NOT NULL,
  `start` datetime NOT NULL,
  `latest_lesson_reached` varchar(64) NOT NULL,
  `recent_content_name` varchar(64) NOT NULL,
  `viewed_contents` varchar(64) NOT NULL,
  constraint `progress_fk1` foreign key(`EID`) references `engineer`(`EID`),
  PRIMARY KEY (`EID`, `SID`, `CID`, `start`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `progress`
--

INSERT INTO `progress` (`EID`, `SID`, `CID`, `start`, `latest_lesson_reached`, `recent_content_name`, `viewed_contents`) VALUES
(001, 'G1', 'IS111', CAST('2021-04-01 09:15:00' AS datetime), '2', 'Lesson 2 slides', 'Lesson 2 slides'),
(001, 'G2', 'IS112', CAST('2021-05-01 09:15:00' AS datetime), '1', 'Lesson 1 How get free money', 'Lesson 1 How to train dragons|Lesson 1 How get free money')
;

-- --------------------------------------------------------




