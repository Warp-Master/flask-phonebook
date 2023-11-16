CREATE TABLE IF NOT EXISTS Firstnames
(
    id        SERIAL PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_firstname ON Firstnames(firstname);

CREATE TABLE IF NOT EXISTS Lastnames
(
    id       SERIAL PRIMARY KEY,
    lastname VARCHAR(50) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_lastname ON Lastnames(lastname);

CREATE TABLE IF NOT EXISTS Surnames
(
    id      SERIAL PRIMARY KEY,
    surname VARCHAR(50) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_surname ON Surnames(surname);

CREATE TABLE IF NOT EXISTS Persons
(
    id    SERIAL PRIMARY KEY,
    fname INT REFERENCES Firstnames(id) NOT NULL,
    lname INT REFERENCES Lastnames(id)  NOT NULL,
    sname INT REFERENCES Surnames(id)   NOT NULL
);

CREATE TABLE IF NOT EXISTS Cities
(
    id   SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_city ON Cities(city);

CREATE TABLE IF NOT EXISTS Addresses
(
    id       INT PRIMARY KEY REFERENCES Persons(id),
    building VARCHAR(10) NOT NULL,
    street   VARCHAR(50) NOT NULL,
    city     INT REFERENCES Cities(id)
);

CREATE TABLE IF NOT EXISTS Phones
(
    id    INT REFERENCES Persons(id),
    phone VARCHAR(15) PRIMARY KEY NOT NULL
)