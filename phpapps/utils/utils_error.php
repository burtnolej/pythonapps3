
<?php
include_once 'utils_utils.php';

class UtilsError {

	function pprint_stack($basename,$funcname,$lineno,$args,$fulltrace,$padstr=" ") {	
		
		printf("%s|%s|%s|%s|%s\n",str_pad($basename,20,$padstr),
									str_pad($funcname,30,$padstr),
									str_pad($lineno,10,$padstr),
									str_pad($args,30,$padstr),"");
									//str_pad($fulltrace,150,$padstr));
	}
	
	function exception_handler($e) {
	
	
		print_r($e);
		echo PHP_EOL.'Exception: ',$e->getMessage(),"\n\n";
		$stack_as_array = explode("\n",$e->getTraceAsString());
		$i=0;
		pprint_stack('basename','funcname','lineno','args','fulltrace');
		pprint_stack('','','','','','-');
		
		foreach ($stack_as_array as $frame) {
			
			// make sure full frame output line
			if (strpos($frame,':') !== false) {
				
					// split frame by colon into 3 vars
					list($fullpath, $rest) = explode(":",substr($frame,3));
					
					// find the start of the args in the non path section
					$open_bracket_posn = strpos($rest,'(');
						
					// put args into an array
					$args_str = substr($rest,$open_bracket_posn+1,-1);
					
					// get the func name 
					$func_name = substr($rest,1,$open_bracket_posn-1);
									
					// get the lineno
					$open_bracket_posn = strpos(basename($fullpath),'(');
					$lineno = substr(basename($fullpath),$open_bracket_posn+1,-1);
					
					// get the source file basename
					$basename = substr(basename($fullpath),0,$open_bracket_posn);
					
					pprint_stack($basename, $func_name, $lineno, $args_str,$frame);
			}
		}
		echo PHP_EOL;	
	}
		

	public static function error_handler($errno, $errstr, $errfile, $errline) {
	
		if (strpos($errstr,'must be of the type array') == true) {
			throw new Exception("parameter must be array");
		}
		elseif (strpos($errstr,'must be an instance of SimpleXMLElement') == true) {
			throw new Exception("parameter must be an instance of SimpleXMLElement");
		}
		else {
			//echo $errstr.PHP_EOL.PHP_EOL;
			
			$stackframes= debug_backtrace();
			
			// process first frame as we know this from the
			$fframe = array_shift($stackframes);
			
			print_r($fframe);
	
			__echoif($fframe,'line');
			__echoif($fframe,'function');
			
			echo $fframe['args'][1].PHP_EOL.PHP_EOL;
			
			//echo $fframe['function'];			
			//echo $fframe['line'];			
			echo $fframe['args'][0];			
			
			$scope="";
			foreach ($fframe['args'][4] as $varname=>$val) {
				if (is_printable($val)) {
					$scope = $scope.$varname.'=>'.$val.",";
				}
				else {
					$scope = $scope.$varname.'=>'.gettype($val).",";
				}
			}
			echo $scope.PHP_EOL;;
			
			foreach ($stackframes as $frame) {
				__echoif($frame,'line');
				__echoif($frame,'function');

				$argstr="(";
				foreach (array_values($frame['args']) as $arg) {
					if (in_array(gettype($arg),array('integer','string'))) {
						$argstr = $argstr.$arg;
					}
					else {
						$argstr = $argstr.gettype($arg);
					}
				}
				$argstr = $argstr.")";
				echo $argstr.PHP_EOL;
			}
			
			trigger_error("Fatal error", E_USER_ERROR);
		}
	}
}


?>