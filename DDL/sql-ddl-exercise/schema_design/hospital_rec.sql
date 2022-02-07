DROP DATABASE IF EXISTS  hospital_records;

CREATE DATABASE hospital_records;

\c hospital_records

CREATE TABLE hospital (
    id SERIAL PRIMARY KEY,
    name text UNIQUE NOT NULL
);

CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name text NOT NULL,
    hospital_id INTEGER REFERENCES hospital ON DELETE CASCADE
);

CREATE TABLE patients (
    id SERIAL Primary KEY,
    name text  NOT NULL,
    last_visit timestamp NOT NULL
);

CREATE TABLE ailments (
    "id" SERIAL PRIMARY KEY,
    "name" text UNIQUE,
    "description:" varchar(200)  NOT NULL
);

CREATE TABLE visits (
    "id" SERIAL PRIMARY KEY,
    "visit_time" timestamp NOT NULL,
    "doctor_id" INTEGER REFERENCES doctors ON DELETE SET NULL,
    "patient_id" INTEGER REFERENCES patients ON DELETE SET NULL    
);

CREATE TABLE diagnosis (
    "id" SERIAL PRIMARY KEY,
    "name" TEXT   NOT NULL,
    "patient_id" INTEGER REFERENCES patients ON DELETE SET NULL,
    "doctor_id" INTEGER REFERENCES doctors ON DELETE SET NULL,
    "ailment_id" INTEGER REFERENCES ailments ON DELETE SET NULL,
    "visit_id" INTEGER REFERENCES visits ON DELETE SET NULL
);
