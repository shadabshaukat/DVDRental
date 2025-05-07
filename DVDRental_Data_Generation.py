import time
import random
import string
from datetime import datetime, timedelta
from faker import Faker
import mysql.connector
import cx_Oracle
import psycopg2
from threading import Thread
from queue import Queue

# Initialize Faker
fake = Faker()

# Database connection configurations
DB_CONFIG = {
    'mysql': {
        'host': '10.180.2.88',
        'user': 'ggadmin',
        'password': 'RAbbithole1234##',
        'database': 'dvdrental'
    },
    'oracle': {
        'user': 'mpos',
        'password': 'abcdABCD1234##',
        'dsn': '10.180.2.158:1521/T1DB04'
    },
    'postgresql': {
        'host': '10.180.2.205',
        'user': 'ggadmin',
        'password': 'RAbbithole1234##',
        'database': 'dvdrental'
    }
}

# Global counters to ensure unique IDs across all databases
GLOBAL_ID_COUNTERS = {
    'actor': 1,
    'address': 1,
    'category': 1,
    'city': 1,
    'country': 1,
    'customer': 1,
    'film': 1,
    'inventory': 1,
    'language': 1,
    'payment': 1,
    'rental': 1,
    'staff': 1,
    'store': 1
}

# Thread-safe queue for database operations
db_queue = Queue()

def get_next_global_id(table_name):
    """Get the next global ID for a table and increment the counter"""
    global GLOBAL_ID_COUNTERS
    current_id = GLOBAL_ID_COUNTERS[table_name]
    GLOBAL_ID_COUNTERS[table_name] += 1
    return current_id

def generate_phone():
    """Generate a realistic phone number"""
    return f"{fake.country_calling_code()}{fake.msisdn()[3:]}"

def generate_postal_code():
    """Generate a realistic postal code"""
    if random.choice([True, False]):
        return fake.postcode()
    return f"{random.randint(10000, 99999)}"

def generate_special_features():
    """Generate special features for films"""
    features = ['Trailers', 'Commentaries', 'Deleted Scenes', 'Behind the Scenes']
    selected = random.sample(features, random.randint(1, len(features)))
    return selected

def generate_rating():
    """Generate a film rating"""
    return random.choice(['G', 'PG', 'PG-13', 'R', 'NC-17'])

def generate_status():
    """Generate rental status"""
    return random.choice(['rented', 'returned', 'overdue', 'lost'])

def generate_film_description():
    """Generate a realistic film description"""
    themes = [
        "A heartwarming tale of", "An epic journey through", "A thrilling adventure about",
        "A dramatic story of", "A comedic look at", "A mysterious account of",
        "A romantic story about", "A sci-fi exploration of", "A horror flick featuring"
    ]
    subjects = [
        "a young hero", "an unlikely friendship", "a dangerous mission",
        "a family secret", "a lost treasure", "a forbidden love",
        "a futuristic world", "a haunted house", "a political conspiracy"
    ]
    return f"{random.choice(themes)} {random.choice(subjects)}."

def generate_country_data():
    """Generate data for country table"""
    country_id = get_next_global_id('country')
    return {
        'country_id': country_id,
        'country': fake.country(),
        'last_update': datetime.now()
    }

def generate_city_data(country_id):
    """Generate data for city table"""
    city_id = get_next_global_id('city')
    return {
        'city_id': city_id,
        'city': fake.city(),
        'country_id': country_id,
        'last_update': datetime.now()
    }

def generate_address_data(city_id):
    """Generate data for address table"""
    address_id = get_next_global_id('address')
    return {
        'address_id': address_id,
        'address': fake.street_address(),
        'address2': fake.secondary_address() if random.random() > 0.7 else None,
        'district': fake.state(),
        'city_id': city_id,
        'postal_code': generate_postal_code(),
        'phone': generate_phone(),
        'last_update': datetime.now()
    }

def generate_actor_data():
    """Generate data for actor table"""
    actor_id = get_next_global_id('actor')
    return {
        'actor_id': actor_id,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'last_update': datetime.now()
    }

