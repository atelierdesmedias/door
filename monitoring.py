# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen
import time
import os

#
# Monitoring
#
# Simply POST to http://atelier-medias.org/porte-status.php every minute. See that URL for status.
#

def _log(info):
    LOGFILE='/tmp/monitoring.log'
    if os.path.exists(LOGFILE) and (os.path.getsize(LOGFILE) > (100 * 1000 * 1000)):
        os.remove(LOGFILE)
    with open(LOGFILE, 'a') as file: file.write(info + "\n")
    
def ping(status):
    '''ping the intranet to tell him we are alive :)'''
    try:
        data = urlencode({'status': status if status else b''}).encode()
        urlopen('https://www.atelier-medias.org/porte-status.php', data=data, timeout=10)
    except Exception as e:
        _log("Error in ping: %r" % e)

def sync():
    '''Sync the card numbers, ie. simply ping www/index.php file in the same git repo, which will query the intranet

    Returns: None if successful, error information otherwise.'''
    try:
        output = urlopen('http://localhost/', data=urlencode({'sync': '1'}).encode(), timeout=10).read().decode()
    except Exception as e:
        return ("Error in sync: %r" % e)
    return None if ('<b>OK</b>' in output) else ("POST to http://porte.local failed: " + (output if output else "no data returned"))

ping('Started')

while True:
    ping(("ERROR: " + sync_status) if sync_status else '')
    time.sleep(60)


'''

le script qui est sur http://atelier-medias.org/porte-status.php est:

<?php

/*
Monitoring de la porte.

Le serveur d'ouvreur de porte fait un POST sur cette page PHP toutes les minutes
*/

$marker = '/tmp/mark.txt';
$log = '/tmp/porte-status.txt';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
   if(!empty($_POST['status'])) {
      if (filesize($log) > (100*1000*1000)) { unlink($log); } // avoid filling tmp folder - limit to 100MBytes
      file_put_contents($log, date(DATE_RFC2822).": ".$_POST['status']."\n", FILE_APPEND);
   }
   else {
      file_put_contents($marker, "placeholder file for http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]");
   }
   exit("OK\n");
}

echo "<html>";
echo '<head><meta charset="UTF-8"></head><body>';

echo "<h1>Monitoring de la porte de l'AdM</h1>";
echo "<p>Current status:</p>";

$time = time() - filemtime($marker);
if ( file_exists($marker) && ($time < (5 * 60)) ) // 5 minutes
{  
   echo '<p><font color="green">OK</font></p>';
}
else
{  
   // Ne pas modifier ce texte ! le monitoring l'utilise
   echo '<p><font color="red">NOT OK</font></p>';
}
echo "<p>Last ping from the door: ".gmdate("H:i:s", $time)." ago.</p>";

echo "<h1>Liens utiles</h1>";
echo "<p><a href=\"http://192.168.1.8\">Site de la porte</a> (seulement accessible depuis le reseau interne de l'AdM)</p>";
echo "<p><a href=\"http://www.gotsitemonitor.com\">Monitoring de cette page</a> (login: adm-informatique+porte@googlegroups.com password: adm ) verifie que cette page ne contient pas <i>NOT-espac\
e-OK</i></p>";
echo "<h1>Historique</h1><pre>";
echo file_get_contents($log);
echo "</pre></p>";

echo "</body><html>";

?>


'''
