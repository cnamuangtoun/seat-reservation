#!/usr/bin/python

import sqlite3
from sqlite3 import Error
from pathlib import Path




def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect("data.sqlite")
        return conn
    except Error as e:
        print(e)

    return None


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM seats")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE seats
              SET status = ?
              WHERE seat_id = ?'''
    cur = conn.cursor()
    cur.execute(sql,task)
    print(cur.rowcount)

def conmain():
    #database = "C:\\Users\Asus\Desktop\seat-reservation-v2\data.sqlite"
    # create a database connection
    print("Hello")
    conn = create_connection("data.sqlite")
    print("Hello")
    with conn:
        update_task(conn, (1, 'A0'))
