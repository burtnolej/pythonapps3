

/*

isarray(obj)
compare_1darrays(arr1, arr2) 
pp(obj)
 _addElement(html_arr,hidden,parentelement,placement='bottom')
  addElement(element_type,id,options)
myTimer()
getElementValues(type)
getElementsName(type)
getElementsIds(type)
getElementValueChanges(elementtype,initvalues)
delElement(id)
makeRequest(url,alert_contents) 
writeHttpResponse()
writeHttpServiceStatus()
geturl()  */

function isarray(obj) {
  /* returns true if the passed object is an array */
  if (Object.prototype.toString.call(obj) === '[object Array]') {
    return true;
  }
  return false;
}
function compare_1darrays(arr1, arr2) {
  /* both arguments must be 1d arrays; returns 0 if identical or 
		returns an array with the indexes of the elements that are different
		in it */
  if (!isarray(arr1) || !isarray(arr2)) {
    throw ('both arguments need to be of type array')
  } 
  else if (arr1.length != arr2.length) {
    throw ('arrays are different lengths')
  } 
  else {
    var diffs = Array();
    for (i = 0; i < arr1.length; i++) {
      if (arr1[i] != arr2[i]) {
        diffs.push(i);
      }
    }
    if (diffs.length != 0) {
      return diffs
    }
  }
  return 0
}

function pp(obj) {
  /* return a string represenation of an object*/
  return JSON.stringify(obj);
}

function _addElement(html_arr,hidden,parentelement,placement='bottom') {
	var div= document.createElement('div');

	if (hidden) { html_arr.splice(2,0," hidden ") }
	
	html_str =html_arr.join("");
	
	div.innerHTML= html_str;
	var el= div.firstChild;
	
	if (placement=="bottom") {
		parentelement.appendChild(el);   
	}
	else {
		parentelement.insertBefore(el,parentelement.firstChild);   
	}
	
	return el;
}

function addElement(element_type,id,options) {

	/*var options = {
		//label:null;
		//name:null;
		hidden:false
		//subtype=null;
		//default=null;
		//classs=null;
		//parentid=null;
	};*/
		
	var html_arr = Array();
	var hidden = options.hidden;
	delete options['hidden'];
	
	html_arr.push('<');
	html_arr.push(element_type);
	
	/*for (var property in options) {
		if (options.hasOwnProperty(property)) {
			if (options[property] != null) {
				html_arr.push(' '+property+'="');html_arr.push(options[property]);html_arr.push('"');
			}
	    }
	}*/

	if (options.href != null) {
		html_arr.push(' href="');html_arr.push(options.href);html_arr.push('"');
	}
	
	if (options.subtype != null) {
		html_arr.push(' type="');html_arr.push(options.subtype);html_arr.push('"');
	}
	
	if (options.default != null) {
		html_arr.push(' value="');html_arr.push(options.default);html_arr.push('"');
	}
	
	if (options.class != null) {
		html_arr.push(' class="');html_arr.push(options.class);html_arr.push('"');
	}
	
	if (options.name != null) {
		html_arr.push(' name="');html_arr.push(options.name);html_arr.push('"');
	}
	
	html_arr.push(' id="');
	html_arr.push(id);
	html_arr.push('"');
	
	html_arr.push('>');
	
	if (options.label != null) {
		html_arr.push(options.label);	
	}
	
	if (options.options != null) {
		for (i = 0; i < options.options.length; i++) {
			html_arr.push('<option>');
			html_arr.push(options.options[i]);
			html_arr.push('</option>');
		}
	}
	
	html_arr.push('</');
	html_arr.push(element_type);
	html_arr.push('>');
	
	if (options.parentid == null) {
		parentelement = document.body;
	}
	else {
		parentelement = document.getElementById(options.parentid);
	}
	
	return _addElement(html_arr,hidden,parentelement,options.placement);
}

function myTimer() {
    var d = new Date();
    document.getElementById("time").innerHTML = d.toLocaleTimeString();
    makeRequest("http://0.0.0.0:8080/command/ping",writeHttpServiceStatus);
}

function getElementValues(type) {
	var values = Array();
	$(type).each(function (index, value) {
   		values.push(this.value);
	});
	return values;
}

function getElementsName(type) {
	var values = Array();
	$(type).each(function (index, name) {
   		values.push(this.name);
	});
	return values;
}

function getElementsIds(type) {
	var values = Array();
	$(type).each(function (index, id) {
   		values.push(this.id);
	});
	return values;
}

function getElementValueChanges(elementtype,initvalues) {
	newvalues = getElementValues(elementtype);
	diffvalues = compare_1darrays(initvalues,newvalues);
	ids = getElementsIds(elementtype);
	result = Array();

	for (i=0;i<diffvalues.length;i++) {
		result.push(ids[diffvalues[i]]);
		result.push(newvalues[diffvalues[i]]);
	}
	
	return result;
}

function delElement(id) {
	/* seems to be easier to write to the DOM via jscript functions rather than jquery */	
	el = document.getElementById(id);
	document.getElementById(id).parentElement.removeChild(el);
	
}

function makeRequest(url,alert_contents) {
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
      alert('Giving up :( Cannot create an XMLHTTP instance');
      return false;
    }
    httpRequest.onreadystatechange = alert_contents;
    httpRequest.open('GET', url,true);
    httpRequest.send();
    
	element = document.getElementById("history")

    var linkid = new Date().getTime();

	var options = {
		hidden:false,
		href: url
	};
	
	options.name = "foobar";
	options.label = linkid;
	options.parentid = "history";
	options.placement = "top";

	_addElement(Array("<br>"),false,document.getElementById("history"),'top');
	addElement("a",linkid,options);
	
	
	$('a[id="'+linkid+'"]').on('click',function (id) {
   		console.log(this.href);
   		return false;
	});
}

function writeHttpResponse() {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			document.getElementById("message").innerHTML = this.responseText;
			
      } else {
      		alert(httpRequest.status);
      }
	}	
}

function writeHttpServiceStatus() {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		element = document.getElementById("status")
		if (httpRequest.status === 200) {
			element.innerHTML = this.responseText;
			if (this.responseText == "ping") {
				$("p[id='timer']").css("background-color", "#F00");
				element.style.backgroundColor = "green";
			}
      } else {
      		element.style.backgroundColor = "red";
      }
	}	
}
 
function geturl()  {
	names =getElementsName("input");
	values = getElementValues("input");
	url = "http://";
		
	url = "http://" + $('input[name="ip"]').attr('value');
	url = url + ":" + $('input[name="port"]').attr('value');
	url = url + "/" + $('input[name="command"]').attr('value') + "?";

	for (i=3;i<names.length;i++) {
		if ( values[i] != "") {
			url = url + names[i] + "=" + values[i] + "&";
		}
	}
	document.getElementById("url").innerHTML = url;
	return url;
}
