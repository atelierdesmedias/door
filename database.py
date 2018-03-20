'''
Helper for database access. 
'''
import mysql.connector
import threading

def createConnection():
    connection = mysql.connector.connect(
        user='door', password='door',
        host='127.0.0.1',
        database='door')

    return connection;

def containsCard(code):
    connection = createConnection()

    cursor = connection.cursor()
    query = ("SELECT * FROM card where code = %s")
    data = (code,)
    cursor.execute(query, data, False)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result is None:
        return False

    return True

def log_card_async(code, success):
    thread = threading.Thread(target=log_card, args=(code, success,))
    thread.start()

def log_card(code, success):
    connection = createConnection()

    cursor = connection.cursor()
    query = ("INSERT INTO log_card (code, success, timestamp) VALUES (%s, %s, now())")
    data = (code, success,)
    cursor.execute(query, data, False)

    connection.commit()

    cursor.close()
    connection.close()

def log_button_async():
    thread = threading.Thread(target=log_button)
    thread.start()

def log_button():
    connection = createConnection()

    cursor = connection.cursor()
    query = ("INSERT INTO log_button (timestamp) VALUES (now())")
    cursor.execute(query, multi=False)

    connection.commit()

    cursor.close()
    connection.close()

def log_door_async(info):
    thread = threading.Thread(target=log_door, args=(info,))
    thread.start()

def log_door(info):
    connection = createConnection()

    cursor = connection.cursor()
    query = ("INSERT INTO log_door (info, timestamp) VALUES (%s, now())")
    data = (info,)
    cursor.execute(query, data, multi=False)

    connection.commit()

    cursor.close()
    connection.close()
