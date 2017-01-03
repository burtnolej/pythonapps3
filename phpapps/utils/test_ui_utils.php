<?php

$PHPLIBPATH = getenv("PHPLIBPATH");

if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

set_include_path($PHPLIBPATH);
require_once 'autoload.php';

include_once 'ui_utils.php';
include_once 'utils_error.php';
include_once 'utils_utils.php';

set_error_handler('\\UtilsError::error_handler');

class test_gethtmldropdown extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
		
		ob_start(); 
		
		$this->expected_result = '<label for="foobar" >foobar</label><input type="text" name="foobar" id="foobar" list="suggestions0"><datalist id="suggestions0"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></datalist>';
				
		$_result = gethtmldropdown($column,$values,$widgetcount);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_default()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
	 	$default=3;
	 	
		ob_start(); 
		
		$this->expected_result = '<label for="foobar" >foobar</label><input type="text" name="foobar" id="foobar" list="suggestions0" value="3"><datalist id="suggestions0"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></datalist>';
						
		$_result = gethtmldropdown($column,$values,$widgetcount,$default);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
}

class test_gethtmldbdropdown extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$dbname = "test_gethtmldbdropdown.sqlite";
		$tablename = "lesson";

		ob_start(); 
		
		$this->expected_result = '<div class="container"><label for="subject" >subject</label><input type="text" name="subject" id="subject" list="suggestions0"><datalist id="suggestions0"><option>Math</option><option>ELA</option><option>Engineering</option></datalist></div>';
						
		gethtmldbdropdown($dbname,$tablename);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmlbutton extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$type = "submit";
		$label = "go";

		ob_start(); 
		
		$this->expected_result = '<input type="submit" name="submit" value="go" />';
								
		gethtmlbutton($type,$label);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmlxmldropdown extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$xml = "<root>
		          <dropdown id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values></dropdown>
		          <dropdown id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		          </dropdown>
		        </root>";

		ob_start(); 
		
		$this->expected_result = '<div class="container"><label for="xaxis" >xaxis</label><input type="text" name="xaxis" id="xaxis" list="suggestions0"><datalist id="suggestions0"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div><div class="container"><label for="yaxis" >yaxis</label><input type="text" name="yaxis" id="yaxis" list="suggestions1"><datalist id="suggestions1"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div>';
										
		gethtmlxmldropdown($xml);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_default()
	{
		$xml = "<root>
		          <dropdown id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <default>dow</default>
		           </dropdown>
		            
		          <dropdown id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <default>subject</default>
		          </dropdown>
		        </root>";

		ob_start(); 
		
		$this->expected_result = '<div class="container"><label for="xaxis" >xaxis</label><input type="text" name="xaxis" id="xaxis" list="suggestions0" value="dow"><datalist id="suggestions0"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div><div class="container"><label for="yaxis" >yaxis</label><input type="text" name="yaxis" id="yaxis" list="suggestions1" value="subject"><datalist id="suggestions1"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div>';
												
		gethtmlxmldropdown($xml);
					
		$result = ob_get_contents();
		ob_end_clean();
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmlmultiselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$dbname = "test_gethtmlmultiselect.sqlite";
		$query = "select name from sqlite_master";
		$name = "ingredients";

		ob_start(); 
		
		$this->expected_result = '<table><tr><td><input id="adult" type="checkbox" name="ingredients[]" value="adult"/><label for="adult" >adult</label></td></tr><tr><td><input id="student" type="checkbox" name="ingredients[]" value="student"/><label for="student" >student</label></td></tr><tr><td><input id="period" type="checkbox" name="ingredients[]" value="period"/><label for="period" >period</label></td></tr><tr><td><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label></td></tr><tr><td><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label></td></tr><tr><td><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label></td></tr><tr><td><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label></td></tr><tr><td><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label></td></tr><tr><td><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label></td></tr><tr><td><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label></td></tr></table>';				
		getdbhtmlmultiselect($dbname,$query,$name);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_maxy3()
	{
		$dbname = "test_gethtmlmultiselect.sqlite";
		$query = "select name from sqlite_master";
		$name = "ingredients";

		ob_start(); 
		
		$this->expected_result = '<table><tr><td><input id="adult" type="checkbox" name="ingredients[]" value="adult"/><label for="adult" >adult</label></td><td><input id="student" type="checkbox" name="ingredients[]" value="student"/><label for="student" >student</label></td><td><input id="period" type="checkbox" name="ingredients[]" value="period"/><label for="period" >period</label></td></tr><tr><td><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label></td><td><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label></td><td><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label></td></tr><tr><td><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label></td><td><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label></td><td><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label></td></tr><tr><td><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label></td></tr></table>';
																
		getdbhtmlmultiselect($dbname,$query,$name,2);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_default()
	{
		$dbname = "test_gethtmlmultiselect.sqlite";
		$query = "select name from sqlite_master";
		$name = "ingredients";

		$checked = array('adult','student','period');
		ob_start();
		
		$this->expected_result = '<table><tr><td><input id="adult" type="checkbox" name="ingredients[]" value="adult"checked/><label for="adult" >adult</label></td></tr><tr><td><input id="student" type="checkbox" name="ingredients[]" value="student"checked/><label for="student" >student</label></td></tr><tr><td><input id="period" type="checkbox" name="ingredients[]" value="period"checked/><label for="period" >period</label></td></tr><tr><td><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label></td></tr><tr><td><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label></td></tr><tr><td><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label></td></tr><tr><td><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label></td></tr><tr><td><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label></td></tr><tr><td><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label></td></tr><tr><td><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label></td></tr></table>';
																		
		getdbhtmlmultiselect($dbname,$query,$name,0,$checked);
				
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_default_row5()
	{
		$dbname = "test_gethtmlmultiselect.sqlite";
		$query = "select name from sqlite_master";
		$name = "ingredients";

		$checked = array('adult','student','period');
		ob_start();
		
		$this->expected_result = '<table><tr><td><input id="adult" type="checkbox" name="ingredients[]" value="adult"checked/><label for="adult" >adult</label></td><td><input id="student" type="checkbox" name="ingredients[]" value="student"checked/><label for="student" >student</label></td><td><input id="period" type="checkbox" name="ingredients[]" value="period"checked/><label for="period" >period</label></td><td><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label></td><td><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label></td><td><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label></td></tr><tr><td><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label></td><td><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label></td><td><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label></td><td><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label></td></tr></table>';
																				
		getdbhtmlmultiselect($dbname,$query,$name,5,$checked);
				
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmlselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
		
		ob_start(); 
		
		$this->expected_result = '<span ><select id="foobar" name="foobar"><option value="1">1</option><option value="2"selected>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option></select></span>';
						
		$_result = gethtmlselect($column,$values,$widgetcount,2);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_label()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
		
		ob_start(); 
		
		$this->expected_result = '<span ><label for=number>number</label><select id="foobar" name="foobar"><option value="1">1</option><option value="2"selected>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option></select></span>';
								
		$_result = gethtmlselect($column,$values,$widgetcount,2,"number");
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_class()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
		
		ob_start(); 
		
		$this->expected_result = '<span class ="class1"><select class ="class2" id="foobar" name="foobar"><option value="1">1</option><option value="2"selected>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option></select></span>';
										
		$_result = gethtmlselect($column,$values,$widgetcount,2,NULL,NULL,"class1","class2");
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
}

class test_gethtmlxmlselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$xml = "<root>
		          <select id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values></select>
		          <select id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		          </select>
		        </root>";

		ob_start(); 
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		$this->expected_result = '<span ><select id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><br><br><span ><select id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><br><br>';
												
		gethtmlxmlselect($xml,$defaults);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_labels()
	{
		$xml = "<root>
		          <select id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values></select>
		          <select id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		          </select>
		        </root>";

		ob_start(); 
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		$this->expected_result = '<span ><label for=xaxis>xaxis</label><select id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><br><br><span ><label for=yaxis>yaxis</label><select id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><br><br>';
														
		gethtmlxmlselect($xml,$defaults,TRUE);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_class()
	{
		$xml = "<root>
		          <select id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values></select>
		          <select id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		          </select>
		        </root>";

		ob_start(); 
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		$this->expected_result = '<span class ="class1"><select class ="class2" id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><br><br><span class ="class1"><select class ="class2" id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><br><br>';
														
		gethtmlxmlselect($xml,$defaults,FALSE,FALSE,"class1","class2");
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmllabel extends PHPUnit_Framework_TestCase
{
	public function test_()
	{

		$label = "foobar";
		ob_start(); 
		
		$this->expected_result = '<label for=foobar>foobar</label>';
										
		gethtmllabel($label);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmlswitch extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		//ob_start(); 
		
		$this->expected_result = '<link rel="stylesheet" type="text/css" href="switch.css" /><label class="switch"><input id="foobar" type="checkbox" name="foobar"><div class="slider"></div></label>';
												
		gethtmlswitch("foobar","foobar");
					
		//$result = ob_get_contents();
		//ob_end_clean();		
		//$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_checked()
	{
		ob_start(); 
		
		$this->expected_result = '<link rel="stylesheet" type="text/css" href="switch.css" /><label class="switch"><input id="foobar" type="checkbox" name="foobar"checked><div class="slider"></div></label>';														
		gethtmlswitch("foobar","foobar",array("foobar"));
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_getchtmlselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
	
		$this->expected_result = '<p class="label">foobar</p><span class="select"><select class="custom" id="foobar" name="foobar"><option value="foobar">foobar</option><option value="barfoo"selected>barfoo</option></select></span><span class="comment"><p>blah blah blah blah blah blah blah blah blah blah blah blah blah blah</p></span>';
						
		ob_start(); 
		
		$values = array("foobar","barfoo");
		getchtmlselect("foobar",$values,1,"barfoo",array('comment' => 'blah blah blah blah blah blah blah blah blah blah blah blah blah blah'));
		
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_label()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
	
		$this->expected_result = '<p class="label">vardy</p><span class="select"><select class="custom" id="foobar" name="foobar"><option value="foobar">foobar</option><option value="barfoo"selected>barfoo</option></select></span><span class="comment"><p>blah blah blah blah blah blah blah blah blah blah blah blah blah blah</p></span>';
								
		ob_start(); 
		
		$values = array("foobar","barfoo");
		getchtmlselect("foobar",$values,1,"barfoo",array('label' => 'vardy','comment' => 'blah blah blah blah blah blah blah blah blah blah blah blah blah blah'));
		
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_getxmlchtmlselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
	
		$xml = "<root>
		          <select id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <comment>foobar foobar foobar</comment>
		            </select>
		            
		          <select id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <comment>barfoo barfoo barfoo</comment>
		          </select>
		        </root>";
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		
		$this->expected_result = '<div class="contain"><p class="divlabel">this is a div label</p><p class="label">xaxis</p><span class="select"><select class="custom" id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><span class="comment"><p>foobar foobar foobar</p></span><p class="label">yaxis</p><span class="select"><select class="custom" id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><span class="comment"><p>barfoo barfoo barfoo</p></span></div>';
										
		ob_start(); 

		getxmlhtmlcselect($xml,$defaults,'this is a div label');

		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_starttag()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
	
		$xml = "<root>
					<foobar>
		          <select id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <comment>foobar foobar foobar</comment>
		            </select>
		            
		          <select id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <comment>barfoo barfoo barfoo</comment>
		          </select>
		          </foobar>
		          <random>
		          	<random>
		          	</random>
		          </random>
		        </root>";
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		
		$this->expected_result = '<div class="contain"><p class="divlabel">this is a div label</p><p class="label">xaxis</p><span class="select"><select class="custom" id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><span class="comment"><p>foobar foobar foobar</p></span><p class="label">yaxis</p><span class="select"><select class="custom" id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><span class="comment"><p>barfoo barfoo barfoo</p></span></div>';
		ob_start(); 

		getxmlhtmlcselect($xml,$defaults,'this is a div label','foobar');

		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_starttag2() {
		
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		
		$xml = " <root>
			<dpivot>
				<select id='1'>
				<field>xaxis</field>
				<values>
		      		<value>period</value>
				</values>
				</select>
			</dpivot>
			<dsearch>
				<select id='1'>
				<field>yaxis</field>
				<values>
		      		<value>pooppoo</value>
				</values>
				</select>
			</dsearch>
			</root>";
			
		$defaults = array();
		
		$this->expected_result = '<div class="contain"><p class="divlabel">this is a div label</p><p class="label">xaxis</p><span class="select"><select class="custom" id="xaxis" name="xaxis"><option value="period">period</option></select></span></div>';
		ob_start(); 

		getxmlhtmlcselect($xml,$defaults,'this is a div label','dpivot');

		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_label()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
	
		$xml = "<root>
					<foobar>
		          <select id='1'>
		            <field>xaxis</field>
		            <label>row header</label>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <comment>foobar foobar foobar</comment>
		            </select>
		            
		          <select id='2'>
		            <field>yaxis</field>
		            <label>column header</label>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <comment>barfoo barfoo barfoo</comment>
		          </select>
		          </foobar>
		          <random>
		          	<random>
		          	</random>
		          </random>
		        </root>";
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		
		$this->expected_result = '<div class="contain"><p class="divlabel">this is a div label</p><p class="label">row header</p><span class="select"><select class="custom" id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><span class="comment"><p>foobar foobar foobar</p></span><p class="label">column header</p><span class="select"><select class="custom" id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><span class="comment"><p>barfoo barfoo barfoo</p></span></div>';
		ob_start(); 

		getxmlhtmlcselect($xml,$defaults,'this is a div label','foobar');

		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_getchtmldbselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		
		$dbname = "test_getchtmldbselect.sqlite";
		$column = "name";
		$name = "foobar";
		$tablename="dow";
		
		ob_start(); 
		
		$this->expected_result = '<div class="contain"><p class="divlabel">divlabel</p><p class="label">foobar</p><span class="select"><select class="custom" id="foobar" name="foobar"><option value="NotSelected">NotSelected</option><option value="all">all</option><option value="Monday">Monday</option><option value="Tuesday"selected>Tuesday</option><option value="Thursday">Thursday</option><option value="Wednesday">Wednesday</option><option value="Friday">Friday</option></select></span><span class="comment"><p>another comment</p></span></div>';
															
		$args = array('comment'=>'another comment','divlabel' => 'divlabel');						
		getchtmldbselect($dbname,$tablename,$column,$name,1,'Tuesday',$args);
							
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_label_novalues_directive()
	{
		/* early version with no directive for how to get option values */
		
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		
		$dbname = "test_getchtmldbselect.sqlite";
		$column = "name";
		$name = "foobar";
		$tablename="dow";
		
		ob_start(); 
		
		$this->expected_result = '<div class="contain"><p class="divlabel">divlabel</p><p class="label">dsfdf</p><span class="select"><select class="custom" id="foobar" name="foobar"><option value="NotSelected">NotSelected</option><option value="all">all</option><option value="Monday">Monday</option><option value="Tuesday"selected>Tuesday</option><option value="Thursday">Thursday</option><option value="Wednesday">Wednesday</option><option value="Friday">Friday</option></select></span><span class="comment"><p>another comment</p></span></div>';
															
		$args = array('comment'=>'another comment','divlabel' => 'divlabel','label' => 'dsfdf');						
		getchtmldbselect($dbname,$tablename,$column,$name,1,'Tuesday',$args);
							
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_label_distinct()
	{
		/*supports directive for values but using distinct values of main record table (like lesson)*/
		
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		
		$dbname = "test_getchtmldbselect.sqlite";
		$column = "name";
		$name = "foobar";
		$tablename="dow";
		
		ob_start(); 
		
		$this->expected_result = '<div class="contain"><p class="divlabel">divlabel</p><p class="label">dsfdf</p><span class="select"><select class="custom" id="foobar" name="foobar"><option value="NotSelected">NotSelected</option><option value="all">all</option><option value="Monday">Monday</option><option value="Tuesday"selected>Tuesday</option><option value="Thursday">Thursday</option><option value="Wednesday">Wednesday</option><option value="Friday">Friday</option></select></span><span class="comment"><p>another comment</p></span></div>';
															
		$args = array('comment'=>'another comment','divlabel' => 'divlabel','label' => 'dsfdf','distinct' => true);						
		getchtmldbselect($dbname,$tablename,$column,$name,1,'Tuesday',$args);
							
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_tablevalues()
	{
		/*supports directive for values and uses values in specific tables (like period) */
				
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		
		$dbname = "test_getchtmldbselect.sqlite";
		$column = "period";
		$name = "foobar";
		$tablename="dow";
		
		ob_start(); 
		
		$this->expected_result = '<div class="contain"><p class="divlabel">divlabel</p><p class="label">dsfdf</p><span class="select"><select class="custom" id="foobar" name="foobar"><option value="NotSelected">NotSelected</option><option value="all">all</option><option value="830-910">830-910</option><option value="910-950">910-950</option><option value="950-1030">950-1030</option><option value="1030-1110">1030-1110</option><option value="1110-1210">1110-1210</option><option value="1210-100">1210-100</option><option value="100-140">100-140</option><option value="140-220">140-220</option><option value="220-300">220-300</option><option value="300-330">300-330</option></select></span><span class="comment"><p>another comment</p></span></div>';
															
		$args = array('comment'=>'another comment','divlabel' => 'divlabel','label' => 'dsfdf','distinct' => false);						
		getchtmldbselect($dbname,$tablename,$column,$name,1,'Tuesday',$args);
							
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}	
}

class test_getchtmlswitch extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/switch.css\" />";
		
		ob_start(); 
		$this->expected_result = '<p class="label switch">foobar</p><label class="switch"><input id="foobar" type="checkbox" name="foobar"><p class="slider"></p></label>';
																	
		getchtmlswitch("foobar","foobar");
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_checked()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/switch.css\" />";
		
		ob_start(); 
		
		$this->expected_result = '<p class="label switch">foobar</p><label class="switch"><input id="foobar" type="checkbox" name="foobar"checked><p class="slider"></p></label>';
		getchtmlswitch("foobar","foobar",array("foobar"));
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_multi()
	{
		
		echo "<!DOCTYPE html>";
		echo "<html>";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/switch.css\" />";
		
		//ob_start(); 
		$this->expected_result = '<p class="label switch">foobar</p><label class="switch"><input id="foobar" type="checkbox" name="foobar"><p class="slider"></p></label>';
																	
		getchtmlswitch("foobar","foobar");
		getchtmlswitch("foobar2","foobar3");
		getchtmlswitch("foobar2","foobar3");
					
		//$result = ob_get_contents();
		//ob_end_clean();		
		//$this->assertEquals($result,$this->expected_result);
	}
}

class test_getchtmlxmlmenu extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
	   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/menu.css\" />";
	    
	   ob_start();
	   
		$xml = "<root>
		          <item name='view'>
		          	<item name='by student'>
		          		<link>foobar.php</link>
		          	</item>
		          	<item name='by adult'>
		          		<link>barfoo.php</link>
		          	</item>
		          </item>
		         </root>";	 
		         
		 $this->expected_result = '<div id="wrap"><ul class = "nav"><li>view<ul><li><a href="foobar.php">by student</a></li><li><a href="barfoo.php">by adult</a></li></ul></ul></div>';
		 		         
		 getchtmlxmlmenu2($xml,"foobar");   
		 
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);     
	}

	public function test_multilevel()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
	   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/menu.css\" />";
	    
	   ob_start();
	   
		$xml = "<root>
		          <item name='view'>
		          	<item name='by student'>
		          		<link>foobar.php</link>
		          	</item>
		          	<item name='by adult'>
		          		<link>barfoo.php</link>
		         		    	<item name='ana'>
		          				<link>barfoo.php</link>
		          			</item>
		         		    	<item name='patrick'>
		          				<link>barfoo.php</link>
		          			</item>
		         		    	<item name='diana'>
		          				<link>barfoo.php</link>
		          				<item name='option1'>
		          					<link>barfoo.php</link>
		          				</item>
		          				<item name='option2'>
		          					<link>barfoo.php</link>
		          				</item>
		          			</item>
		          	</item>
		          </item>
		         </root>";	 
		         
		$this->expected_result = '<div id="wrap"><ul class = "nav"><li>view<ul><li><a href="foobar.php">by student</a></li><li><a href="barfoo.php">by adult</a><ul><li></li><li><a href="barfoo.php">ana</a></li><li><a href="barfoo.php">patrick</a></li><li><a href="barfoo.php">diana</a><ul><li></li><li><a href="barfoo.php">option1</a></li><li><a href="barfoo.php">option2</a></li></ul></ul></ul></ul></div>';
		 		 		         
		 getchtmlxmlmenu2($xml,"foobar");   
		 
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);     
	}
	
	public function test_linkcomponent(){
	
		echo "<!DOCTYPE html>";
		echo "<html>";
	   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/menu.css\" />";
	    
	   ob_start();
		$xml =  "<root>					
		<item name='by student'>
			<item name='Booker'>
				<link>
					<ip>192.168.1.254</ip>
					<target>dpivot.php</target>
					<flags>
			        	<xaxis>period</xaxis>
			        	<yaxis>dow</yaxis>
			       	<source_type>student</source_type>
			       	<source>56newworkp</source>
			       	<source_value>Booker</source_value>
						<cnstr_subject>NotSelected</cnstr_subject>
						<cnstr_dow>NotSelected</cnstr_dow>
						<cnstr_period>NotSelected</cnstr_period>
						<cnstr_student>NotSelected</cnstr_student>
						<cnstr_adult>NotSelected</cnstr_adult>
						<cnstr_prep>NotSelected</cnstr_prep>
						<formats>on</formats>
						<rollup>on</rollup>
						<status>on</status>
						<student>on</student>
						<ztypes>subject,adult</ztypes>
					</flags>
				</link>
			</item>
		</item>
	</root>";

		$this->expected_result ='<div id="wrap"><ul class = "nav"><li>by student<ul><li><a href="http://192.168.1.254//?xaxis=period&yaxis=dow&source_type=student&source=56newworkp&source_value=Booker&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Booker</a></li></ul></ul></div>';
				 		 		         
		 getchtmlxmlmenu2($xml,"foobar");   
		 
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);     
	}
	
	public function test_build_menu_xml2() {

		$xml = build_menu_xml(['Booker','Peter','Clayton'],'foobar','localhost','dpivot.php');
		
		$expected_result = '<div id="wrap"><ul class = "nav"><li>foobar<ul><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=dow&source_type=student&source=56newworkp&source_value=Booker&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Booker</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=dow&source_type=student&source=56newworkp&source_value=Peter&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Peter</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=dow&source_type=student&source=56newworkp&source_value=Clayton&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Clayton</a></li></ul></ul></div>';
		
		ob_start();
			   
		getchtmlxmlmenu2($xml,'foobar');
		
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$expected_result);  
	}
	
	public function test_build_dbmenu_xml() {
		
		echo "<!DOCTYPE html>";
		echo "<html>";
	   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/menu.css\" />";
	   
	   $expected_result = '<div id="wrap"><ul class = "nav"><li>foobar<ul><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Nathaniel&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Nathaniel</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Clayton&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Clayton</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Bruno&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Bruno</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Orig&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Orig</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Stephen&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Stephen</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Oscar&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Oscar</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Peter&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Peter</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Jack&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Jack</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Jake&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Jake</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Coby&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Coby</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Thomas&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Thomas</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Yosef&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Yosef</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Tristan&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Tristan</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Ashley&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Ashley</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Simon A&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Simon A</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Booker&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Booker</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=OmerC&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">OmerC</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Asher&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Asher</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Shane&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Shane</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Simon B&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Simon B</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Mackenzie&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Mackenzie</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Nick&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Nick</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Lucy&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Lucy</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Liam&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Liam</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Donovan&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Donovan</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Luke&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Luke</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Tris&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Tris</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Prep 4&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Prep 4</a></li></ul></ul></div>';
	   
		$xml = build_dbmenu_xml('test_getdbmenuxml.sqlite','student','name');
		
		ob_start();
		
		getchtmlxmlmenu2($xml,'foobar');
		
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$expected_result);  
	}	
	
	public function test_append_menu_xml() {
		/* append a db menu to an existing menu node */
		
		$_xml = "<root><item name='view'><item name='by student'><item name='perioddow'></item></item></item></root>";	   		
		$_xmlinsert = "<root><item name='foobar'><value>dsdasdd</value></item></root>";	   
		$expected_result = '<div id="wrap"><ul class = "nav"><li>view<ul><li>by student<ul><li>perioddow<ul><li>foobar</li></ul></ul></ul></ul></div>';
				 		 		         
		echo "<!DOCTYPE html>";
		echo "<html>";
	   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/menu.css\" />";
	   	
		$xmlinsert = simplexml_load_string($_xmlinsert,'utils_xml');
		$xml = simplexml_load_string($_xml,'utils_xml');
		
		$item =  $xml->get_item("perioddow","item","@name");	
		append_xml($xmlinsert,$item);
		
		ob_start();
		getchtmlxmlmenu2($xml->asXML(),'foobar');
		
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$expected_result);  
		
	}	

	public function test_append_dbmenu_xml() {
		/* append a db menu to an existing menu node */
		
		$xml = "<root><item name='view'><item name='by student'><item name='period-dow'></item></item></item></root>";	 
		         
		$this->expected_result = '';
				 		 		         
		echo "<!DOCTYPE html>";
		echo "<html>";
	   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/menu.css\" />";
	   	 		
		$expected_result = '<div id="wrap"><ul class = "nav"><li>view<ul><li>by student<ul><li>period-dow<ul><li>foobar<ul><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Nathaniel&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Nathaniel</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Clayton&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Clayton</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Bruno&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Bruno</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Orig&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Orig</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Stephen&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Stephen</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Oscar&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Oscar</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Peter&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Peter</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Jack&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Jack</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Jake&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Jake</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Coby&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Coby</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Thomas&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Thomas</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Yosef&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Yosef</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Tristan&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Tristan</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Ashley&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Ashley</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Simon A&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Simon A</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Booker&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Booker</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=OmerC&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">OmerC</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Asher&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Asher</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Shane&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Shane</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Simon B&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Simon B</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Mackenzie&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Mackenzie</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Nick&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Nick</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Lucy&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Lucy</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Liam&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Liam</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Donovan&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Donovan</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Luke&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Luke</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Tris&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Tris</a></li><li><a href="http://localhost//dpivot.php?xaxis=period&yaxis=adult&source_type=student&source=56newworkp&source_value=Prep 4&cnstr_subject=NotSelected&cnstr_dow=NotSelected&cnstr_period=NotSelected&cnstr_student=NotSelected&cnstr_adult=NotSelected&cnstr_prep=NotSelected&formats=on&rollup=on&status=on&student=on&ztypes=subject,adult&">Prep 4</a></li></ul></ul></ul></ul></ul></div>';
		
		$_insertxml = build_dbmenu_xml('test_getdbmenuxml.sqlite','student','name');
		$insertxml = simplexml_load_string($_insertxml,'utils_xml');
		$targetxml = simplexml_load_string($xml,'utils_xml');
		
		$item =  $targetxml->get_item("period-dow","item","@name");	
		append_xml($insertxml,$item);
		ob_start();
		getchtmlxmlmenu2($targetxml->asXML(),'foobar');
		
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$expected_result);  
	}	
	
}

