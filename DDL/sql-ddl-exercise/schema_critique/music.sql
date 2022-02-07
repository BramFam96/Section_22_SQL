-- from the terminal run:
-- psql < music.sql

DROP DATABASE IF EXISTS music;
CREATE DATABASE music;
\c music

------------------------------------------------------------------------

CREATE TABLE artists (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE albums
(
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  release_date DATE NOT NULL

);

CREATE TABLE producers
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE songs
(
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  duration_in_seconds INTEGER NOT NULL,
  album_id INT REFERENCES albums ON DELETE CASCADE
);

--M:M relationships:
CREATE TABLE performed_by
(
  id SERIAL PRIMARY KEY,
  song_id INT REFERENCES songs ON DELETE CASCADE,
  artist_id INT REFERENCES artists ON DELETE SET NULL
);
CREATE TABLE produced_by 
(
  id SERIAL PRIMARY KEY,
  producer_id INT REFERENCES producers ON DELETE SET NULL,
  album_id INT REFERENCES songs ON DELETE CASCADE
);
-------------------------------------------------------------------------------------------------
INSERT INTO artists 
(name)
VALUES 
('Hanson'),
('Queen');

INSERT INTO albums 
(title, release_date)
VALUES 
('Middle of Nowhere','04-15-1997'), 
('A Night at the Opera', '10-31-1975');

INSERT INTO producers 
(name)
VALUES 
('Dust Brothers'), 
('Stephen Lironi'), 
('Roy Thomas Baker');
 

INSERT INTO songs 
(title, duration_in_seconds, album_id)
VALUES 
('MMMBop', 238, 1), 
('Bohemian Rhapsody',355,2);

INSERT INTO performed_by 
(song_id, artist_id)
VALUES 
(1,1),
(2,2);

INSERT INTO produced_by 
(producer_id, album_id)
VALUES 
(1,1),
(2,1),
(3,2);

-- INSERT INTO songs
--   (title, duration_in_seconds, release_date, artists, album, producers)
-- VALUES
--   ('MMMBop', 238, '04-15-1997', '{"Hanson"}', 'Middle of Nowhere', '{"Dust Brothers", "Stephen Lironi"}'),
--   ('Bohemian Rhapsody', 355, '10-31-1975', '{"Queen"}', 'A Night at the Opera', '{"Roy Thomas Baker"}'),
--   ('One Sweet Day', 282, '11-14-1995', '{"Mariah Cary", "Boyz II Men"}', 'Daydream', '{"Walter Afanasieff"}'),
--   ('Shallow', 216, '09-27-2018', '{"Lady Gaga", "Bradley Cooper"}', 'A Star Is Born', '{"Benjamin Rice"}'),
--   ('How You Remind Me', 223, '08-21-2001', '{"Nickelback"}', 'Silver Side Up', '{"Rick Parashar"}'),
--   ('New York State of Mind', 276, '10-20-2009', '{"Jay Z", "Alicia Keys"}', 'The Blueprint 3', '{"Al Shux"}'),
--   ('Dark Horse', 215, '12-17-2013', '{"Katy Perry", "Juicy J"}', 'Prism', '{"Max Martin", "Cirkut"}'),
--   ('Moves Like Jagger', 201, '06-21-2011', '{"Maroon 5", "Christina Aguilera"}', 'Hands All Over', '{"Shellback", "Benny Blanco"}'),
--   ('Complicated', 244, '05-14-2002', '{"Avril Lavigne"}', 'Let Go', '{"The Matrix"}'),
--   ('Say My Name', 240, '11-07-1999', '{"Destiny''s Child"}', 'The Writing''s on the Wall', '{"Darkchild"}');
