<?php
$servername = "localhost";
$username = "door";
$password = "door";
$dbname = "door";

// Create connection
$link = new mysqli($servername, $username, $password, $dbname);
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Gestion des cartes</title>
</head>
<body>

<?php
// Check connection
if ($link === false) {
    die("Connection failed: " . $conn->connect_error);
}else{
	if(!empty($_POST))
	{
		if(!empty($_POST['add_new_code']))
		{
			// Escape user inputs for security
			$new_code = mysqli_real_escape_string($link, $_POST['new_code']);
			// Attempt insert query execution
			$check_if_exist = $link->query("SELECT * FROM card WHERE code = '$new_code'"); 
		        
			if(mysqli_num_rows($check_if_exist) > 0){
				echo "Carte dejà présente";
			}else{
				$sql_insert = "INSERT INTO card (code) VALUES ('$new_code')";
				$result = $link->query($sql_insert);
				if($result){
					echo "Carte correctement ajouté";
				} else{
					echo "ERREUR: requette. " . mysqli_error($link);
				}
			}
			// Close connection
			// mysqli_close($link);
		}
		if(!empty($_POST['checkbox']))
		{
			foreach($_POST['checkbox'] as $checkbox){
				$sql_remove = "DELETE FROM card WHERE code = $checkbox";
   				$remove = $link->query($sql_remove);
			}
		}
	}
}
?>


<h1>Ajouter carte</h1>

<form action="" method="post">
    <p>
        <label for="new_code">Code carte à ajouter:</label>
        <input type="text" name="new_code" id="new_code">
    </p>
    <input type="submit" name="add_new_code" value="Ajouter">
</form>

<h1>Listing des cartes</h1>

<form action="" method="post">
    <p>
<?php
	$sql = "SELECT * FROM card";
	$result = $link->query($sql);
	if ($result->num_rows > 0) {
		while($row = $result->fetch_assoc()){
?>
			<div class="line-card">
				<label for="cbox2">card id : <?php echo $row["code"] ?></label>
				<input type="checkbox" class='form' value="<?php echo $row["code"] ?>" name="checkbox[]" />
			</div>
<?php
		}
	}else {
		echo "0 results";
	}
?>
	</p>
    <input type="submit" name="remove_code" value="Supprimer">
</form>

</body>
</html>
