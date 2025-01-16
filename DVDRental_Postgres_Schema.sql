-- Schema for DVDrental database in PostgreSQL 14

-- Create table: actor
CREATE TABLE actor (
    actor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: address
CREATE TABLE address (
    address_id SERIAL PRIMARY KEY,
    address VARCHAR(50) NOT NULL,
    address2 VARCHAR(50),
    district VARCHAR(20) NOT NULL,
    city_id INT NOT NULL,
    postal_code VARCHAR(10),
    phone VARCHAR(20) NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: category
CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(25) NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: city
CREATE TABLE city (
    city_id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    country_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: country
CREATE TABLE country (
    country_id SERIAL PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: customer
CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    store_id INT NOT NULL,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    email VARCHAR(50),
    address_id INT NOT NULL,
    activebool BOOLEAN DEFAULT TRUE NOT NULL,
    create_date DATE DEFAULT CURRENT_DATE NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active INT
);

-- Create table: film
CREATE TABLE film (
    film_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    release_year YEAR,
    language_id INT NOT NULL,
    rental_duration INT DEFAULT 3 NOT NULL,
    rental_rate NUMERIC(4,2) DEFAULT 4.99 NOT NULL,
    length INT,
    replacement_cost NUMERIC(5,2) DEFAULT 19.99 NOT NULL,
    rating VARCHAR(5) DEFAULT 'G',
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    special_features TEXT[],
    fulltext TSVECTOR
);

-- Create table: film_actor
CREATE TABLE film_actor (
    actor_id INT NOT NULL,
    film_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (actor_id, film_id)
);

-- Create table: film_category
CREATE TABLE film_category (
    film_id INT NOT NULL,
    category_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (film_id, category_id)
);

-- Create table: inventory
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    film_id INT NOT NULL,
    store_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: language
CREATE TABLE language (
    language_id SERIAL PRIMARY KEY,
    name CHAR(20) NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: payment
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    staff_id INT NOT NULL,
    rental_id INT NOT NULL,
    amount NUMERIC(5,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: rental
CREATE TABLE rental (
    rental_id SERIAL PRIMARY KEY,
    rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    inventory_id INT NOT NULL,
    customer_id INT NOT NULL,
    return_date TIMESTAMP,
    staff_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create table: staff
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    address_id INT NOT NULL,
    email VARCHAR(50),
    store_id INT NOT NULL,
    active BOOLEAN DEFAULT TRUE NOT NULL,
    username VARCHAR(16) NOT NULL,
    password VARCHAR(40),
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    picture BYTEA
);

-- Create table: store
CREATE TABLE store (
    store_id SERIAL PRIMARY KEY,
    manager_staff_id INT NOT NULL,
    address_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Procedure to insert n random rows into the actor table
CREATE OR REPLACE PROCEDURE SampleInsertActor(n INT)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    random_first_name VARCHAR(45);
    random_last_name VARCHAR(45);
BEGIN
    FOR i IN 1..n LOOP
        -- Generate random names
        random_first_name := chr(trunc(65 + random() * 26)::INT) || chr(trunc(65 + random() * 26)::INT);
        random_last_name := chr(trunc(65 + random() * 26)::INT) || chr(trunc(65 + random() * 26)::INT);

        -- Insert data
        INSERT INTO actor (first_name, last_name, last_update)
        VALUES (random_first_name, random_last_name, CURRENT_TIMESTAMP);
    END LOOP;
END;
$$;

-- Example to insert 1000 random records
CALL SampleInsertActor(1000);
