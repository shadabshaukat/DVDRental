# DVDRental Schema
Cross-Database Clone of DVDRental Postgres Schema Across Heterogenous Databases

```plaintext
+----------------+       +----------------+       +----------------+       +----------------+        +-----------------+
|   country      |       |    city        |       |  address       |       |     customer    |       |     rental      |
+----------------+       +----------------+       +----------------+       +----------------+        +-----------------+
| country_id PK  |<------| city_id PK     |<------| address_id PK  |<------| customer_id PK  |<------| rental_id PK    |
| country        |       | city           |       | address        |       | store_id        |       | rental_date     |
| last_update    |       | country_id FK  |       | address2       |       | first_name      |       | inventory_id FK |
+----------------+       | last_update    |       | district       |       | last_name       |       | customer_id FK  |
                        +----------------+       | postal_code    |       | email           |        | return_date     |
                                                 | phone          |       | address_id FK   |        | status          |
                                                 | last_update    |       | active          |        | staff_id FK     |
                                                 +----------------+       +----------------+         | last_update     |
                                                                                                     +-----------------+

+----------------+       +----------------+       +----------------+       +----------------+       +----------------+
|  inventory     |       |     film       |       |    film_actor  |       |   film_category |       |    category     |
+----------------+       +----------------+       +----------------+       +----------------+       +----------------+
| inventory_id PK|<------| film_id PK     |<------| actor_id FK    |       | film_id FK      |       | category_id PK  |
| film_id FK     |       | title          |       | film_id FK     |       | category_id FK  |       | name            |
| store_id       |       | description    |       | last_update    |       | last_update     |       | last_update     |
| last_update    |       | release_year   |       +----------------+       +----------------+       +----------------+
+----------------+       | language_id FK |
                        | rental_duration|
                        | rental_rate    |
                        | length         |
                        | replacement_cost|
                        | rating         |
                        | last_update    |
                        | special_features|
                        +----------------+

+----------------+       +----------------+       +----------------+       +----------------+       +----------------+
|  staff         |       |     store      |       |    language    |       |      payment    |       |    actor        |
+----------------+       +----------------+       +----------------+       +----------------+       +----------------+
| staff_id PK    |<------| store_id PK    |       | language_id PK |       | payment_id PK   |       | actor_id PK     |
| first_name     |       | manager_staff_id|       | name           |       | customer_id FK  |       | first_name      |
| last_name      |       | address_id FK  |       | last_update    |       | staff_id FK     |       | last_name       |
| address_id FK  |       | last_update    |       +----------------+       | rental_id FK    |       | last_update     |
| email          |       +----------------+                          | amount         |       +----------------+
| store_id FK    |                                                     | payment_date   |
| username       |                                                     +----------------+
| password       |
| last_update    |
+----------------+
```
# Explanation of Schema and Relationships

The DVDRental schema is designed to model a video rental business. 

   ## Country, City, Address:
        country contains the list of countries.
        city belongs to a country (country_id is a foreign key).
        address specifies locations linked to cities (city_id is a foreign key).

   ##    Customer:
        Each customer is associated with an address (address_id is a foreign key) and a store (store_id).

   ##     Store and Staff:
        A store is managed by a staff member (manager_staff_id is a foreign key).
        staff members are linked to an address and store.

   ##    Film, Inventory, Rental, and Payment:
        film contains details about movies, including associated languages.
        inventory links films to stores for tracking availability.
        rental logs customer rentals, connecting inventory, customers, and staff.
        payment records the financial transactions related to rentals.

   ##    Actors and Categories:
        actor lists actors in the films.
        film_actor creates a many-to-many relationship between films and actors.
        category groups films into genres, with film_category managing the many-to-many relationship.

# DVDRental Data Generation with Python

## Install Python
```plaintext
    sudo yum install -y \
        gcc \
        make \
        zlib-devel \
        libffi-devel \
        openssl-devel \
        bzip2-devel \
        xz-devel \
        ncurses-devel \
        sqlite-devel \
        readline-devel
        
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz

tar -xJf Python-3.9.0.tar.xz
    
cd Python-3.9.0
./configure --enable-optimizations

make -j $(nproc)

sudo make altinstall

python3.9 --version

which python3.9

/usr/local/bin/python3.9

/usr/local/bin/python3.9 -m site

sys.path = [
    '/home/opc/Python-3.9.0',
    '/usr/local/lib/python39.zip',
    '/usr/local/lib/python3.9',
    '/usr/local/lib/python3.9/lib-dynload',
    '/usr/local/lib/python3.9/site-packages',
]
USER_BASE: '/home/opc/.local' (exists)
USER_SITE: '/home/opc/.local/lib/python3.9/site-packages' (doesn't exist)
ENABLE_USER_SITE: True

/usr/local/bin/python3.9 -m ensurepip --upgrade

sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3
sudo ln -s /usr/local/bin/pip3.9 /usr/bin/pip3
```

## Clone Repo


