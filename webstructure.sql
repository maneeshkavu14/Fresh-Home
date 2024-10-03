-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: webfarm
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `announcement`
--

DROP TABLE IF EXISTS `announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcement` (
  `aid` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(60) NOT NULL,
  `content` varchar(450) NOT NULL,
  `type` varchar(30) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `application` (
  `app_id` int NOT NULL AUTO_INCREMENT,
  `app_name` varchar(60) NOT NULL,
  `image` text NOT NULL,
  `description` varchar(300) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`app_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `crt_id` int NOT NULL AUTO_INCREMENT,
  `pro_id` int NOT NULL,
  `qnty` int NOT NULL,
  `shipping` float NOT NULL,
  `subtotal` float NOT NULL,
  `total` float NOT NULL,
  `usr_id` int NOT NULL,
  PRIMARY KEY (`crt_id`),
  KEY `usr_id_idx` (`usr_id`),
  KEY `pid_idx` (`pro_id`),
  CONSTRAINT `proid` FOREIGN KEY (`pro_id`) REFERENCES `pro_registration` (`pid`),
  CONSTRAINT `usr_id` FOREIGN KEY (`usr_id`) REFERENCES `login` (`lid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `complaint`
--

DROP TABLE IF EXISTS `complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaint` (
  `cmp_id` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `complaint` varchar(300) NOT NULL,
  `reply` varchar(300) DEFAULT NULL,
  `complaint_date` date DEFAULT NULL,
  `reply_date` datetime DEFAULT NULL,
  PRIMARY KEY (`cmp_id`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `llid` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `fid` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `subject` varchar(105) NOT NULL,
  `feedback` varchar(455) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`fid`),
  KEY `logid_idx` (`lid`),
  CONSTRAINT `logid` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `lid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(70) NOT NULL,
  `password` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orderitem`
--

DROP TABLE IF EXISTS `orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitem` (
  `o_itm` int NOT NULL AUTO_INCREMENT,
  `pid` int NOT NULL,
  `oid` int NOT NULL,
  `qnty` varchar(45) NOT NULL,
  `total` float NOT NULL,
  PRIMARY KEY (`o_itm`),
  KEY `pid_idx` (`pid`),
  KEY `oid_idx` (`oid`),
  CONSTRAINT `oid` FOREIGN KEY (`oid`) REFERENCES `orders` (`oid`),
  CONSTRAINT `pid` FOREIGN KEY (`pid`) REFERENCES `pro_registration` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `oid` int NOT NULL AUTO_INCREMENT,
  `l_id` int NOT NULL,
  `total` float NOT NULL,
  `pay_status` varchar(45) NOT NULL,
  `date` datetime NOT NULL,
  `order_status` varchar(45) NOT NULL,
  PRIMARY KEY (`oid`),
  KEY `l_id_idx` (`l_id`),
  CONSTRAINT `l_id` FOREIGN KEY (`l_id`) REFERENCES `login` (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `pay_id` int NOT NULL AUTO_INCREMENT,
  `oid` int NOT NULL,
  `amount` float NOT NULL,
  `uid` int NOT NULL,
  `card_holder_name` varchar(60) NOT NULL,
  `card_number` varchar(16) NOT NULL,
  `exp` varchar(10) NOT NULL,
  `payment_date` datetime NOT NULL,
  PRIMARY KEY (`pay_id`),
  KEY `uid_idx` (`uid`),
  KEY `odrid_idx` (`oid`),
  CONSTRAINT `odrid` FOREIGN KEY (`oid`) REFERENCES `orders` (`oid`),
  CONSTRAINT `uid` FOREIGN KEY (`uid`) REFERENCES `login` (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pro_registration`
--

DROP TABLE IF EXISTS `pro_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pro_registration` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `pname` varchar(90) NOT NULL,
  `image` text NOT NULL,
  `desc` varchar(300) NOT NULL,
  `price` float NOT NULL,
  `stock` varchar(45) NOT NULL,
  `pcid` int NOT NULL,
  `logid` int NOT NULL,
  PRIMARY KEY (`pid`),
  KEY `user_id_idx` (`logid`),
  KEY `pcid_idx` (`pcid`),
  CONSTRAINT `lid` FOREIGN KEY (`logid`) REFERENCES `login` (`lid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `pcid` FOREIGN KEY (`pcid`) REFERENCES `product_category` (`pcid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_category`
--

DROP TABLE IF EXISTS `product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_category` (
  `pcid` int NOT NULL AUTO_INCREMENT,
  `categoryname` varchar(100) NOT NULL,
  `image` text NOT NULL,
  `createdon` datetime NOT NULL,
  PRIMARY KEY (`pcid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `fname` varchar(45) DEFAULT NULL,
  `lname` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `district` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `pin` varchar(45) DEFAULT NULL,
  `society_regno` varchar(45) DEFAULT NULL,
  `adhaarno` varchar(45) DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `adrs` varchar(300) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `lid` int NOT NULL,
  `type` varchar(45) NOT NULL,
  PRIMARY KEY (`rid`),
  UNIQUE KEY `adhaarno_UNIQUE` (`adhaarno`),
  KEY `logid_idx` (`lid`),
  CONSTRAINT `user_id` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-07 16:12:48
