DROP DATABASE IF EXISTS scrape_database;
CREATE DATABASE scrape_database;
USE scrape_database;
DROP TABLE IF EXISTS scrape_data;

CREATE TABLE scrape_data (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  tw_id BIGINT NOT NULL, 
  user_name TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  text TEXT NOT NULL,
  url TEXT NOT NULL,
  og_site_name TEXT,
  og_title TEXT,
  og_description TEXT
);

CREATE TABLE train_data(
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  scrape_id INT NOT NULL,
  category_id Int NOT NULL,
  UNIQUE (scrape_id, category_id),
  FOREIGN KEY(scrape_id) REFERENCES scrape_data(id),
  FOREIGN KEY(category_id) REFERENCES category_data(id)
);


CREATE TABLE category_data(
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  category_name TEXT NOT NULL
);