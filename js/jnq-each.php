<!DOCTYPE html>
<html>
<link rel="stylesheet" type="text/css" href="custom-select.css" />

<section>
    <div id="one"></div>
    <div id="two"></div>
    <div id="three"></div>
    <div id="four"></div>
</section>

<style>
label {
	display: inline-block;
	width:120px;
	text-alight=right;
}

div#one {
    float: left;
}
div#two {
    float: left;
}
div#three {
    float: left;
}
div#four {
    position: absolute;
    top :300px;
}


</style>

</html>
<html>
<div id="fsf">

			<?php 
			
					$xml = "<root>
									<dropdown id='1'>
										<field>xaxis</field>
										<values>
											<value>period</value>
											<value>dow</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<default>period</default>
									</dropdown>
									<dropdown id='2'>
										<field>yaxis</field>
										<values>
											<value>period</value>
											<value>dow</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<default>dow</default>
									</dropdown>
									<dropdown id='3'>
										<field>source_type</field>
										<values>
											<value>student</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<default>student</default>
									</dropdown>
									<dropdown id='4'>
										<field>source</field>
										<values>
											<value>dbinsert</value>
											<value>56n</value>
											<value>4n</value>
											<value>4s</value>
											<value>5s</value>
											<value>6s</value>
											<value>56n,4n,4s,5s,6s</value>
										</values>
										<default>dbinsert</default>
									</dropdown>
								</root>";
								
				$PHPLIBPATH = getenv("PHPLIBPATH");
				$SSDBPATH = getenv("SSDBPATH");
				$SSDBNAME = getenv("SSDBNAME");

				if ($PHPLIBPATH == "") {
					trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);	
				}

				set_include_path($PHPLIBPATH);

				include_once 'ui_utils.php';
				include_once 'db_utils.php';
				include_once 'xml2html2.php';
				include_once 'url.php';

				$api = php_sapi_name();

				if ($api=='cli') {
					$SSDBNAME = $argv[1];
					$SSDB = $SSDBPATH."/".$SSDBNAME;
				}
				else {
					$SSDB = $SSDBPATH."/".$SSDBNAME;
				}

				if ($SSDBNAME == "" or (file_exists($SSDB) == False)) {
					echo "a valid database name must be passed in as an argument";
				}
				
				$spanclass = NULL;
				$class=NULL;
				$spanclass = "custom-dropdown custom-dropdown--white";
				$class = "custom-dropdown__select custom-dropdown__select--white";
				
				echo "<div id='one'>";
				gethtmlxmlselect($xml,$_GET,$spanclass,$class);
				echo "</div>";				
				
				if (isset($_GET['source_type'])) {
					if ($_GET['source_type'] == "adult") {
						$source_type = 'teacher';
					}
					else {
						$source_type = $_GET['source_type'];
					}
				}
				else {
					$source_type = 'student'; // default
				}
				
				echo "<div id='two'>";
				gethtmldbselect($SSDB,'lesson',$source_type,"source_value",1,$_GET['source_value'],$spanclass,$class);
				echo "<br><br>";
				echo "</div>";

				echo "<div id='three'>";
				gethtmlmultiselect("status","status",explode(",",$_GET['ztypes']));
				gethtmlmultiselect("subject","subject",explode(",",$_GET['ztypes']));
				gethtmlmultiselect("adult","adult",explode(",",$_GET['ztypes']));
				gethtmlmultiselect("student","student",explode(",",$_GET['ztypes']));
				echo "</div>";
				?>

</div>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="test.js">

</script>
</html>

<?php

if(isset($_GET['ztypes'])) {

	$SSRESTURL = getenv("SSRESTURL");

	if ($SSRESTURL == "") {
		trigger_error("Fatal error: env SSRESTURL must be set", E_USER_ERROR);
	}

	$args = $_POST;
	if (sizeof(array_keys($_POST)) == 0){
		$args = $_GET;
	}

	if (isset($args['trantype']) == True) {
		switch ($args['trantype']) {
    		case 'new':
      		//$url = buildurl('http://blackbear:8080/new',$args);
      		$url = buildurl($SSRESTURL.'new',$args);
      	break;
    		default:
    			//$url = buildurl('http://blackbear:8080/',$args);
				$url = buildurl($SSRESTURL,$args);
		}
	}
	else {
		//$url = buildurl('http://blackbear:8080/',$args);
		$url = buildurl($SSRESTURL,$args);
	}

	$token = getcurl($url);
echo "<br><br>";
echo "<div id='four'>";
	draw($token,$args);
echo "</div>";
}

?>