CREATE TABLE sites (
  location VARCHAR(150) NOT NULL,
  title VARCHAR(200) NOT NULL,
  startDate TIMESTAMP NOT NULL,
  endDate TIMESTAMP,
  description  VARCHAR(1500) NOT NULL,
  price NUMERIC,
  link VARCHAR(500) PRIMARY KEY);