def generate_category_data():
    """Generate data for category table"""
    category_id = get_next_global_id('category')
    categories = [
        'Action', 'Animation', 'Children', 'Classics', 'Comedy',
        'Documentary', 'Drama', 'Family', 'Foreign', 'Games',
        'Horror', 'Music', 'New', 'Sci-Fi', 'Sports', 'Travel'
    ]
    return {
        'category_id': category_id,
        'name': random.choice(categories),
        'last_update': datetime.now()
    }

def generate_language_data():
    """Generate data for language table"""
    language_id = get_next_global_id('language')
    languages = [
        'English', 'French', 'German', 'Spanish', 'Italian',
        'Japanese', 'Mandarin', 'Russian', 'Arabic', 'Hindi'
    ]
    return {
        'language_id': language_id,
        'name': random.choice(languages),
        'last_update': datetime.now()
    }

def generate_film_data(language_id):
    """Generate data for film table"""
    film_id = get_next_global_id('film')
    release_year = random.randint(1950, datetime.now().year)
    return {
        'film_id': film_id,
        'title': fake.catch_phrase().title(),
        'description': generate_film_description(),
        'release_year': release_year,
        'language_id': language_id,
        'rental_duration': random.randint(3, 7),
        'rental_rate': round(random.uniform(0.99, 5.99), 2),
        'length': random.randint(60, 180),
        'replacement_cost': round(random.uniform(9.99, 29.99), 2),
        'rating': generate_rating(),
        'last_update': datetime.now(),
        'special_features': generate_special_features(),
        'fulltext': fake.text()
    }

def generate_store_data(address_id, staff_id):
    """Generate data for store table"""
    store_id = get_next_global_id('store')
    return {
        'store_id': store_id,
        'manager_staff_id': staff_id,
        'address_id': address_id,
        'last_update': datetime.now()
    }

def generate_staff_data(address_id, store_id):
    """Generate data for staff table"""
    staff_id = get_next_global_id('staff')
    return {
        'staff_id': staff_id,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'address_id': address_id,
        'email': fake.email(),
        'store_id': store_id,
        'active': 1,
        'username': fake.user_name(),
        'password': fake.password(),
        'last_update': datetime.now(),
        'picture': None
    }

def generate_customer_data(store_id, address_id):
    """Generate data for customer table"""
    customer_id = get_next_global_id('customer')
    return {
        'customer_id': customer_id,
        'store_id': store_id,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'address_id': address_id,
        'active': random.randint(0, 1),
        'create_date': fake.date_between(start_date='-5y', end_date='today'),
        'last_update': datetime.now(),
        'activebool': random.choice([True, False])
    }

def generate_inventory_data(film_id, store_id):
    """Generate data for inventory table"""
    inventory_id = get_next_global_id('inventory')
    return {
        'inventory_id': inventory_id,
        'film_id': film_id,
        'store_id': store_id,
        'last_update': datetime.now()
    }

def generate_rental_data(inventory_id, customer_id, staff_id):
    """Generate data for rental table"""
    rental_id = get_next_global_id('rental')
    rental_date = fake.date_time_between(start_date='-1y', end_date='now')
    return_date = rental_date + timedelta(days=random.randint(1, 14)) if random.random() > 0.2 else None
    return {
        'rental_id': rental_id,
        'rental_date': rental_date,
        'inventory_id': inventory_id,
        'customer_id': customer_id,
        'return_date': return_date,
        'status': generate_status(),
        'staff_id': staff_id,
        'last_update': datetime.now()
    }

def generate_payment_data(customer_id, staff_id, rental_id):
    """Generate data for payment table"""
    payment_id = get_next_global_id('payment')
    return {
        'payment_id': payment_id,
        'customer_id': customer_id,
        'staff_id': staff_id,
        'rental_id': rental_id,
        'amount': round(random.uniform(1.99, 19.99), 2),
        'payment_date': datetime.now()
    }

def generate_film_actor_data(actor_id, film_id):
    """Generate data for film_actor table"""
    return {
        'actor_id': actor_id,
        'film_id': film_id,
        'last_update': datetime.now()
    }

