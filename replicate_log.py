import urllib
import requests
import database
import json
from datetime import datetime

'''

Code to send the log of the database to the intranet

Called every 5 minutes by a cron job by root.

Only sends the items that have been added since the last server timestamp.
'''


def getRemoteTimestamp(table):
    request = requests.get('https://intra.atelier-medias.org/xwiki/bin/get/Door/Code/ReplicationService?outputSyntax=plain&code=85aV5wzDDZFJLDQ6&table=' + table + '&raction=lasttimestamp')
    rtext = request.text

    remoteTimestamp = 0
    if (rtext.isdigit()):
      remoteTimestamp = float(request.text) / 1000

    return datetime.utcfromtimestamp(remoteTimestamp)

def pushTable(table, l):
    url = 'https://intra.atelier-medias.org/xwiki/bin/get/Door/Code/ReplicationService'
    params = {'outputSyntax': 'plain', 'table': table, 'raction': 'push', 'code' : '85aV5wzDDZFJLDQ6'}
    r = requests.post(url, params=params, json=l)
    print(r.status_code, r.reason, r.text)

############################
## log_card
############################

remoteDate = getRemoteTimestamp('log_card')

connection = database.createConnection()
cursor = connection.cursor()
query = ('SELECT * FROM log_card where timestamp > %s')
data = (remoteDate,)
cursor.execute(query, data, False)

results = cursor.fetchall()

l = []
for code, success, timestamp in results:
    l.append({'code' : code, 'success' : success, 'timestamp' : int(timestamp.timestamp() * 1000)})

print(l)

cursor.close()
connection.close()

pushTable('log_card', l)

############################
## log_door
############################

remoteDate = getRemoteTimestamp('log_door')

connection = database.createConnection()
cursor = connection.cursor()
query = ('SELECT * FROM log_door where timestamp > %s')
data = (remoteDate,)
cursor.execute(query, data, False)

results = cursor.fetchall()

l = []
for timestamp, info in results:
    l.append({'info' : info, 'timestamp' : int(timestamp.timestamp() * 1000)})

print(l)

pushTable('log_door', l)
