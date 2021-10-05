-- MariaDB dump 10.19  Distrib 10.6.3-MariaDB, for osx10.16 (x86_64)
--
-- Host: localhost    Database: pokemondb
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Gym_Leaders`
--

DROP TABLE IF EXISTS `Gym_Leaders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Gym_Leaders` (
  `leadID` int NOT NULL AUTO_INCREMENT,
  `leadName` varchar(255) NOT NULL,
  PRIMARY KEY (`leadID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gym_Leaders`
--

LOCK TABLES `Gym_Leaders` WRITE;
/*!40000 ALTER TABLE `Gym_Leaders` DISABLE KEYS */;
INSERT INTO `Gym_Leaders` VALUES (1,'Roark'),(2,'Gardenia'),(3,'Maylene'),(4,'Crasher Wake');
/*!40000 ALTER TABLE `Gym_Leaders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Locations`
--

DROP TABLE IF EXISTS `Locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Locations` (
  `locationID` int NOT NULL AUTO_INCREMENT,
  `locationName` varchar(255) NOT NULL,
  `locationBio` varchar(255) DEFAULT NULL,
  `leader` int DEFAULT NULL,
  PRIMARY KEY (`locationID`),
  KEY `leader` (`leader`),
  CONSTRAINT `Locations_ibfk_1` FOREIGN KEY (`leader`) REFERENCES `Gym_Leaders` (`leadID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Locations`
--

LOCK TABLES `Locations` WRITE;
/*!40000 ALTER TABLE `Locations` DISABLE KEYS */;
INSERT INTO `Locations` VALUES (1,'Oreburgh City','A mining town blessed with significant natural resources.',1),(2,'Route 201','A route in southwestern Sinnoh, connecting Twinleaf Town and Sandgem Town',NULL),(3,'Fuego Ironworks','Refines iron ore mined from Mt. Coronet to make iron and to manufacture mechanical parts.',NULL),(4,'Twinleaf Town ','The coziest town in the Sinnoh region',NULL);
/*!40000 ALTER TABLE `Locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Moves`
--

DROP TABLE IF EXISTS `Moves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Moves` (
  `moveID` int NOT NULL AUTO_INCREMENT,
  `moveName` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `type` int NOT NULL,
  PRIMARY KEY (`moveID`),
  KEY `type` (`type`),
  CONSTRAINT `Moves_ibfk_1` FOREIGN KEY (`type`) REFERENCES `Types` (`typeID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Moves`
--

LOCK TABLES `Moves` WRITE;
/*!40000 ALTER TABLE `Moves` DISABLE KEYS */;
INSERT INTO `Moves` VALUES (1,'Ember','Special',4),(2,'Gust','Special',3),(3,'Thundershock','Special',7),(4,'Thunderpunch','Physical',7);
/*!40000 ALTER TABLE `Moves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pokemon`
--

DROP TABLE IF EXISTS `Pokemon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pokemon` (
  `pokeID` int NOT NULL AUTO_INCREMENT,
  `pokeName` varchar(255) NOT NULL,
  `pokeBio` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pokeID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pokemon`
--

LOCK TABLES `Pokemon` WRITE;
/*!40000 ALTER TABLE `Pokemon` DISABLE KEYS */;
INSERT INTO `Pokemon` VALUES (1,'Chimchar','A small, feisty Pokemon we received from Professor Rowan.'),(2,'Starly','A species of Bird Pokemon found on Route 201'),(3,'Shinx','A quadrupedal, feline Pokémon resembling a lion cub or lynx kitten'),(4,'Electivire','A large, humanoid Pokémon covered in yellow fur with black stripes'),(6,'Squirtle','A small Pokemon that resembles a turtle');
/*!40000 ALTER TABLE `Pokemon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pokemon_Locations`
--

DROP TABLE IF EXISTS `Pokemon_Locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pokemon_Locations` (
  `sinnoh_pokemon` int NOT NULL,
  `location` int NOT NULL,
  PRIMARY KEY (`sinnoh_pokemon`,`location`),
  KEY `sinnoh_pokemon` (`sinnoh_pokemon`),
  KEY `location` (`location`),
  CONSTRAINT `Pokemon_Locations_ibfk_1` FOREIGN KEY (`sinnoh_pokemon`) REFERENCES `Pokemon` (`pokeID`) ON DELETE CASCADE,
  CONSTRAINT `Pokemon_Locations_ibfk_2` FOREIGN KEY (`location`) REFERENCES `Locations` (`locationID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pokemon_Locations`
--

LOCK TABLES `Pokemon_Locations` WRITE;
/*!40000 ALTER TABLE `Pokemon_Locations` DISABLE KEYS */;
INSERT INTO `Pokemon_Locations` VALUES (1,1),(2,2),(3,3),(4,4);
/*!40000 ALTER TABLE `Pokemon_Locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pokemon_Moves`
--

DROP TABLE IF EXISTS `Pokemon_Moves`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pokemon_Moves` (
  `sinnoh_pokemon` int NOT NULL,
  `move` int NOT NULL,
  PRIMARY KEY (`sinnoh_pokemon`,`move`),
  KEY `sinnoh_pokemon` (`sinnoh_pokemon`),
  KEY `move` (`move`),
  CONSTRAINT `Pokemon_Moves_ibfk_1` FOREIGN KEY (`sinnoh_pokemon`) REFERENCES `Pokemon` (`pokeID`) ON DELETE CASCADE,
  CONSTRAINT `Pokemon_Moves_ibfk_2` FOREIGN KEY (`move`) REFERENCES `Moves` (`moveID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pokemon_Moves`
--

LOCK TABLES `Pokemon_Moves` WRITE;
/*!40000 ALTER TABLE `Pokemon_Moves` DISABLE KEYS */;
INSERT INTO `Pokemon_Moves` VALUES (1,1),(1,2),(2,2),(3,3),(3,4);
/*!40000 ALTER TABLE `Pokemon_Moves` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Types`
--

DROP TABLE IF EXISTS `Types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Types` (
  `typeID` int NOT NULL AUTO_INCREMENT,
  `typeName` varchar(255) NOT NULL,
  `weakness` varchar(255) DEFAULT NULL,
  `strength` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`typeID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Types`
--

LOCK TABLES `Types` WRITE;
/*!40000 ALTER TABLE `Types` DISABLE KEYS */;
INSERT INTO `Types` VALUES (1,'Rock','Fighting','Flying'),(2,'Fighting','Flying','Rock'),(3,'Flying','Rock','Fighting'),(4,'Fire','Water','Grass'),(5,'Water','Grass','Fire'),(6,'Grass','Fire','Water'),(7,'Electric','Ground','Water');
/*!40000 ALTER TABLE `Types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-08-08 22:21:13