def generate_film_category_data(film_id, category_id):
    """Generate data for film_category table"""
    return {
        'film_id': film_id,
        'category_id': category_id,
        'last_update': datetime.now()
    }

def execute_mysql_query(query, params=None):
    """Execute a query on MySQL database"""
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG['mysql'])
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(f"MySQL Error: {e}")
    finally:
        if conn:
            conn.close()

def execute_oracle_query(query, params=None):
    """Execute a query on Oracle database"""
    conn = None
    try:
        conn = cx_Oracle.connect(**DB_CONFIG['oracle'])
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(f"Oracle Error: {e}")
    finally:
        if conn:
            conn.close()

def execute_postgresql_query(query, params=None):
    """Execute a query on PostgreSQL database"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG['postgresql'])
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(f"PostgreSQL Error: {e}")
    finally:
        if conn:
            conn.close()

def generate_and_insert_data():
    """Generate and insert data into all databases"""
    # Generate base data
    country_data = generate_country_data()
    city_data = generate_city_data(country_data['country_id'])
    address_data = generate_address_data(city_data['city_id'])
    actor_data = generate_actor_data()
    category_data = generate_category_data()
    language_data = generate_language_data()
    film_data = generate_film_data(language_data['language_id'])
    
    # Generate staff before store as store needs staff_id
    staff_data = generate_staff_data(address_data['address_id'], None)
    
    # Now generate store with the staff_id
    store_data = generate_store_data(address_data['address_id'], staff_data['staff_id'])
    
    # Update staff with store_id
    staff_data['store_id'] = store_data['store_id']
    
    customer_data = generate_customer_data(store_data['store_id'], address_data['address_id'])
    inventory_data = generate_inventory_data(film_data['film_id'], store_data['store_id'])
    
    # Generate rental after inventory exists
    rental_data = generate_rental_data(
        inventory_data['inventory_id'],
        customer_data['customer_id'],
        staff_data['staff_id']
    )
    
    # Generate payment after rental exists
    payment_data = generate_payment_data(
        customer_data['customer_id'],
        staff_data['staff_id'],
        rental_data['rental_id']
    )
    
    film_actor_data = generate_film_actor_data(actor_data['actor_id'], film_data['film_id'])
    film_category_data = generate_film_category_data(film_data['film_id'], category_data['category_id'])
    
    # MySQL Queries
    mysql_queries = [
        ("INSERT INTO country (country_id, country, last_update) VALUES (%s, %s, %s)", 
         (country_data['country_id'], country_data['country'], country_data['last_update'])),
        ("INSERT INTO city (city_id, city, country_id, last_update) VALUES (%s, %s, %s, %s)", 
         (city_data['city_id'], city_data['city'], city_data['country_id'], city_data['last_update'])),
        ("INSERT INTO address (address_id, address, address2, district, city_id, postal_code, phone, last_update) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
         (address_data['address_id'], address_data['address'], address_data['address2'], address_data['district'], 
          address_data['city_id'], address_data['postal_code'], address_data['phone'], address_data['last_update'])),
        ("INSERT INTO actor (actor_id, first_name, last_name, last_update) VALUES (%s, %s, %s, %s)", 
         (actor_data['actor_id'], actor_data['first_name'], actor_data['last_name'], actor_data['last_update'])),
        ("INSERT INTO category (category_id, name, last_update) VALUES (%s, %s, %s)", 
         (category_data['category_id'], category_data['name'], category_data['last_update'])),
        ("INSERT INTO language (language_id, name, last_update) VALUES (%s, %s, %s)", 
         (language_data['language_id'], language_data['name'], language_data['last_update'])),
        ("INSERT INTO film (film_id, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, last_update, special_features, `fulltext`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
         (film_data['film_id'], film_data['title'], film_data['description'], film_data['release_year'], 
          film_data['language_id'], film_data['rental_duration'], float(film_data['rental_rate']), 
          film_data['length'], float(film_data['replacement_cost']), film_data['rating'], 
          film_data['last_update'], str(film_data['special_features']), film_data['fulltext'])),
        ("INSERT INTO staff (staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update, picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
         (staff_data['staff_id'], staff_data['first_name'], staff_data['last_name'], staff_data['address_id'], 
          staff_data['email'], staff_data['store_id'], staff_data['active'], staff_data['username'], 
          staff_data['password'], staff_data['last_update'], staff_data['picture'])),
        ("INSERT INTO store (store_id, manager_staff_id, address_id, last_update) VALUES (%s, %s, %s, %s)", 
         (store_data['store_id'], store_data['manager_staff_id'], store_data['address_id'], store_data['last_update'])),
        ("INSERT INTO customer (customer_id, store_id, first_name, last_name, email, address_id, active, create_date, last_update, activebool) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
         (customer_data['customer_id'], customer_data['store_id'], customer_data['first_name'], 
          customer_data['last_name'], customer_data['email'], customer_data['address_id'], 
          customer_data['active'], customer_data['create_date'], customer_data['last_update'], 
          int(customer_data['activebool']) if customer_data['activebool'] is not None else None)),
        ("INSERT INTO inventory (inventory_id, film_id, store_id, last_update) VALUES (%s, %s, %s, %s)", 
         (inventory_data['inventory_id'], inventory_data['film_id'], inventory_data['store_id'], inventory_data['last_update'])),
        ("INSERT INTO rental (rental_id, rental_date, inventory_id, customer_id, return_date, status, staff_id, last_update) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
         (rental_data['rental_id'], rental_data['rental_date'], rental_data['inventory_id'], 
          rental_data['customer_id'], rental_data['return_date'], rental_data['status'], 
          rental_data['staff_id'], rental_data['last_update'])),
        ("INSERT INTO payment (payment_id, customer_id, staff_id, rental_id, amount, payment_date) VALUES (%s, %s, %s, %s, %s, %s)", 
         (payment_data['payment_id'], payment_data['customer_id'], payment_data['staff_id'], 
          payment_data['rental_id'], float(payment_data['amount']), payment_data['payment_date'])),
        ("INSERT INTO film_actor (actor_id, film_id, last_update) VALUES (%s, %s, %s)", 
         (film_actor_data['actor_id'], film_actor_data['film_id'], film_actor_data['last_update'])),
        ("INSERT INTO film_category (film_id, category_id, last_update) VALUES (%s, %s, %s)", 
         (film_category_data['film_id'], film_category_data['category_id'], film_category_data['last_update']))
    ]
    
    # Oracle Queries (similar structure but with :param syntax)
    oracle_queries = [
        ("INSERT INTO country (country_id, country, last_update) VALUES (:1, :2, :3)", 
         (country_data['country_id'], country_data['country'], country_data['last_update'])),
        ("INSERT INTO city (city_id, city, country_id, last_update) VALUES (:1, :2, :3, :4)", 
         (city_data['city_id'], city_data['city'], city_data['country_id'], city_data['last_update'])),
        ("INSERT INTO address (address_id, address, address2, district, city_id, postal_code, phone, last_update) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", 
         (address_data['address_id'], address_data['address'], address_data['address2'], address_data['district'], 
          address_data['city_id'], address_data['postal_code'], address_data['phone'], address_data['last_update'])),
        ("INSERT INTO actor (actor_id, first_name, last_name, last_update) VALUES (:1, :2, :3, :4)", 
         (actor_data['actor_id'], actor_data['first_name'], actor_data['last_name'], actor_data['last_update'])),
        ("INSERT INTO category (category_id, name, last_update) VALUES (:1, :2, :3)", 
         (category_data['category_id'], category_data['name'], category_data['last_update'])),
        ("INSERT INTO language (language_id, name, last_update) VALUES (:1, :2, :3)", 
         (language_data['language_id'], language_data['name'], language_data['last_update'])),
        ("INSERT INTO film (film_id, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, last_update, special_features, fulltext) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)", 
         (film_data['film_id'], film_data['title'], film_data['description'], film_data['release_year'], 
          film_data['language_id'], film_data['rental_duration'], float(film_data['rental_rate']), 
          film_data['length'], float(film_data['replacement_cost']), film_data['rating'], 
          film_data['last_update'], str(film_data['special_features']), film_data['fulltext'])),
        ("INSERT INTO staff (staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update, picture) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)", 
         (staff_data['staff_id'], staff_data['first_name'], staff_data['last_name'], staff_data['address_id'], 
          staff_data['email'], staff_data['store_id'], staff_data['active'], staff_data['username'], 
          staff_data['password'], staff_data['last_update'], staff_data['picture'])),
        ("INSERT INTO store (store_id, manager_staff_id, address_id, last_update) VALUES (:1, :2, :3, :4)", 
         (store_data['store_id'], store_data['manager_staff_id'], store_data['address_id'], store_data['last_update'])),
        ("INSERT INTO customer (customer_id, store_id, first_name, last_name, email, address_id, active, create_date, last_update, activebool) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)", 
         (customer_data['customer_id'], customer_data['store_id'], customer_data['first_name'], 
          customer_data['last_name'], customer_data['email'], customer_data['address_id'], 
          customer_data['active'], customer_data['create_date'], customer_data['last_update'], 
          int(customer_data['activebool']) if customer_data['activebool'] is not None else None)),
        ("INSERT INTO inventory (inventory_id, film_id, store_id, last_update) VALUES (:1, :2, :3, :4)", 
         (inventory_data['inventory_id'], inventory_data['film_id'], inventory_data['store_id'], inventory_data['last_update'])),
        ("INSERT INTO rental (rental_id, rental_date, inventory_id, customer_id, return_date, status, staff_id, last_update) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", 
         (rental_data['rental_id'], rental_data['rental_date'], rental_data['inventory_id'], 
          rental_data['customer_id'], rental_data['return_date'], rental_data['status'], 
          rental_data['staff_id'], rental_data['last_update'])),
        ("INSERT INTO payment (payment_id, customer_id, staff_id, rental_id, amount, payment_date) VALUES (:1, :2, :3, :4, :5, :6)", 
         (payment_data['payment_id'], payment_data['customer_id'], payment_data['staff_id'], 
          payment_data['rental_id'], float(payment_data['amount']), payment_data['payment_date'])),
        ("INSERT INTO film_actor (actor_id, film_id, last_update) VALUES (:1, :2, :3)", 
         (film_actor_data['actor_id'], film_actor_data['film_id'], film_actor_data['last_update'])),
        ("INSERT INTO film_category (film_id, category_id, last_update) VALUES (:1, :2, :3)", 
         (film_category_data['film_id'], film_category_data['category_id'], film_category_data['last_update']))
    ]
    
    # PostgreSQL Queries
    postgresql_queries = [
        ("INSERT INTO country (country_id, country, last_update) VALUES (%s, %s, %s)", 
         (country_data['country_id'], country_data['country'], country_data['last_update'])),
        ("INSERT INTO city (city_id, city, country_id, last_update) VALUES (%s, %s, %s, %s)", 
         (city_data['city_id'], city_data['city'], city_data['country_id'], city_data['last_update'])),
        ("INSERT INTO address (address_id, address, address2, district, city_id, postal_code, phone, last_update) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
         (address_data['address_id'], address_data['address'], address_data['address2'], address_data['district'], 
          address_data['city_id'], address_data['postal_code'], address_data['phone'], address_data['last_update'])),
        ("INSERT INTO actor (actor_id, first_name, last_name, last_update) VALUES (%s, %s, %s, %s)", 
         (actor_data['actor_id'], actor_data['first_name'], actor_data['last_name'], actor_data['last_update'])),
        ("INSERT INTO category (category_id, name, last_update) VALUES (%s, %s, %s)", 
         (category_data['category_id'], category_data['name'], category_data['last_update'])),
        ("INSERT INTO language (language_id, name, last_update) VALUES (%s, %s, %s)", 
         (language_data['language_id'], language_data['name'], language_data['last_update'])),
        ("INSERT INTO film (film_id, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, last_update, special_features, fulltext) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
         (film_data['film_id'], film_data['title'], film_data['description'], film_data['release_year'], 
          film_data['language_id'], film_data['rental_duration'], float(film_data['rental_rate']), 
          film_data['length'], float(film_data['replacement_cost']), film_data['rating'], 
          film_data['last_update'], film_data['special_features'], film_data['fulltext'])),
        ("INSERT INTO staff (staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update, picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
         (staff_data['staff_id'], staff_data['first_name'], staff_data['last_name'], staff_data['address_id'], 
          staff_data['email'], staff_data['store_id'], staff_data['active'], staff_data['username'], 
          staff_data['password'], staff_data['last_update'], staff_data['picture'])),
        ("INSERT INTO store (store_id, manager_staff_id, address_id, last_update) VALUES (%s, %s, %s, %s)", 
         (store_data['store_id'], store_data['manager_staff_id'], store_data['address_id'], store_data['last_update'])),
        ("INSERT INTO customer (customer_id, store_id, first_name, last_name, email, address_id, activebool, create_date, last_update, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
         (customer_data['customer_id'], customer_data['store_id'], customer_data['first_name'], 
          customer_data['last_name'], customer_data['email'], customer_data['address_id'], 
          customer_data['activebool'], customer_data['create_date'], customer_data['last_update'], 
          customer_data['active'])),
        ("INSERT INTO inventory (inventory_id, film_id, store_id, last_update) VALUES (%s, %s, %s, %s)", 
         (inventory_data['inventory_id'], inventory_data['film_id'], inventory_data['store_id'], inventory_data['last_update'])),
        ("INSERT INTO rental (rental_id, rental_date, inventory_id, customer_id, return_date, status, staff_id, last_update) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
         (rental_data['rental_id'], rental_data['rental_date'], rental_data['inventory_id'], 
          rental_data['customer_id'], rental_data['return_date'], rental_data['status'], 
          rental_data['staff_id'], rental_data['last_update'])),
        ("INSERT INTO payment (payment_id, customer_id, staff_id, rental_id, amount, payment_date) VALUES (%s, %s, %s, %s, %s, %s)", 
         (payment_data['payment_id'], payment_data['customer_id'], payment_data['staff_id'], 
          payment_data['rental_id'], float(payment_data['amount']), payment_data['payment_date'])),
        ("INSERT INTO film_actor (actor_id, film_id, last_update) VALUES (%s, %s, %s)", 
         (film_actor_data['actor_id'], film_actor_data['film_id'], film_actor_data['last_update'])),
        ("INSERT INTO film_category (film_id, category_id, last_update) VALUES (%s, %s, %s)", 
         (film_category_data['film_id'], film_category_data['category_id'], film_category_data['last_update']))
    ]
    
    # Add all queries to the queue
    for query in mysql_queries:
        db_queue.put(('mysql', query))
    
    for query in oracle_queries:
        db_queue.put(('oracle', query))
    
    for query in postgresql_queries:
        db_queue.put(('postgresql', query))

def database_worker():
    """Worker thread to process database operations from the queue"""
    while True:
        db_type, (query, params) = db_queue.get()
        try:
            if db_type == 'mysql':
                execute_mysql_query(query, params)
            elif db_type == 'oracle':
                execute_oracle_query(query, params)
            elif db_type == 'postgresql':
                execute_postgresql_query(query, params)
        except Exception as e:
            print(f"Error in {db_type} worker: {e}")
        finally:
            db_queue.task_done()

def main():
    """Main function to run the data generation"""
    # Start database worker threads
    for _ in range(5):  # 5 worker threads
        worker = Thread(target=database_worker, daemon=True)
        worker.start()
    
    # Generate and insert data in batches
    batch_size = 10
    delay_seconds = 2
    
    try:
        while True:
            print(f"Generating and inserting {batch_size} records...")
            for _ in range(batch_size):
                generate_and_insert_data()
            
            # Wait for all operations to complete
            db_queue.join()
            print(f"Batch inserted successfully. Waiting {delay_seconds} seconds...")
            time.sleep(delay_seconds)
    except KeyboardInterrupt:
        print("\nStopping data generation...")
        # Wait for remaining operations to complete
        db_queue.join()
        print("All operations completed. Exiting.")

if __name__ == "__main__":
    main()
