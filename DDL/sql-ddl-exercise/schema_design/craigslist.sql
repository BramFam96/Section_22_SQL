DROP DATABASE IF EXISTS mock_craigslist_db;
CREATE DATABASE mock_craigslist_db;

\c mock_craigslist_db;
CREATE TABLE country (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE 
);

CREATE TABLE region (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE,
  country_id INTEGER REFERENCES country ON DELETE SET NULL
);
CREATE TABLE category (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE
);
CREATE TABLE users(
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE,
  preferred_region TEXT REFERENCES region(name) ON DELETE SET NULL
);
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title varchar(20) UNIQUE NOT NULL,
  description varchar(250) NOT NULL,
  location TEXT NOT NULL,
  user_id INTEGER REFERENCES users ON DELETE SET NULL,
  cat TEXT REFERENCES category(name) ON DELETE CASCADE,
  region TEXT REFERENCES region(name) ON DELETE SET NULL,
  country TEXT REFERENCES country(name) ON DELETE SET NULL
);