class test_getchtmlinput extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		echo "<!DOCTYPE html>";
		echo "<html>";
	   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
	   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/input.css\" />";
	    
	   ob_start();
	   		         
		$this->expected_result = '<p class="label">doofar</p><input class = "custom" type="text" id="foobar" value="barfoo" /><p class="comment">a comment</p>';
				 		 		         
		getchtmlinput("doofar","foobar","barfoo","a comment");   
		 
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);     
	}
}

class test_getxmlchtmlinput extends PHPUnit_Framework_TestCase 
{
	public function test_()
		{
			echo "<!DOCTYPE html>";
			echo "<html>";
			echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/select.css\" />";
		   echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/input.css\" />";
			echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"css/div.css\" />";
		
			$xml = "<root>
								<foobar>
				          		<input id='1'>
				            			<field>xaxis</field>
				             		<label>period</label>
				             		<comment>blah blah blah</comment>
				           		</input>
				          		<input id='2'>
				            			<field>yaxis</field>
				             		<label>dow</label>
				             		<comment>blah blah blah</comment>
				           		</input>
			           		</foobar>
			        		</root>";
			
			$defaults = array("xaxis" => "adult", "yaxis" => "dow");
			
			$this->expected_result = '<div class="contain"><p class="divlabel">this is a div label</p><p class="label">period</p><input class = "custom" type="text" id="xaxis" value="adult" /><p class="comment">blah blah blah</p><p class="label">dow</p><input class = "custom" type="text" id="yaxis" value="dow" /><p class="comment">blah blah blah</p></div>';
			ob_start(); 
	
			getxmlhtmlinput($xml,$defaults,'this is a div label',"foobar");
	
			$result = ob_get_contents();
			ob_end_clean();		
			$this->assertEquals($result,$this->expected_result);	
	}
}
			       

