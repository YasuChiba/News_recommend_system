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
  scrape_id Int UNIQUE NOT NULL,
  category Int NOT NULL,
  FOREIGN KEY(scrape_id)
  REFERENCES scrape_data(id)
);