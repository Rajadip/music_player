import sqlite3 as db

def Connect():
    connection = None
    try:
        connection = db.connect('Playlist')
    except db.Error as e:
        print("ERROR %s:" % e.args[0])
    finally:
        return connection


def CloseConnection(connection):
    if connection:
        connection.close()


def Insert(query, argList):
    conn = None
    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(query, argList)
        conn.commit()
        return True
    except db.Error as e:
        print(str(e))
        return False
    finally:
        CloseConnection(conn)


def Select(query, argList):
    conn = None
    data = None
    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(query, argList)
        data = cursor.fetchall()
    except db.Error as e:
        print(str(e))
    finally:
        CloseConnection(conn)
        return data

def Delete(query,argList=()):
    conn=None
    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(query,argList)
        conn.commit()
        return True
    except db.Error as e:
        print(str(e))
        return False
    finally:
        CloseConnection(conn)
