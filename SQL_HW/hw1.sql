CREATE TABLE films (title VARCHAR PRIMARY KEY,id serial, country VARCHAR, box_office serial, release_year serial);
INSERT INTO films VALUES ('The Terminator', 507, 'USA', 78371200, 1984);
INSERT INTO films VALUES ('Terminator 2: Judgment Day', 444, 'USA', 519843345, 1991);
INSERT INTO films VALUES ('Terminator 3: Rise of the Machines', 319, 'USA', 433371112, 2003);
INSERT INTO films VALUES ('Terminator Salvation', 160932, 'USA', 371353001, 2009);
INSERT INTO films VALUES ('Terminator Genisys', 436225, 'USA', 440603537, 2015);
SELECT * FROM films;

CREATE TABLE persons (id serial PRIMARY KEY, fio VARCHAR);
INSERT INTO persons VALUES (6264, 'Arnold Swarzenegger');
INSERT INTO persons VALUES (28012, 'Linda Hamilton');
INSERT INTO persons VALUES (13297, 'Nick Stahl');
INSERT INTO persons VALUES (21495, 'Christian Bale');
INSERT INTO persons VALUES (1830611, 'Emilia Clarke');
SELECT * FROM persons;

CREATE TABLE persons2content (person_id serial, film_id serial PRIMARY KEY, person_type VARCHAR);
INSERT INTO persons2content VALUES (6264, 507, 'actor');
INSERT INTO persons2content VALUES (28012, 444, 'actor');
INSERT INTO persons2content VALUES (13297, 319, 'actor');
INSERT INTO persons2content VALUES (21495, 160932, 'actor');
INSERT INTO persons2content VALUES (1830611, 436225, 'actor');
SELECT * FROM persons2content;

