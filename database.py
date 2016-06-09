import mysql.connector

def containsCard(code):
    '''
    Helper for database access. 
    '''
    conection = mysql.connector.connect(
        user='door', password='door',
        host='127.0.0.1',
        database='door')

    cursor = conection.cursor()
    query = ("SELECT * FROM card where code = %s")
    data = (code,)
    cursor.execute(query, data, False)

    result = cursor.fetchone()

    cursor.close()

    conection.close()

    if result is None:
        return False

    return True

