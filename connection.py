import os
import psycopg2
import psycopg2.extras


def get_connection_string():
    username = os.environ.get("PSQL_USERNAME")
    host = os.environ.get("PSQL_HOST")
    password = os.environ.get("PSQL_PASSWORD")
    db_name = os.environ.get("PSQL_DB_NAME")
    return f"postgresql://{username}:{password}@{host}/{db_name}"


def open_database():
    connection = psycopg2.connect(get_connection_string())
    connection.autocommit = True
    return connection


def connection_handler(fn):
    def wrapper(*args, **kwargs):
        connection = open_database()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        result = fn(cursor, *args, **kwargs)
        cursor.close()
        connection.close()
        return result

    return wrapper
