-- Schema for DVDrental database optimized for Amazon Redshift

drop table FILM ;
drop table FILM_ACTOR ;
drop table FILM_CATEGORY ;
drop table INVENTORY ;
drop table LANGUAGE ;
drop table PAYMENT ;
drop table RENTAL ;
drop table STAFF ;
drop table STORE ;
drop table ACTOR ;
drop table ADDRESS ;
drop table CATEGORY ;
drop table CITY ;
drop table COUNTRY ;
drop table CUSTOMER ;

-- Customer table
CREATE TABLE customer (
    customer_id INT ,
    store_id SMALLINT,
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    email VARCHAR(50),
    address_id INT,
    activebool BOOLEAN,
    create_date DATE,
    last_update TIMESTAMP,
    PRIMARY KEY (customer_id)
)
DISTSTYLE KEY
DISTKEY (store_id)
SORTKEY (last_name, first_name);

-- Store table
CREATE TABLE store (
    store_id SMALLINT ,
    manager_staff_id SMALLINT,
    address_id INT,
    last_update TIMESTAMP,
    PRIMARY KEY (store_id)
)
DISTSTYLE ALL
SORTKEY (store_id);

-- Staff table
CREATE TABLE staff (
    staff_id SMALLINT ,
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    address_id INT,
    email VARCHAR(50),
    store_id SMALLINT,
    active BOOLEAN,
    username VARCHAR(200),
    password VARCHAR(32),
    last_update TIMESTAMP,
    PRIMARY KEY (staff_id)
)
DISTSTYLE EVEN
SORTKEY (last_name, first_name);

-- Address table
CREATE TABLE address (
    address_id INT ,
    address VARCHAR(50),
    address2 VARCHAR(50),
    district VARCHAR(20),
    city_id INT,
    postal_code VARCHAR(10),
    phone VARCHAR(20),
    last_update TIMESTAMP,
    PRIMARY KEY (address_id)
)
DISTSTYLE EVEN
SORTKEY (city_id, district);

-- City table
CREATE TABLE city (
    city_id INT ,
    city VARCHAR(50),
    country_id INT,
    last_update TIMESTAMP,
    PRIMARY KEY (city_id)
)
DISTSTYLE EVEN
SORTKEY (country_id);

-- Country table
CREATE TABLE country (
    country_id INT ,
    country VARCHAR(300),
    last_update TIMESTAMP,
    PRIMARY KEY (country_id)
)
DISTSTYLE ALL
SORTKEY (country);

-- Film table
CREATE TABLE film (
    film_id INT ,
    title VARCHAR(255),
    description VARCHAR(1000),
    release_year INT,
    language_id INT,
    rental_duration SMALLINT,
    rental_rate DECIMAL(4,2),
    length SMALLINT,
    replacement_cost DECIMAL(5,2),
    rating CHAR(5),
    last_update TIMESTAMP,
    PRIMARY KEY (film_id)
)
DISTSTYLE KEY
DISTKEY (language_id)
SORTKEY (title);

-- Language table
CREATE TABLE language (
    language_id INT,
    name CHAR(20),
    last_update TIMESTAMP,
    PRIMARY KEY (language_id)
)
DISTSTYLE ALL
SORTKEY (name);

-- Inventory table
CREATE TABLE inventory (
    inventory_id INT,
    film_id INT,
    store_id SMALLINT,
    last_update TIMESTAMP,
    PRIMARY KEY (inventory_id)
)
DISTSTYLE KEY
DISTKEY (store_id)
SORTKEY (film_id);

-- Rental table
CREATE TABLE rental (
    rental_id INT,
    rental_date TIMESTAMP,
    inventory_id INT,
    customer_id INT,
    return_date TIMESTAMP,
    status varchar(50),
    staff_id SMALLINT,
    last_update TIMESTAMP,
    PRIMARY KEY (rental_id)
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (rental_date);

-- Payment table
CREATE TABLE payment (
    payment_id INT,
    customer_id INT,
    staff_id SMALLINT,
    rental_id INT,
    amount DECIMAL(5,2),
    payment_date TIMESTAMP,
    PRIMARY KEY (payment_id)
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (payment_date);

-- Film_actor table
CREATE TABLE film_actor (
    actor_id INT,
    film_id INT,
    last_update TIMESTAMP,
    PRIMARY KEY (actor_id, film_id)
)
DISTSTYLE EVEN
SORTKEY (film_id);

-- Film_category table
CREATE TABLE film_category (
    film_id INT,
    category_id INT,
    last_update TIMESTAMP,
    PRIMARY KEY (film_id, category_id)
)
DISTSTYLE EVEN
SORTKEY (category_id);

-- Actor table
CREATE TABLE actor (
    actor_id INT,
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    last_update TIMESTAMP,
    PRIMARY KEY (actor_id)
)
DISTSTYLE EVEN
SORTKEY (last_name, first_name);

-- Category table
CREATE TABLE category (
    category_id INT,
    name VARCHAR(25),
    last_update TIMESTAMP,
    PRIMARY KEY (category_id)
)
DISTSTYLE ALL
SORTKEY (name);
