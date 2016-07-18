<?php
$servername = "localhost";
$username = "door";
$password = "door";
$dbname = "door";

$link = new mysqli($servername, $username, $password, $dbname);
if ($link === false) {
    die("Connection to DB failed");
}

function db() {
	global $link;
	return $link;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Gestion des cartes</title>
</head>
<body>

<?php

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
	history("ADDED $card");
	
	$card = mysqli_real_escape_string(db(), $card);

	$check_if_exist = db()->query("SELECT * FROM card WHERE code = '$card'"); 
	        
	if(mysqli_num_rows($check_if_exist) > 0){
		echo "Carte dejà présente";
	}else{
		$sql_insert = "INSERT INTO card (code) VALUES ('$card')";
		$result = db()->query($sql_insert);
		if(!$result){
			echo "ERREUR: requette. " . mysqli_error(db())."<br/>";
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
	$sql_remove = "DELETE FROM card WHERE code = $card";
 	$remove = db()->query($sql_remove);
}

function process_cards($process_coworker, $process_card)
{
	$json = json_decode(file_get_contents('https://intra.atelier-medias.org/xwiki/bin/get/XWiki/CoworkersService?outputSyntax=plain&code=85aV5wzDDZFJLDQ6'), true);
	if (count($json["coworkers"]) < 30) {
	   //paranoid: fail if not enough :) coworkers. This should catch any issue with the intranet.
 	   die("Recu ".count($json["coworkers"])." coworkers de l'intranet, qq chose de pourri !!");
	}
	
	$cards = get_cards();
	foreach($json["coworkers"] as $coworker)
	{
		$process_coworker($cards, $coworker);
		$cards = array_diff($cards, [$coworker["card"]]);
	}
	
	foreach($cards as $card) {
		$process_card($card);
	}
}

if($_SERVER['REQUEST_METHOD'] === 'POST')
{
	if(!empty($_POST['sync']))
	{
		process_cards(function ($cards, $coworker) {
				if ($coworker["card"] && (! in_array($coworker["card"], $cards)) && (($coworker["formule"] === "nomade") || ($coworker["formule"] === "fixe") )) {
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
	echo "<br/>Liste des coworkers nomades ou fixes dont la carte n'est pas  d&eacute;finie correctement sur l'intranet (absent sur la porte, ou incorrecte)<br/>";
	process_cards(function ($cards, $coworker) {
		if (! ($coworker["card"] && in_array($coworker["card"], $cards)) && (($coworker["formule"] === "nomade") || ($coworker["formule"] === "fixe") )) {
		     echo "<br/>".$coworker["email"]." - ".$coworker["first_name"]." ".$coworker["last_name"]." - ".$coworker["formule"]." (".($coworker["card"] ? "absent de la porte: ".$coworker["card"] : "non d&eacute;fini sur l'intranet").")";
		}
	}, function ($card) { });
}
elseif (!empty($_GET['list']))
{      
	echo "<br/><br/>Liste des cartes qui seront ajout&eacute;es (coworkers nomades ou fixes, dont la carte est d&eacute;finie dans l'intranet mais pas pr&eacute;sent dans la porte):";
	echo "<br/>";
	process_cards(function ($cards, $coworker) {
		if ($coworker["card"] && (! in_array($coworker["card"], $cards)) && (($coworker["formule"] === "nomade") || ($coworker["formule"] === "fixe") )) {
		   echo "<br/>".$coworker["card"]. " (".$coworker["email"]." - ".$coworker["first_name"]." ".$coworker["last_name"]." - ".$coworker["formule"].")";
		}
	}, function ($card) use (&$missing) { $missing .= "<br/>".$card."\n";});

	echo "<br/><br/>Liste des cartes qui seront enlev&eacute;es de la porte:";
	echo "<br/>";
 	echo $missing;
}
else
{
?>


<h1>Sync des cartes depuis l'intranet</h1>

<a href="?list=1">Voir la liste des cartes &agrave; syncer...</a>
<br/>
<br/>
<form action="" method="post">
    <input type="submit" name="sync" value="Sync immediatement !">
</form>


<h1>Historique des changements</h1>

<a href="history.txt">ici</a>.

<h1>Coworkers sans carte</h1>

<a href="?missing=1">ici</a>.

<h1>Liste des cartes</h1>

    <p>
<?php
	foreach(get_cards() as $card) {
?>
			<div class="line-card">
				<label for="cbox2">card id : <?php echo $card ?></label>
			</div>
<?php
		}
?>
	</p>
<?php
}
?>
</body>
</html>
