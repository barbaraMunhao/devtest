
# DB Functions to create the database and the demand table.
# The database and the demand table are created if they do not already exist.

import sqlite3


def create_database(database_file):
    connection = None
    try:
        connection = sqlite3.connect(database_file)
        create_demand_table(connection)

    except sqlite3.Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def create_demand_table(connection):
    cursor = connection.cursor()
    query = ("CREATE TABLE IF NOT EXISTS demand ( id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
             "elevator_id INT, rest_floor INT, demanded_floor INT)")
    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)

