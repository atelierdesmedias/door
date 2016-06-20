# -*- coding: utf-8 -*-
import http.client
import time

#
# Monitoring. Simply POST to http://atelier-medias.org/porte-status.php every minute. See that URL for status.
#

def ping():
    http.client.HTTPConnection("atelier-medias.org", timeout=20).request("POST", "/porte-status.php")


while (True):
    ping()
    time.sleep(60)


'''

pour reference, le script qui est sur http://atelier-medias.org/porte-status.php :

<?php

/* 
Monitoring de la porte - 

Design:

Une petit page PHP avec le fonctionnement suivant :

- on met un thread ou service Python dans le serveur d'ouvreur de porte qui fait un POST sur cette page PHP toutes les ~2 minutes. ce POST sauve un fichier-marqueur
- Lorsqu'on fait un GET sur cette page PHP, elle montre "OK" en vert si (et seulement si) le fichier-marqueur est a été modifié il y  moins de 5 minutes
- un service de monitoring HTTP/HTML tierce (y'en a plein de gratuits) vérifie que la page continue toujours "OK" en vert et nous envoie un email/SMS/whatever si ce n'est pas le cas

De cette manière, on vérifie "end-to-end" que:
  * le serveur d'ouvreur de porte est "up and running" - dès qu'il a un prb, le monitoring va nous alerter
  * l'internet marche depuis le bureau
  * le monitoring fonctionne (le script ici-présent est bien hébergé sur un serveur qui marche)

Le seul point de défaillance est le service de monitoring tierce. Mais c'est leur métier, non ? et on pourrait d'ailleurs facilement en avoir plusieurs, puisque c'est juste un GET sur une page web.

Un inconvénient, est de ne pas pouvoir différencier à distance entre une panne d'internet, et une panne du serveur de porte. Mais par définition, nous ne pouvons plus rien monitorer si l'internet ne marche pas, à moins d'utiliser des moyens alternatifs, tels que fusées de détresse, pigeon voyageurs, drone immobile au-dessus du Rhône... Et rien ne nous empêche d'avoir un autre systeme (similaire à celui-ci ?) pour monitorer la connection internet. Mais c'est un autre sujet : je ne sais pas si c'est un problème que nous avons.

*/

$marker = '/tmp/mark.txt';
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
   file_put_contents($marker, "placeholder file for http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]");
   exit("OK\n");
}

echo "<html>";
echo '<head><meta charset="UTF-8"></head><body>';

echo "<h1>Monitoring de la porte de l'AdM</h1>";
echo "<p>Current status:</p>";
echo "<p>";

$time = 5 * 60 ; //in seconds 

if ( file_exists($marker) && ( (time() - filemtime($marker)) < $time ) )
{
   echo '<p><font color="green">OK</font></p>';
}
else
{
   echo '<p><font color="red">NOT ';
   echo 'OK</font></p>';   
}  

echo "<p>Last ping from the door: ".gmdate("H:i:s", (time() - filemtime($marker)))." ago.</p>";
echo "<br/><br/><br/><br/>------<br/>(This file contains:<pre>";
echo htmlspecialchars(file_get_contents(basename(__FILE__)));
echo "</pre>";
echo ")";
echo "</body><html>";

?>
'''
