
<?php
class recipe_arrays
{
    public function dump_array($array)
    {
        foreach ($array as $key => $value) {
            echo $key, $value;
        }
    }
}

function create_empty_array(){
	return array();
}

function append_to_array(&$array,$append_item){
	$array[] = $append_item;
}

/* basic array */
$basic_array = array(
    123,456
);

print_r($basic_array);
append_to_array($basic_array,789);
print_r($basic_array);

echo gettype(create_empty_array());

if (is_array(create_empty_array())){
	echo "its an array"; 
}
$array = array(
    "foo" => "bar",
    "bar" => "foo",
);
/* basic associative */



print join($array,",");


// array comprehension

$out=array_map(function($x) {return $x*$x;}, range(0, 9))

// array operators


if (array("foo","bar") == array("foo","bar")){
}
?>

	
	setattr
	getattr
	
	$array=array();
	foreach ($attrs as $attr) {
		$array[$attr] = $menu_item[$attr];
	}