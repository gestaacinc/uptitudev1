-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 07, 2024 at 10:39 AM
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
-- Database: `uptitudev2`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('f38dbfe49a77');

-- --------------------------------------------------------

--
-- Table structure for table `audit_logs`
--

CREATE TABLE `audit_logs` (
  `id` int(11) NOT NULL,
  `staff_id` int(11) DEFAULT NULL,
  `action` varchar(255) DEFAULT NULL,
  `details` text DEFAULT NULL,
  `module` enum('courses','enrollees','payments','documents') DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` int(11) NOT NULL,
  `course_name` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `type` enum('TESDA','Regular') DEFAULT NULL,
  `qualification_type` enum('NC1','NC2','NC3','NTR') DEFAULT NULL,
  `fee` decimal(10,2) DEFAULT NULL,
  `assessment_fee` decimal(10,2) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `status` enum('active','archived') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp(),
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `course_name`, `description`, `type`, `qualification_type`, `fee`, `assessment_fee`, `duration`, `status`, `created_at`, `updated_at`, `created_by`, `updated_by`) VALUES
(1, 'Course 1', 'Description 1', 'TESDA', 'NC1', 5000.00, 1000.00, 45, 'active', '2024-12-07 06:01:22', '2024-12-07 06:01:22', NULL, NULL),
(2, 'Course 2', 'Description 2', 'TESDA', 'NC2', 4500.00, 900.00, 40, 'active', '2024-12-07 06:01:22', '2024-12-07 06:01:22', NULL, NULL),
(3, 'Course 3', 'Description 3', 'TESDA', 'NC3', 5500.00, 1100.00, 50, 'active', '2024-12-07 06:01:22', '2024-12-07 06:01:22', NULL, NULL),
(27, 'Computer Systems Servicing', 'ELECTRONICS SECTOR', 'TESDA', 'NC2', 37890.00, NULL, 35, 'active', '2024-12-07 03:42:43', '2024-12-07 03:42:43', NULL, NULL),
(28, 'Web Development', 'ICT', 'TESDA', 'NC3', 40000.00, NULL, 3189, 'active', '2024-12-07 03:43:24', '2024-12-07 03:43:24', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `id` int(11) NOT NULL,
  `enrollee_id` int(11) DEFAULT NULL,
  `document_name` varchar(255) DEFAULT NULL,
  `required_by` date DEFAULT NULL,
  `submitted` tinyint(1) DEFAULT NULL,
  `status` enum('Pending','Incomplete','Approved') DEFAULT 'Pending',
  `file_path` varchar(255) DEFAULT NULL,
  `uploaded_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`id`, `enrollee_id`, `document_name`, `required_by`, `submitted`, `status`, `file_path`, `uploaded_at`, `created_at`, `updated_at`) VALUES
(7, 36, 'diploma', NULL, 0, 'Approved', 'C:\\Users\\Tech\\documents\\project\\uploads\\36\\WEB DEVELOPMENT NC.pdf', NULL, '2024-12-07 09:01:11', '2024-12-07 09:01:11'),
(8, 36, 'form137', NULL, 0, 'Approved', 'C:\\Users\\Tech\\documents\\project\\uploads\\36\\WEB DEVELOPMENT NC (1).pdf', NULL, '2024-12-07 09:01:12', '2024-12-07 09:01:12'),
(9, 36, 'birthCertificate', NULL, 0, 'Approved', 'C:\\Users\\Tech\\documents\\project\\uploads\\36\\Image (118).jpg', NULL, '2024-12-07 09:01:13', '2024-12-07 09:01:13'),
(10, 37, 'diploma', NULL, 0, 'Approved', 'C:\\Users\\Tech\\documents\\project\\uploads\\37\\465021853_1298462171474658_5063861563615385900_n.jpg', NULL, '2024-12-07 09:38:02', '2024-12-07 09:38:02'),
(11, 37, 'form137', NULL, 0, 'Approved', 'C:\\Users\\Tech\\documents\\project\\uploads\\37\\viber_image_2024-11-28_10-42-37-245.jpg', NULL, '2024-12-07 09:38:07', '2024-12-07 09:38:07'),
(12, 37, 'birthCertificate', NULL, 0, 'Approved', 'C:\\Users\\Tech\\documents\\project\\uploads\\37\\screencapture-192-168-1-9-8080-2024-11-25-09_05_03.png', NULL, '2024-12-07 09:38:12', '2024-12-07 09:38:12');

-- --------------------------------------------------------

--
-- Table structure for table `enrollees`
--

