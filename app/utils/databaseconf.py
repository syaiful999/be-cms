import os
import psycopg2
import psycopg2.extras
import json
import datetime


def databaseConnector():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT'),
            password=os.getenv('DATABASE_PASSWORD')
        )
        db = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return db
    except AssertionError as e:
        raise TypeError(e)


def runQuery(query):
    try:
        db = databaseConnector()
        db.execute(query)
        data = db.fetchall()
        db.close()
        jsonStringConv = json.dumps(data, default=dateTimeConverter)
        return json.loads(jsonStringConv)
    except AssertionError as e:
        raise TypeError(e)


def runMutationQuery(query, values):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT'),
            password=os.getenv('DATABASE_PASSWORD')
        )
        cur = conn.cursor()
        cur.execute(query, (values))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return id


def runDelete(query, part_id):
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT'),
            password=os.getenv('DATABASE_PASSWORD')
        )
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(query, (part_id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def dateTimeConverter(data):
    if isinstance(data, datetime.datetime):
        return data.__str__()
