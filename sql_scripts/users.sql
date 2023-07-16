CREATE TABLE users (
  id SERIAL NOT NULL,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users (username,password) VALUES ('admin','admin');