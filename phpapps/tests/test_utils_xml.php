<?php

$xmlstr = <<<XML
<menu>
	<menuitemid>1</menuitemid>
	<label>root</label>
	<menuitem>
		<menuitemid>2</menuitemid>
		<label>theuppermiddle</label>
		<tag>foo</tag>
		<menuitem>
			<menuitemid>3</menuitemid>
			<label>thelowermiddle</label>
			<tag>bar</tag>
			<menuitem>
				<menuitemid>31</menuitemid>
				<label>thebottom</label>
				<tag>foobar</tag>
			</menuitem>
		</menuitem>
		<menuitem>
			<menuitemid>4</menuitemid>
			<label>thelowermiddle-sibling1</label>
			<menuitem>
				<menuitemid>41</menuitemid>
				<label>thelowermiddle-cousin1</label>
			</menuitem>
		</menuitem>
		<menuitem>
			<menuitemid>5</menuitemid>
			<label>thelowermiddle-sibling2</label>
			<menuitem>
				<menuitemid>51</menuitemid>
				<label>thelowermiddle-sibling-child1</label>
				<menuitem>
					<menuitemid>511</menuitemid>
					<label>thelowermiddle-sibling-grandchild1</label>
					<menuitem>
						<menuitemid>5111</menuitemid>
						<label>thelowermiddle-sibling-greatgrandchild1</label>
					</menuitem>
				</menuitem>
				<menuitem>
					<menuitemid>512</menuitemid>
					<label>thelowermiddle-sibling-grandchild2</label>
				</menuitem>
				<menuitem>
					<menuitemid>513</menuitemid>
					<label>thelowermiddle-sibling-grandchild3</label>
				</menuitem>
			</menuitem>
		</menuitem>
		<menuitem>
			<menuitemid>6</menuitemid>
			<label>thelowermiddle-sibling3</label>
		</menuitem>
		<menuitem>
			<menuitemid>foobar</menuitemid>
			<label>foobar-sibling</label>
		</menuitem>
	</menuitem>
</menu>
XML;

$xmlstr_alternate = <<<XML
<menu>
	<menuitem>
		<menuitemid>1</menuitemid>
		<name>jack</name>
		<menuitem>
			<menuitemid>1.1</menuitemid>
			<name>ben</name>
			<menuitem>	
				<menuitemid>1.1.1</menuitemid>
				<name>jane</name>
			</menuitem>
			<menuitem>
				<menuitemid>1.1.2</menuitemid>
				<name>jim</name>
			</menuitem>
			<menuitem>
				<menuitemid>1.1.3</menuitemid>
				<name>jamie</name>
			</menuitem>
		</menuitem>
	</menuitem>
	<menuitem>
		<menuitemid>2</menuitemid>
		<name>justin</name>
		<menuitem>
			<id>2.1</id>
			<name>joan</name>
		</menuitem>
	</menuitem>
</menu>
XML;
				

// ------------------------------------------------------------------
// search tests -----------------------------------------------------
// ------------------------------------------------------------------

include '../utils/utils_xml.php';
include '../utils/utils_error.php';
include '../utils/utils_test.php';