CREATE TABLE `enrollees` (
  `id` int(11) NOT NULL,
  `enrollee_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `contact_info` varchar(50) DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `date_of_enrollment` date DEFAULT NULL,
  `enrollment_status` enum('Pending','Ongoing','Completed') DEFAULT NULL,
  `completion_date` date DEFAULT NULL,
  `total_fee` decimal(10,2) DEFAULT NULL,
  `balance` decimal(10,2) DEFAULT 0.00,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp(),
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `enrollees`
--

INSERT INTO `enrollees` (`id`, `enrollee_name`, `email`, `contact_info`, `photo_path`, `address`, `course_id`, `date_of_enrollment`, `enrollment_status`, `completion_date`, `total_fee`, `balance`, `created_at`, `updated_at`, `created_by`, `updated_by`) VALUES
(36, 'Chester Bautista', 'cfbautista.official.01@gmail.com', '09167252664', NULL, '348 Sta Maria Street\nBonuan Boquig, Dagupan City', 2, '2024-12-26', 'Pending', NULL, NULL, 4000.00, '2024-12-07 09:00:28', '2024-12-07 09:00:46', NULL, NULL),
(37, 'Ryan Lim', 'ryan@mail.com', '094586585', NULL, 'adfadfdfdf', 28, '2024-12-10', 'Pending', '2033-09-03', NULL, 39700.00, '2024-12-07 09:37:19', '2024-12-07 09:37:41', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `fee_breakdowns`
--

CREATE TABLE `fee_breakdowns` (
  `id` int(11) NOT NULL,
  `enrollee_id` int(11) DEFAULT NULL,
  `fee_type` enum('Assessment','TESDA Certification') DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `enrollee_id` int(11) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `payment_type` enum('Down Payment','Second Payment','Third Payment') DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_method` enum('Cash','GCash','Bank Transfer') DEFAULT NULL,
  `transaction_id` varchar(255) DEFAULT NULL,
  `payment_for` enum('Training','Assessment','TESDA Certification') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`id`, `enrollee_id`, `payment_date`, `payment_type`, `amount`, `payment_method`, `transaction_id`, `payment_for`, `created_at`, `updated_at`) VALUES
(3, 36, '2024-12-07', 'Down Payment', 500.00, 'Cash', NULL, 'Training', '2024-12-07 09:00:46', '2024-12-07 09:00:46'),
(4, 37, '2024-12-07', 'Down Payment', 300.00, 'Cash', NULL, 'Training', '2024-12-07 09:37:41', '2024-12-07 09:37:41');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` enum('ADMIN','FINANCE','STAFF') DEFAULT NULL,
  `login_attempts` int(11) DEFAULT NULL,
  `lockout_until` datetime DEFAULT NULL,
  `status` enum('ACTIVE','INACTIVE') DEFAULT 'ACTIVE',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp(),
  `password_hash` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`id`, `name`, `email`, `role`, `login_attempts`, `lockout_until`, `status`, `created_at`, `updated_at`, `password_hash`) VALUES
(7, 'Admin User', 'cfbautista.official.01@gmail.com', 'ADMIN', 0, NULL, 'ACTIVE', '2024-12-01 15:41:20', '2024-12-07 02:22:43', 'scrypt:32768:8:1$7G287KQwNjr1uHNx$a1166be73f3879497176f2f85ef6ef5ee1f9006c579617097f480418fb71764cea0ded536d6f568273c48d50397943454c0a98440c99284f2c2fb0965b77000e'),
(8, 'Finance User', 'finance@example.com', 'FINANCE', 0, NULL, 'ACTIVE', '2024-12-01 15:41:20', '2024-12-01 15:41:20', 'scrypt:32768:8:1$om8fQsmVNIgh0L0C$a18436f2329d6fd1cc954efde5b4f2de088745cfca171f6e394111bbde88e300f8b2f969fac0346c565a77f11e88fc474eca6e91fa49bda2a61b16daab6f3535'),
(9, 'Staff User', 'staff@example.com', 'STAFF', 0, NULL, 'ACTIVE', '2024-12-01 15:41:20', '2024-12-01 15:41:20', 'scrypt:32768:8:1$Bv0Oe4drzuiAJqJG$3a17c185a7524a9101581d79d34a08a5da28cba4100bfe938bc653c89d3b4d4777142a4931fbbf7654675c61e1359fad1ab6148bd0c955cbcca359c87e13ae93');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `staff_id` (`staff_id`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `course_name` (`course_name`),
  ADD KEY `fk_courses_created_by` (`created_by`),
  ADD KEY `fk_courses_updated_by` (`updated_by`);

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `enrollee_id` (`enrollee_id`);

--
-- Indexes for table `enrollees`
--
ALTER TABLE `enrollees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_enrollees_created_by` (`created_by`),
  ADD KEY `fk_enrollees_updated_by` (`updated_by`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `fee_breakdowns`
--
ALTER TABLE `fee_breakdowns`
  ADD PRIMARY KEY (`id`),
  ADD KEY `enrollee_id` (`enrollee_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `enrollee_id` (`enrollee_id`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_staff_email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `audit_logs`
--
ALTER TABLE `audit_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `enrollees`
--
ALTER TABLE `enrollees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `fee_breakdowns`
--
ALTER TABLE `fee_breakdowns`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `audit_logs`
--
ALTER TABLE `audit_logs`
  ADD CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`);

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `fk_courses_created_by` FOREIGN KEY (`created_by`) REFERENCES `staff` (`id`),
  ADD CONSTRAINT `fk_courses_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `staff` (`id`);

--
-- Constraints for table `documents`
--
ALTER TABLE `documents`
  ADD CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`enrollee_id`) REFERENCES `enrollees` (`id`);

--
-- Constraints for table `enrollees`
--
ALTER TABLE `enrollees`
  ADD CONSTRAINT `enrollees_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  ADD CONSTRAINT `fk_enrollees_created_by` FOREIGN KEY (`created_by`) REFERENCES `staff` (`id`),
  ADD CONSTRAINT `fk_enrollees_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `staff` (`id`);

--
-- Constraints for table `fee_breakdowns`
--
ALTER TABLE `fee_breakdowns`
  ADD CONSTRAINT `fee_breakdowns_ibfk_1` FOREIGN KEY (`enrollee_id`) REFERENCES `enrollees` (`id`);

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`enrollee_id`) REFERENCES `enrollees` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
