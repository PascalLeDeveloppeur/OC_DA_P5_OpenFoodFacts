-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema OCP5
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema OCP5
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `OCP5` DEFAULT CHARACTER SET utf8 ;
USE `OCP5` ;

-- -----------------------------------------------------
-- Table `OCP5`.`P5_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`P5_product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(45) NULL,
  `nutri_score` VARCHAR(2) NULL,
  `ingredients` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OCP5`.`P5_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`P5_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OCP5`.`P5_category_has_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`P5_category_has_product` (
  `FK_category_id` INT NOT NULL,
  `FK_product_id` INT NOT NULL,
  PRIMARY KEY (`FK_category_id`, `FK_product_id`),
  INDEX `fk_P5_category_has_P5_products_P5_products1_idx` (`FK_product_id` ASC) VISIBLE,
  INDEX `fk_P5_category_has_P5_products_P5_category_idx` (`FK_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_P5_category_has_P5_products_P5_category`
    FOREIGN KEY (`FK_category_id`)
    REFERENCES `mydb`.`P5_category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_P5_category_has_P5_products_P5_products1`
    FOREIGN KEY (`FK_product_id`)
    REFERENCES `mydb`.`P5_product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OCP5`.`P5_store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`P5_store` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `store_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OCP5`.`P5_store_has_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`P5_store_has_product` (
  `P5_products_id` INT NOT NULL,
  `P5_store_id` INT NOT NULL,
  PRIMARY KEY (`P5_products_id`, `P5_store_id`),
  INDEX `fk_P5_products_has_P5_store_P5_store1_idx` (`P5_store_id` ASC) VISIBLE,
  INDEX `fk_P5_products_has_P5_store_P5_products1_idx` (`P5_products_id` ASC) VISIBLE,
  CONSTRAINT `fk_P5_products_has_P5_store_P5_products1`
    FOREIGN KEY (`P5_products_id`)
    REFERENCES `mydb`.`P5_product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_P5_products_has_P5_store_P5_store1`
    FOREIGN KEY (`P5_store_id`)
    REFERENCES `mydb`.`P5_store` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OCP5`.`P5_favorite`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`P5_favorite` (
  `P5_product_id` INT NOT NULL,
  PRIMARY KEY (`P5_product_id`),
  CONSTRAINT `fk_favorite_P5_product1`
    FOREIGN KEY (`P5_product_id`)
    REFERENCES `mydb`.`P5_product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
