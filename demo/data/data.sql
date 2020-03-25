-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: online_social_networks
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `weibo_user_profile`
--

DROP TABLE IF EXISTS `weibo_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weibo_user_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `weibo_num` varchar(255) DEFAULT NULL,
  `following` varchar(255) DEFAULT NULL,
  `follower` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weibo_user_profile`
--

LOCK TABLES `weibo_user_profile` WRITE;
/*!40000 ALTER TABLE `weibo_user_profile` DISABLE KEYS */;
INSERT INTO `weibo_user_profile` VALUES

(43,'答与不答','6574167541','63','238','71'),
(44,'沙丁鱼哦','5543580678','62','29','36'),
(45,'纪念10月离去的你','2641472087','82','533','46'),
(46,'那一朵向阳花花','3717084375','316','236','116'),
(47,'殷彩鹤','6293376227','46','202','20'),
(48,'雪影飞菲','5114142824','51','108','26'),
(49,'腻撑2018','1855825885','9','221','40'),
(50,'花落夏寂','5594064831','214','348','29'),
(51,'YunWorkbench','3779064072','12','362','40'),
(52,'主义一定要实现','1776824593','218','152','78'),

