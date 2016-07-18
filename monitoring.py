# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen
import time
import os

#
# Monitoring and card number sync
#
# Simply POST to http://atelier-medias.org/porte-status.php every minute. See that URL for status.
# Also sync the card numbers from the intranet by POSTING to http://localhost/ (see www.index.php)
#

def _log(info):
    LOGFILE='/tmp/monitoring.log'
    if os.path.exists(LOGFILE) and (os.path.getsize(LOGFILE) > (100 * 1000 * 1000)):
        os.remove(LOGFILE)
    with open(LOGFILE, 'a') as file: file.write(info + "\n")
    
def ping(status):
    try:
        data = urlencode({'status': status if status else b''}).encode()
        urlopen('http://atelier-medias.org/porte-status.php', data=data, timeout=10)
    except Exception as e:
        _log("Error in ping: %r" % e)

def sync():
    # sync the card numbers. See the www/index.php file in the same git repo as this file.
    try:
        output = urlopen('http://localhost/', data=urlencode({'sync': '1'}).encode(), timeout=10).read().decode()
    except Exception as e:
        return ("Error in sync: %r" % e)
    return None if ('<b>OK</b>' in output) else "Sync failed: 'OK' not found in output of POST to http://localhost/ (aka http://porte/)"

ping('Started')


while (True):
    sync_status = sync()
    ping(sync_status)
    time.sleep(60)


'''

le script qui est sur http://atelier-medias.org/porte-status.php est:

<?php

/*
Monitoring de la porte - Une petit page PHP avec le fonctionnement suivant :

- le serveur d'ouvreur de porte qui fait un POST sur cette page PHP toutes les minutes. Optionnellement il peut passer un champs "status" qui est logge
- Lorsqu'on fait un GET sur cette page PHP, elle montre "OK" en vert si (et seulement si) le fichier-marqueur est a été modifié il y  moins de 5 minutes
- un compte de monitoring sur http://www.gotsitemonitor.com (login: adm-informatique+porte@googlegroups.com password: adm ) verifie la presence de 'OK'
  toutes les 10 minutes, et envoie un email a adm-informatique+porte@googlegroups.com si '>OK<' n'est pas present sur la page
*/

$marker = '/tmp/mark.txt';
$log = '/tmp/porte-status.txt';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
   file_put_contents($marker, "placeholder file for http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]");
   if(!empty($_POST['status'])) {
      if (filesize($log) > (100*1000*1000)) { unlink($log); } // avoid filling tmp folder - limit to 100MBytes
      file_put_contents($log, date(DATE_RFC2822).": ".$_POST['status']."\n", FILE_APPEND);
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
   echo '<p><font color="red">NOT OK</font></p>';
}
echo "<p>Last ping from the door: ".gmdate("H:i:s", $time)." ago.</p>";

echo "<p>Status history: <pre>";
echo file_get_contents($log);
echo "</pre></p>";

echo "</body><html>";

?>

'''
