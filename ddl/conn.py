import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def connection_to_postgresql():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        )
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return None
    
def get_db_connection():
    try:
        # Connect to the PostgreSQL database
        db_connection = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            database=os.getenv("DATABASE_NAME")
        )
        return db_connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return None