<?php
$configuration = parse_ini_file("/usr/local/door/www/configuration.ini");

$servername = $configuration['servername'];
$username = $configuration['username'];
$password = $configuration['password'];
$dbname = $configuration['dbname'];
$code = $configuration['code'];
$extracards = $configuration['extracards'];

$link = new mysqli($servername, $username, $password, $dbname);
if ($link === false) {
    die("Connection to DB failed");
}

function db() {
	global $link;
	return $link;
}

function history($action)
{
    file_put_contents('/usr/local/door/www/history.txt',  date(DATE_RFC2822).": ".$action."\n", FILE_APPEND);
}

function debug() {
	  // set it to 1 to avoid changing the DB
	 return 0;
}

function get_cards() {
	 $result = db()->query("SELECT code FROM card ORDER BY code");
	 
	 if ($result->num_rows > 0) {
	 	while($row = $result->fetch_assoc()){
 			   $cards[] = $row["code"];
		}
	}

	return $cards;
}

function add_card($card)
{
	echo "ADDING $card<br/>";
	if (debug()) {
	    return;
	}
	
	$card = mysqli_real_escape_string(db(), $card);

	$check_if_exist = db()->query("SELECT * FROM card WHERE code = '$card'"); 
	        
	if(mysqli_num_rows($check_if_exist) > 0){
		history("CARD ALLREADY PRESENT $card");
		echo "Carte dejà présente";
	}else{
		$sql_insert = "INSERT INTO card (code) VALUES ('$card')";
		$result = db()->query($sql_insert);
		if(!$result){
			echo "ERREUR: requette. " . mysqli_error(db())."<br/>";
 			history("ERROR ADDING $card");
		} else {
		  history("ADDED $card");
		}
	}
}

// not used -- only to recover a backup, e.g.:
//add_from_file('/usr/local/door/www/cartes_20160712.txt'); exit(1);
function add_from_file($file)
{
	foreach(explode("\n", trim(file_get_contents($file))) as $card)
	{
		add_card($card);
	}
}

function delete_card($card)
{
	echo "DELETING $card<br/>";
	if (debug()) {
	    return;
	}
	history("DELETING $card");

	$card = mysqli_real_escape_string(db(), $card);
	$sql_remove = "DELETE FROM card WHERE code = '$card'";
 	$remove = db()->query($sql_remove);
}

function get_coworkers_from_intranet() {
	global $code;
	global $extracards;

	$json = json_decode(
		file_get_contents(
			"https://intra.atelier-medias.org/xwiki/bin/get/XWiki/CoworkersService?outputSyntax=plain&code=$code",
			// TODO: decide if we allow not having a valid certificate ?
			false/*,
			stream_context_create([
				"ssl" => [
					"verify_peer"=>false,
 					"verify_peer_name"=>false
				]
			])
		*/),
		true);
	if (count($json["coworkers"]) < 30) {
	   //paranoid: fail if not enough :) coworkers. This should catch any issue with the intranet.
 	   die("ERREUR: Re&ccedil;u ".count($json["coworkers"])." coworkers de l'intranet, y-a-t-il un probl&egrave;me de connection &agrave; l'intranet ?");
	}

	$coworkers = array_filter($json["coworkers"], function($coworker) {
	     return (($coworker["active"] == 1) // already done on the server, but ya never now
	     	      && (($coworker["formule"] === "nomade") || ($coworker["formule"] === "fixe") || ($coworker["membre_honneur"] == 1)));
		     });

	// Add extra cards
	foreach($extracards as $extracard) {
		$coworkers[] = array('card' => $extracard);
	}

	return $coworkers;
}

function process_cards($process_coworker, $process_card_to_remove)
{
	$cards = get_cards();
	$coworkers = get_coworkers_from_intranet();
	foreach($coworkers as $coworker)
	{
	   $process_coworker($cards, $coworker);
	   // enleve de la liste des cartes, ceux utilisee sur l'intranet
	   $cards = array_diff($cards, [$coworker["card"]]);
	}


	foreach($cards as $card) {
		$process_card_to_remove($card);
	}
}


?>
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Gestion des cartes</title></head><body>
<?php

