
<?php

include 'menu.php';

$xml = new SimpleXMLElement($xmlstr);

// output all of 10000 item and children
//print_r($xml->items->{'item'});

// print all the labels
foreach ($xml->items->{'item'} as $item) {
	print_r($item->label);
	$parent = $item->xpath(".."); 
	print_r($parent->{'label'});
}
#print_r($xml);

?>
