-- MySQL Script generated by MySQL Workbench
-- Sun May 19 23:43:48 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema TP_PROGRAMACION3
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema TP_PROGRAMACION3
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `TP_PROGRAMACION3` DEFAULT CHARACTER SET utf8 ;
USE `TP_PROGRAMACION3` ;

-- -----------------------------------------------------
-- Table `TP_PROGRAMACION3`.`HABITACIONES`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TP_PROGRAMACION3`.`HABITACIONES` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `TIPO` VARCHAR(15) NOT NULL,
  `COSTO` INT NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TP_PROGRAMACION3`.`REGISTROS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TP_PROGRAMACION3`.`REGISTROS` (
  `IDREGISTROS` INT NOT NULL AUTO_INCREMENT,
  `NUMERO` INT NOT NULL,
  `TIPO` VARCHAR(15) NOT NULL,
  `COSTO` INT NOT NULL,
  `DIAS` INT NOT NULL,
  `PAGO` VARCHAR(2) NOT NULL,
  `SUBTOTAL` INT NOT NULL,
  `DESCUENTO` INT NOT NULL,
  `TOTAL` INT NOT NULL,
  `ESTADO` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`IDREGISTROS`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