function test_search($utilsxml) {
	$expected_label = 'thelowermiddle-sibling1';
	$test="search tree for specific item - new style";
	
	$result_bool = false;
	$result_str="";
	
	$item = $utilsxml->get_item(4);
	
	assert_strs_equal($item->label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_search_int_as_string($utilsxml) {
	$test="search tree for specific item - int as a string";
	$expected_label = 'thelowermiddle-sibling1';
	
	$result_bool = false;
	$result_str="";
	
	$item = $utilsxml->get_item('4');
	
	assert_strs_equal($item->label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_search_string($utilsxml) {
	$test="search tree for specific item - string";
	$expected_label = 'foobar-sibling';

	$result_bool = false;
	$result_str="";
	
	$item = $utilsxml->get_item('foobar');
	
	assert_strs_equal($item->label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_search_top_item($utilsxml) {
	$test="search tree for top item";
	$expected_label = 'theuppermiddle';
	
	$result_bool = false;
	$result_str="";
	
	$item = $utilsxml->get_item(2);
	
	assert_strs_equal($item->label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

// ------------------------------------------------------------------
// parent tests -----------------------------------------------------
// ------------------------------------------------------------------

function test_parent($utilsxml) {
	$test="get label of parent node";
	$expected_label = 'thelowermiddle';

	$result_bool = false;
	$result_str="";
	
	$item = $utilsxml->get_item(31);
	$parent_label = $utilsxml->get_parent($item)->label;
	
	assert_strs_equal($parent_label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_parent_bad_arg($utilsxml) {
	$test="get label of parent node - bad arg";
	$expected_results = "parameter must be as instance of SimpleXMLElement";

	$result_bool = false;
	$result_str="";
	
	try {
		$parent_label = $utilsxml->get_parent(31)->label;
	} catch (Exception $e) {
		assert_str_contains($expected_results,$e->getMessage(),
										$result_bool,$result_str);
	}
	
	output_results($result_bool,$result_str,$test);
}

// ------------------------------------------------------------------
// item details tests -----------------------------------------------
// ------------------------------------------------------------------

function test_item_details($utilsxml) {
	$test="get all details of node";
	$expected_results = array('tag' => 'foobar','label'=>'thelowermiddle');
	
	$result_bool = false;
	$result_str="";
	
	$item = $utilsxml->get_item(31);
	$details = $utilsxml->get_item_details($item,array('tag'),array('label'));
	
	assert_arrays_equal($details,$expected_results,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);	
}

// ------------------------------------------------------------------
// item depth tests -------------------------------------------------
// ------------------------------------------------------------------

function test_item_depth($utilsxml) {
	
	$test="get depth of node";
	$result = "PASSED:".$test;
	$expected_results = 3;
	$result_bool = false;
	$result_str="";

	$depth = $utilsxml->get_item_depth(41);
	
	assert_ints_equal($depth,$expected_results,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_item_depth_root($utilsxml) {
	
	$test="get depth of node";
	$result = "PASSED:".$test;
	$expected_results = 0;
	$result_bool = false;
	$result_str="";

	$depth = $utilsxml->get_item_depth(1);
	
	assert_ints_equal($depth,$expected_results,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}


// ------------------------------------------------------------------
// ancestor tests ---------------------------------------------------
// ------------------------------------------------------------------

function test_get_ancestor_details($utilsxml) {
	$test="get all ancestors of node from menuid";
	$result = "PASSED:".$test;
	$result_bool = false;
	$result_str="";
	
	$expected_results = array(array('menuitemid'=>4,'label'=>'theuppermiddle'),
									  array('menuitemid'=>2,'label'=>'root'),
									  array('menuitemid'=>1,'label'=>''));

	//$ancestors=$utilsxml->get_ancestors(41);
	
	$ancestor_details = $utilsxml->get_ancestor_details(41, 
															array('menuitemid'),
															array('label'));
	
	assert_arrays_equal($ancestor_details,$expected_results,
								$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);;
}

// ------------------------------------------------------------------
// siblings tests ---------------------------------------------------
// ------------------------------------------------------------------

function test_get_sibling_details($utilsxml) {

	$test="get siblings of node - overide xnode";
	
	$result_bool = false;
	$result_str="";
	
	$expected_results = array(array('menuitemid'=>3,'label'=>'theuppermiddle'),
									  array('menuitemid'=>4,'label'=>'theuppermiddle'),
									  array('menuitemid'=>5,'label'=>'theuppermiddle'),
									  array('menuitemid'=>6,'label'=>'theuppermiddle'),
									  array('menuitemid'=>'foobar','label'=>'theuppermiddle'));

	$sibling_details = $utilsxml->get_sibling_details(3, 
															array('menuitemid'),
															array('label'));
	
	assert_arrays_equal($sibling_details,$expected_results,
								$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_get_sibling_details_arg1_int($utilsxml) {

	$test="get siblings details - bad 1st arg";
	$expected_results = "1st parameter must be integer";
	
	$result_str="";
	$result_bool = false;
	
	try {
		$sibling_details = $utilsxml->get_sibling_details(array("foobar"), 
																array('menuitemid'),
																array('label'));
	} catch (Exception $e) {
		
			assert_str_contains($expected_results,$e->getMessage(),
							$result_bool,$result_str);			
	}

	output_results($result_bool,$result_str,$test);
}

function test_get_sibling_details_arg2_int($utilsxml) {

	$test="get siblings details - bad 2nd arg";
	$expected_results = "parameter must be array";
	
	$result_bool = false;
	$result_str="";
	
	try {
		$sibling_details = $utilsxml->get_sibling_details(3, 
																"foobar",
																array('label'));
	} catch (Exception $e) {
			assert_str_contains($expected_results,$e->getMessage(),
							$result_bool,$result_str);
	}
	
	output_results($result_bool,$result_str,$test);
}	

// ------------------------------------------------------------------
// children tests -------------------------------------------------
// ------------------------------------------------------------------

function test_get_children_details($utilsxml) {
	
	$result_bool = false;
	$result_str="";
	
	$test="get children - new style functions";
	$expected_array = array(array('menuitemid'=>3,'label' => 'theuppermiddle'),
									array('menuitemid'=>4,'label' => 'theuppermiddle'),
									array('menuitemid'=>5,'label' => 'theuppermiddle'),
									array('menuitemid'=>6,'label' => 'theuppermiddle'),
									array('menuitemid'=>'foobar','label' => 'theuppermiddle'));
													
	$child_details = $utilsxml->get_children_details(2, array('menuitemid'),
													array('label'));
	
	assert_arrays_equal($expected_array,$child_details,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);	
}

function test_children_no_child() {
	$test="get children - no child";
	$result = "PASSED:".$test;
	$expected_array = array();
	
	$result_bool = false;
	$result_str="";
	
	//print_r($expected_array);
	
	$child_details = $utilsxml->get_child_details(5111,array('menuitemid'),
												array('label'));
	
	if ($child_details  != $expected_array) {
		$result = "FAILED:".$test;
	}
	echo $result."\n";
}

// ------------------------------------------------------------------
// item tests -------------------------------------------------------
// ------------------------------------------------------------------

function test_item($utilsxml) {
	$test="get item";
	$expected_result = true;

	$result_bool = false;
	$result_str="";
														
	$item = $utilsxml->get_item(5111);
	
	//if (!is_SimpleXMLElement($item) == true) {	}
	
	//print_r($item);	
	assert_true($expected_result,$utilsxml->is_SimpleXMLElement($item),
							$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);	
}

// ------------------------------------------------------------------
// main -------------------------------------------------------------
// ------------------------------------------------------------------

$utilsxml = simplexml_load_string($xmlstr, 'UtilsXML');
$utilsxml->configure('menuitemid',1,'menuitem','menuitemid');

$e = new UtilsError();

set_error_handler('\\UtilsError::error_handler');

/*test_item_depth($utilsxml);
test_item_depth_root($utilsxml);*/

test_item($utilsxml);
test_get_sibling_details_arg1_int($utilsxml);
test_get_sibling_details_arg2_int($utilsxml);
test_get_sibling_details($utilsxml);
test_get_children_details($utilsxml);
test_get_ancestor_details($utilsxml);
test_item_details($utilsxml);
test_parent($utilsxml);
test_parent_bad_arg($utilsxml);
test_search($utilsxml);
test_search_int_as_string($utilsxml);
test_search_string($utilsxml);
test_search_top_item($utilsxml);

?>