if($_SERVER['REQUEST_METHOD'] === 'POST')
{
	if(!empty($_POST['sync']))
	{
		process_cards(function ($cards, $coworker) {
			if ($coworker["card"] && (! in_array($coworker["card"], $cards))) {
			           add_card($coworker["card"]);
				}
			}, function ($card) {
 			   	delete_card($card);
			});
			echo "<b>OK</b>"; // Used for monitoring -- See the 'monitoring.py' file in the same git repo as this file.
	}

}
elseif (!empty($_GET['missing']))
{
	echo "<br/>Liste des coworkers nomades ou fixes dont la carte n'est pas d&eacute;finie correctement sur l'intranet<br/>";
	process_cards(function ($cards, $coworker) {
	        if ($coworker["membre_honneur"] == 1) {
		   return;
		}
		if (( !($coworker["card"] && in_array($coworker["card"], $cards))) ||
		    (strlen($coworker["card"]) != 10) ||
		    (substr($coworker["card"], 0, 3 ) !== "000")) {
		     echo "<br/>".$coworker["email"]." - ".$coworker["first_name"]." ".$coworker["last_name"];
		     if ($coworker["card"]) {
		       echo " - ".$coworker["card"].": ";
		       if (in_array($coworker["card"], $cards)) {
		          echo "code invalide (pas 10 chiffres ou ne commencant pas par 3 zeros)";
 		       } else {
			  echo "m&ecirc;me code utilis&eacute; par plusieurs coworkers dans l'intranet: ";
			  // pas efficace, mais pas grave, c'est un cas rare...
 			  echo implode(", ", array_map(function($c) { return $c["first_name"]." ".$c["last_name"]; },
			  	   array_filter(get_coworkers_from_intranet(), function($c) use (&$coworker) { return ($c["card"] === $coworker["card"]); })));
		       }
 		     }
 	             else {
		          echo ": non d&eacute;fini dans l'intranet !";
		     }
		}
	}, function ($card) { });
}
elseif (!empty($_GET['list']))
{      
	echo "<br/><br/>Liste des cartes qui seront ajout&eacute;es (coworkers nomades ou fixes, dont la carte est d&eacute;finie dans l'intranet mais pas pr&eacute;sent dans la porte):";
	echo "<br/>";
	$found = FALSE;
	process_cards(function ($cards, $coworker) use (&$found) {
		if ($coworker["card"] && (! in_array($coworker["card"], $cards))) {
		   echo "<br/>".$coworker["card"]. " (".$coworker["email"]." - ".$coworker["first_name"]." ".$coworker["last_name"]." - ".$coworker["formule"].")";
		   $found = TRUE;
		}
	}, function ($card) use (&$missing) { $missing .= "<br/>".$card."\n";});

	if (!$found) {
	   echo "(pas de carte &agrave; ajouter)";
	}
	echo "<br/><br/>Liste des cartes qui seront enlev&eacute;es de la porte:";
	echo "<br/>";
 	echo $missing;
	if (!$missing) {
	   echo "(pas de carte &agrave; enlever)";
	   }
}
elseif (!empty($_GET['cartes']))
{
	foreach(get_cards() as $card) {
?>
			<div class="line-card">
				<label for="cbox2">card id : <?php echo $card ?></label>
			</div>
<?php
		}
}
elseif (!empty($_GET['coworkers']))
{      
        echo "Coworker with cards (only nomades, fixes et membres d'honneur): ";
	process_cards(function ($cards, $coworker) {
		if ($coworker["card"]) {
		   echo "<br/>".$coworker["card"]. " (".$coworker["email"]." - ".$coworker["first_name"]." ".$coworker["last_name"]." - ".$coworker["formule"].")";
		}
	}, function ($card) { });
}
else
{
?>

<h1>Porte de l'Adm</h1>

Pour activer votre carte (ou badge), voir les instructions sur <a href="https://intra.atelier-medias.org/xwiki/bin/view/Main/Badge">l'intranet</a>.

<h1>Infos et liens utiles</h1>

<p>
<a href="?list=1">Liste des cartes &agrave; syncer</a>
<form action="" method="post">
    <input type="submit" name="sync" value="Sync immediatement !">
</form>
</p>

<p><a href="history.txt">Historique des changements</a></p>

<p><a href="?missing=1">Coworkers sans carte</a></p>

<p><a href="?cartes=1">Liste des cartes sur la porte</a></p>

<p><a href="?coworkers=1">Liste des coworkers avec cartes</a></p>


<?php
}
?>
</body></html>
