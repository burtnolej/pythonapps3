requirejs.config({
    baseUrl: 'js/lib',
    paths: {
       app: '../app'
    }
});

requirejs(['myutils','jquery'],

	function (myutils,$) {
		var ztypes = new Array();
		
		$(document).ready(function(){
			
			// set context menu
			setcontextmenu("ul[class='nav']");
			
			// new button press
			$("input[id='submitfoo']").on('click',function(){
				objtype = $("select[id='objtype").val();
				if (objtype == "lesson") {
					var url = "http://localhost:8080/add/lesson?";
				}
				else {
					var url = "http://localhost:8080/add/"+objtype+"?";
				}
				
				pel = $(this).closest("div");
				pel.find("select").each(function() {
					if (this.id != "source_value") { // ignore source_value select
						url = url + this.name + "=" + this.value + "&";
					}	
				});
				
				pel.find("input").each(function() {
					if (this.id != "submitfoo") { // ignore the submit button
						url = url + this.name + "=" + this.value + "&";
					}
				});
				
				makeRequestResponse(url,alertme);
				
				// reload the page to reflect any added records
	 			setTimeout(function() { 			
			   		pageurl = buildurl();
			   		window.location = pageurl;
	  			},400);	
	  		
	  			$("select[id='objtype").val('NotSelected');
			});
			
			// edit button press
			$("input[id='submitfoo2']").on('click',function(){
					
					id = $("input[id='edit_source_value']").val();
					var url = "http://localhost:8080/update/"+id+"?value_changes=";
					
					pel = $(this).closest("div");				
					var value_changes = getElementValueChanges("select",init_values);
					
					url = url +  value_changes.join(",");
					makeRequestResponse(url,alertme);
				});
				
			// change in new objtype selector
			$("select").on('change',function(){
		   		if ($(this).hasClass("new")) {
		   			var parentel=$(this).closest("div");

					if ($('#tmpdiv').length) {
						$('#tmpdiv').remove();
					}
					
					var tmpdiv = addElement("div","tmpdiv",{hidden:false,parentel:parentel});

		   			if (this.value == "lesson") {
						url = "http://localhost:8080/refdata/all";
						makeRequestResponse(url,drawform_multi,tmpdiv);
						
					}
					else {
						url = "http://localhost:8080/new/"+$(this).value;
						makeRequestResponse(url,drawentryform,tmpdiv);
					}
				}
		 	});
		 	
		   $("select").on('change',function(){
		   		if (!$(this).hasClass("new")) {
		   			pageurl = buildurl();
		   			window.location = pageurl;
		   		}
		   });	  
		});
	}
);