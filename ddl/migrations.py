import psycopg2
from dotenv import load_dotenv
import os
from ddl.conn import *

load_dotenv()

db_name = None
table_name = None

# Create database if not exist
def create_database():
    connection = connection_to_postgresql()
    if connection is None:
        print("Failed to connect to the database.")
        return

    connection.autocommit = True
    cursor = connection.cursor()
    
    try:
        global db_name
        db_name = os.getenv("DATABASE_NAME")
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name};")
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        cursor.close()
        connection.close()

# Create table if not exist
def create_table():
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    cursor = connection.cursor()
    try:
        global table_name
        table_name = os.getenv("TABLE_NAME")
        cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
        exists = cursor.fetchone()[0]
        
        if not exists:
            create_table_query = f'''
            CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                file_path TEXT NOT NULL,
                question Text NOT NULL,
                response TEXT NOT NULL,
                product_category TEXT,
                product_name TEXT,
                answer TEXT
            );
            '''
            cursor.execute(create_table_query)
            connection.commit()
            print(f"Table '{table_name}' created successfully in the database.")
        else:
            print(f"Table '{table_name}' already exists.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        cursor.close()
        connection.close()

# Insert data into into table
def insert_into_table(file_path, question, response, product_category, product_name, answer):
    connection = get_db_connection()

    if connection is None:
        raise Exception("Failed to connect to the database.")
    
    cursor = connection.cursor()
    create_table()
    try:
        cursor.execute(f"INSERT INTO {table_name} (file_path, question, response, product_category, product_name, answer) VALUES (%s, %s, %s, %s, %s, %s)",
                       (file_path, question, str(response), str(product_category), str(product_name), str(answer)))
        connection.commit()
        return "added into the table"
        
    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        raise Exception(f"An error occurred while creating the user: {error}")
    
    finally:
        cursor.close()
        connection.close()