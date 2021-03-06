requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    },
    shim: {
        'myutils': {
            //These script dependencies should be loaded before loading
            //backbone.js
            deps: ['jquery'],
            //Once loaded, use the global 'Backbone' as the
            //module value.
            exports: 'myutils'
        },
	}, waitSeconds: 15,
});
	
//define(['myutils'], function(myutils) {
		
requirejs(['myutils','jquery'],
	function (myutils,$) {

		//$('head').html('<link rel="stylesheet" type="text/css" href="css/select.css" /><link rel="stylesheet" type="text/css" href="css/div.css" /><link rel="stylesheet" type="text/css" href="css/switch.css" /><link rel="stylesheet" type="text/css" href="css/menu.css" />');

		//console.log(getAllInputValues());
		
		var ztypes = new Array();
		var url = "";
		$(document).ready(function(){
		   $("select, input").on('change',function(){
		   	
		   		//url = "http://0.0.0.0/dpivot.php?" + getAllInputValues('ztypes',['qunit-filter-input']);
		   		//url = "http://0.0.0.0/test_dpivot.php?" + getAllInputValues('ztypes',['qunit-filter-input']);
		   		console.log(url);
		    	url = buildurl();
		    	window.location = url;
		   });
		});
	},function (err) {
    //The errback, error callback
    //The error has a list of modules that failed
    var failedId = err.requireModules && err.requireModules[0];
    console.log(failedId);
});



