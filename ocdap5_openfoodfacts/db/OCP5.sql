-- -----------------------------------------------------
-- Schema OCP5
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `OCP5` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `OCP5` ;

-- -----------------------------------------------------
-- Table `OCP5`.`brand`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`brand` (
  `brand_id` INT NOT NULL AUTO_INCREMENT,
  `brand_name` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`brand_id`),
  UNIQUE INDEX `brand_name` (`brand_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 1091
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `OCP5`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`category` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(45) NOT NULL,
  `is_beverage` TINYINT(1) NULL DEFAULT NULL,
  `is_food` TINYINT(1) NULL DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE INDEX `category_name` (`category_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 1731
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `OCP5`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(55) NOT NULL,
  `main_group` VARCHAR(55) NOT NULL,
  `description` VARCHAR(170) NOT NULL,
  `nutriscore` VARCHAR(2) NOT NULL,
  `ingredients` VARCHAR(300) NOT NULL,
  `url` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5900
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `OCP5`.`l_brand_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`l_brand_product` (
  `fk_product_id` INT NULL DEFAULT NULL,
  `fk_brand_id` INT NULL DEFAULT NULL,
  INDEX `fk_product_id` (`fk_product_id` ASC) VISIBLE,
  INDEX `fk_brand_id` (`fk_brand_id` ASC) VISIBLE,
  CONSTRAINT `l_brand_product_ibfk_1`
    FOREIGN KEY (`fk_product_id`)
    REFERENCES `OCP5`.`product` (`id`),
  CONSTRAINT `l_brand_product_ibfk_2`
    FOREIGN KEY (`fk_brand_id`)
    REFERENCES `OCP5`.`brand` (`brand_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `OCP5`.`l_category_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`l_category_product` (
  `fk_product_id` INT NULL DEFAULT NULL,
  `fk_category_id` INT NULL DEFAULT NULL,
  INDEX `fk_product_id` (`fk_product_id` ASC) VISIBLE,
  INDEX `fk_category_id` (`fk_category_id` ASC) VISIBLE,
  CONSTRAINT `l_category_product_ibfk_1`
    FOREIGN KEY (`fk_product_id`)
    REFERENCES `OCP5`.`product` (`id`),
  CONSTRAINT `l_category_product_ibfk_2`
    FOREIGN KEY (`fk_category_id`)
    REFERENCES `OCP5`.`category` (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `OCP5`.`l_original_substitute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`l_original_substitute` (
  `favorite_id` INT NOT NULL AUTO_INCREMENT,
  `original_prod_id` INT NULL DEFAULT NULL,
  `substitute_prod_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`favorite_id`),
  INDEX `original_prod_id` (`original_prod_id` ASC) VISIBLE,
  INDEX `substitute_prod_id` (`substitute_prod_id` ASC) VISIBLE,
  CONSTRAINT `l_original_substitute_ibfk_1`
    FOREIGN KEY (`original_prod_id`)
    REFERENCES `OCP5`.`product` (`id`),
  CONSTRAINT `l_original_substitute_ibfk_2`
    FOREIGN KEY (`substitute_prod_id`)
    REFERENCES `OCP5`.`product` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `OCP5`.`store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`store` (
  `store_id` INT NOT NULL AUTO_INCREMENT,
  `store_name` VARCHAR(35) NOT NULL,
  PRIMARY KEY (`store_id`),
  UNIQUE INDEX `store_name` (`store_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 310
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `OCP5`.`l_product_store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OCP5`.`l_product_store` (
  `fk_product_id` INT NULL DEFAULT NULL,
  `fk_store_id` INT NULL DEFAULT NULL,
  INDEX `fk_product_id` (`fk_product_id` ASC) VISIBLE,
  INDEX `fk_store_id` (`fk_store_id` ASC) VISIBLE,
  CONSTRAINT `l_product_store_ibfk_1`
    FOREIGN KEY (`fk_product_id`)
    REFERENCES `OCP5`.`product` (`id`),
  CONSTRAINT `l_product_store_ibfk_2`
    FOREIGN KEY (`fk_store_id`)
    REFERENCES `OCP5`.`store` (`store_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

