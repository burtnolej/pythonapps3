<?php
//if(preg_match('/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i',$useragent)||preg_match('/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i',substr($useragent,0,4)))


?>

<html>

<section>
    <div id="one"></div>
    <div id="two"></div>
</section>

<style>
label {
	!display: inline-block;
	width:60px;
	text-alight=right;
}

div#one {
    float: left;
}
div#two {
    float: left;
}

</style>
</html>

<?php

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

//set_include_path('/home/burtnolej/Development/pythonapps3/phpapps/utils/');
//include_once 'ui_utils.php';
//include_once 'db_utils.php';

function draw_login($dbname,$tablename,$submitpage) {
?>

<html>
	<body>
		<?php echo "<form method='post' action='".$_SERVER['PHP_SELF']."' accept-charset='UTF-8'>";?>
	
			<fieldset >
				<input type='hidden' name='submitted' id='submitted' value='1'/>
				<div>
				<?php
					
					if (isset($_POST['source_value'])) { 
						$sourcevaldefault=$_POST['source_value'];
					}
					else {
						$sourcevaldefault="Donny";
					}
					
					if (isset($_POST['xaxis'])) { 
						$xaxisdefault=$_POST['xaxis'];
					}
					else {
						$xaxisdefault="period";
					} 

					$xml = "<root>
									<dropdown id='1'>
										<field>xaxis</field>
										<values>
											<value>period</value>
											<value>dow</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<default>".$xaxisdefault."</default>
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
										</values>
										<default>student</default>
									</dropdown>
									<dropdown id='4'>
										<field>source_value</field>
										<values>
											<value>Donny</value>
										</values>
										<default>".$sourcevaldefault."</default>
									</dropdown>
									<dropdown id='5'>
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
									</dropdown>
								</root>";
					
					echo "<div id='one'>";

					//('test.sqlite','lesson');
					gethtmlxmldropdown($xml);
					
					echo "</div>";
				
					echo "<div id='two'>";

					getdbhtmlmultiselect($dbname,"select name from sqlite_master","ztypes",4,$_POST['ztypes']);
					
					echo "</div>";

					gethtmlbutton('submit','go');
					
				?>
				</div>
			</fieldset>
		</form>
	</body>
</html>
<?php
}

    
$api = php_sapi_name();

if ($api=='cli') {
	$SSDBNAME = $argv[1];
	$SSDB = $SSDBPATH."/".$SSDBNAME;
}
else {
	$SSDB = $SSDBPATH."/".$SSDBNAME;
}

if ($SSDBNAME <> "" and (file_exists($SSDB) == True)) {
	
	draw_login($SSDB,'lesson','getlink.php');
}
else {
	echo "a valid database name must be passed in as an argument";
}

if(isset($_POST['submitted'])) {
	$args = $_POST;
	$SSRESTURL = getenv("SSRESTURL");
	$url = buildurl($SSRESTURL,$args);
	$token = getcurl($url);
	draw($token,$args);
}
?>