/*
$stf = new test_gethtmldropdown();
$stf->test_();
$stf->test_default();

$stf = new test_gethtmldbdropdown();
$stf->test_();

$stf = new test_gethtmlxmldropdown();
$stf->test_();
$stf->test_default();

$stf = new test_gethtmlbutton();
$stf->test_();

$stf = new test_gethtmlmultiselect();
$stf->test_();
$stf->test_default();
$stf->test_maxy3();
$stf->test_default_row5();

$test = new test_gethtmlselect();
$test->test_();
$test->test_label();
$test->test_class();

$test = new test_gethtmlxmlselect();
$test->test_();
$test->test_labels();
$test->test_class();

$test = new test_gethtmllabel();
$test->test_();

$test = new test_gethtmlswitch();
$test->test_();
$test->test_checked();

$test = new test_getchtmlselect();
$test->test_();
$test->test_label();

$test = new test_getxmlchtmlselect();
$test->test_();
$test->test_starttag();
$test->test_starttag2();
$test->test_label();*/


$test = new test_getchtmldbselect();
//$test->test_();
//$test->test_label_novalues_directive();
//$test->test_label_distinct();
$test->test_tablevalues();



/*
$test = new test_getchtmlswitch();
$test->test_();
$test->test_multi();
$test->test_checked();


$test = new test_getchtmlxmlmenu();
$test->test_();
$test->test_multilevel();
$test->test_linkcomponent();
$test->test_build_menu_xml2();
$test->test_build_dbmenu_xml();
$test->test_append_menu_xml();
$test->test_append_dbmenu_xml();


$test = new test_getchtmlinput();
$test->test_();

$test = new test_getxmlchtmlinput();
$test->test_();
*/
?>