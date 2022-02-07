
----------------------------------------------------------------------
-- Initialization --
DROP DATABASE IF EXISTS mock_db;
CREATE DATABASE mock_db;
\c mock_db;
----------------------------------------------------------------------
-- Table set-up --
-- Create users first so other tables can match ids;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(20) NOT NULL
);

-- Cats have a one=to-many relationship to users --

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users ON DELETE SET NULL,
  -- users(id) is default, but we could use any valid column from users;
  name VARCHAR(20) NOT NULL UNIQUE,
  description TEXT,
  subscribers INTEGER CHECK (subscribers > 0) DEFAULT 1,
  is_private BOOLEAN NOT NULL DEFAULT false
  );

-- Comments have a one-to-many relationship with users AND cats --

CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  --Comments can still be useful to a cat after without user data;
  -- So we set user to null in this situation:
  user_id INTEGER REFERENCES users ON DELETE SET NULL,
  -------------------------------------------------------
  -- comments are not useful if the category has been deleted;
  -- So we delete comments in this situation:  
  cat_id INTEGER REFERENCES categories ON DELETE CASCADE,
   
  -------------------------------------------------------
  content TEXT NOT NULL
);
----------------------------------------------------------------------
-- Create base data --
----------------------------------------------------------------------
INSERT INTO users 
  (username, password) 
 VALUES
  ('admin', 'pw1'),
  ('admin2', 'pw1');

INSERT INTO categories 
  (name, description, subscribers, is_private, user_id)
 VALUES
  ('saboteur','nefarious acts', 12, false, 1),
  ('eSk8', 'a community for electric skateboarders!', 2, false, 2);

INSERT INTO comments (user_id, cat_id, content)
VALUES (2,1,'whaaaa?');
----------------------------------------------------------------------
-- Updating data --
ALTER TABLE users ADD COLUMN permissions TEXT DEFAULT 'moderator';
ALTER TABLE users DROP COLUMN permissions;
ALTER TABLE users ADD COLUMN permissions TEXT DEFAULT 'read-only';
----------------------------------------------------------------------
-- Creating Indexes --
CREATE INDEX cat_name_index ON categories (name);
-- DROP INDEX cat_name_index;