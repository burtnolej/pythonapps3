$(document).ready(function() {
  $('select,input').on('change', function() {
    var rval = $( "#rinput" ).val();
    var gval = $( "#ginput" ).val();
    var bval = $( "#binput" ).val();
    
    var rgb = "rgb(" +rval.toString(16)+","+gval.toString(16)+","+bval.toString(16)+")";
    	
	var selected = $("input[type='radio'][name='colortype']:checked");
    	console.log(selected.val());
    	
    	//console.log($("#colortype" ).checked());
      if (selected.val() == "font") {
      		$( "#output" ).css("color",rgb);
      }
      else {
      		$( "#output" ).css("background-color",rgb);
      } 
    //});
  });
});
