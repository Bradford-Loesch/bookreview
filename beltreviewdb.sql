-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema BookReview
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema BookReview
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `BookReview` DEFAULT CHARACTER SET utf8 ;
USE `BookReview` ;

-- -----------------------------------------------------
-- Table `BookReview`.`Author`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BookReview`.`Author` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BookReview`.`Book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BookReview`.`Book` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `Author_id` INT NOT NULL,
  PRIMARY KEY (`id`, `Author_id`),
  INDEX `fk_Book_Author1_idx` (`Author_id` ASC),
  CONSTRAINT `fk_Book_Author1`
    FOREIGN KEY (`Author_id`)
    REFERENCES `BookReview`.`Author` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BookReview`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BookReview`.`User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `BookReview`.`Review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `BookReview`.`Review` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rating` INT NULL,
  `comment` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `User_id` INT NOT NULL,
  `Book_id` INT NOT NULL,
  PRIMARY KEY (`id`, `User_id`, `Book_id`),
  INDEX `fk_Review_User1_idx` (`User_id` ASC),
  INDEX `fk_Review_Book1_idx` (`Book_id` ASC),
  CONSTRAINT `fk_Review_User1`
    FOREIGN KEY (`User_id`)
    REFERENCES `BookReview`.`User` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Review_Book1`
    FOREIGN KEY (`Book_id`)
    REFERENCES `BookReview`.`Book` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
