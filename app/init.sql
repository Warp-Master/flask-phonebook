CREATE TABLE IF NOT EXISTS Firstnames
(
    id        SERIAL PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL UNIQUE,
    CHECK(firstname <> '')
);

CREATE TABLE IF NOT EXISTS Lastnames
(
    id       SERIAL PRIMARY KEY,
    lastname VARCHAR(50) NOT NULL UNIQUE,
    CHECK(lastname <> '')
);

CREATE TABLE IF NOT EXISTS Surnames
(
    id      SERIAL PRIMARY KEY,
    surname VARCHAR(50) NOT NULL UNIQUE,
    CHECK(surname <> '')
);

CREATE TABLE IF NOT EXISTS Cities
(
    id   SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL UNIQUE,
    CHECK(city <> '')
);

CREATE TABLE IF NOT EXISTS Streets
(
    id SERIAL PRIMARY KEY,
    street VARCHAR(50) NOT NULL UNIQUE,
    CHECK(street <> '')
);

CREATE TABLE IF NOT EXISTS Persons
(
    id       SERIAL PRIMARY KEY,
    fname    INT REFERENCES Firstnames(id) ON DELETE NO ACTION NOT NULL,
    lname    INT REFERENCES Lastnames(id)  ON DELETE NO ACTION NOT NULL,
    sname    INT REFERENCES Surnames(id)   ON DELETE NO ACTION NOT NULL,
    city     INT REFERENCES Cities(id)     ON DELETE NO ACTION NOT NUll,
    street   INT REFERENCES Streets(id)    ON DELETE NO ACTION NOT NULL,
    building VARCHAR(10)                   NOT NULL,
    phone    VARCHAR(30)                   NOT NULL UNIQUE
    CHECK(building <> ''),
    CHECK(phone <> '')
);