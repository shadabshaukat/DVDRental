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

-- Create table: actor
CREATE TABLE actor (
    actor_id INT  PRIMARY KEY,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE KEY
DISTKEY (actor_id)
SORTKEY (actor_id);

-- Create table: address
CREATE TABLE address (
    address_id INT  PRIMARY KEY,
    address VARCHAR(50) NOT NULL,
    address2 VARCHAR(50),
    district VARCHAR(20) NOT NULL,
    city_id INT NOT NULL,
    postal_code VARCHAR(10),
    phone VARCHAR(20) NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE KEY
DISTKEY (address_id)
SORTKEY (address_id);

-- Create table: category
CREATE TABLE category (
    category_id INT  PRIMARY KEY,
    name VARCHAR(25) NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE ALL
SORTKEY (category_id);

-- Create table: city
CREATE TABLE city (
    city_id INT  PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    country_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE KEY
DISTKEY (city_id)
SORTKEY (city_id);

-- Create table: country
CREATE TABLE country (
    country_id INT  PRIMARY KEY,
    country VARCHAR(200) NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE ALL
SORTKEY (country_id);

-- Create table: customer
CREATE TABLE customer (
    customer_id INT  PRIMARY KEY,
    store_id INT NOT NULL,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    email VARCHAR(50),
    address_id INT NOT NULL,
    active INT DEFAULT 1 NOT NULL,
    create_date DATE,
    last_update TIMESTAMP,
    activebool INT
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (customer_id);

-- Create table: film
CREATE TABLE film (
    film_id INT  PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(65535),
    release_year INT,
    language_id INT NOT NULL,
    rental_duration INT NOT NULL DEFAULT 3,
    rental_rate DECIMAL(4,2) DEFAULT 4.99 NOT NULL,
    length INT,
    replacement_cost DECIMAL(5,2) DEFAULT 19.99 NOT NULL,
    rating VARCHAR(5) DEFAULT 'G',
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL,
    special_features VARCHAR(500),
    fulltext VARCHAR(65535)
)
DISTSTYLE KEY
DISTKEY (film_id)
SORTKEY (film_id);

-- Create table: film_actor
CREATE TABLE film_actor (
    actor_id INT NOT NULL,
    film_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL,
    PRIMARY KEY (actor_id, film_id)
)
DISTSTYLE KEY
DISTKEY (film_id)
SORTKEY (film_id, actor_id);

-- Create table: film_category
CREATE TABLE film_category (
    film_id INT NOT NULL,
    category_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL,
    PRIMARY KEY (film_id, category_id)
)
DISTSTYLE KEY
DISTKEY (film_id)
SORTKEY (film_id, category_id);

-- Create table: inventory
CREATE TABLE inventory (
    inventory_id INT  PRIMARY KEY,
    film_id INT NOT NULL,
    store_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE KEY
DISTKEY (inventory_id)
SORTKEY (inventory_id);

-- Create table: language
CREATE TABLE language (
    language_id INT  PRIMARY KEY,
    name CHAR(20) NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE ALL
SORTKEY (language_id);

-- Create table: payment
CREATE TABLE payment (
    payment_id INT  PRIMARY KEY,
    customer_id INT NOT NULL,
    staff_id INT NOT NULL,
    rental_id INT NOT NULL,
    amount DECIMAL(5,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (payment_date);

-- Create table: rental
CREATE TABLE rental (
    rental_id INT  PRIMARY KEY,
    rental_date TIMESTAMP DEFAULT GETDATE() NOT NULL,
    inventory_id INT NOT NULL,
    customer_id INT NOT NULL,
    return_date TIMESTAMP,
    status VARCHAR(50),
    staff_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (rental_date);

-- Create table: staff
CREATE TABLE staff (
    staff_id INT  PRIMARY KEY,
    first_name VARCHAR(45) NOT NULL,
    last_name VARCHAR(45) NOT NULL,
    address_id INT NOT NULL,
    email VARCHAR(50),
    store_id INT NOT NULL,
    active SMALLINT DEFAULT 1 NOT NULL,
    username VARCHAR(200) NOT NULL,
    password VARCHAR(40),
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL,
    picture VARCHAR(65535)
)
DISTSTYLE ALL
SORTKEY (staff_id);

-- Create table: store
CREATE TABLE store (
    store_id INT  PRIMARY KEY,
    manager_staff_id INT NOT NULL,
    address_id INT NOT NULL,
    last_update TIMESTAMP DEFAULT GETDATE() NOT NULL
)
DISTSTYLE ALL
SORTKEY (store_id);
