function gotoreports(){
	var port = window.location.port || 8000;
	var url = "http://lajan.silo:" + port + "/polls/report_page/";
    window.open(url, "_self");
    /*window.open("http://lajan.silo:8001/polls/report_page/","_self")*/
}
function gotouploads(){
	var port = window.location.port || 8000;
	var url = "http://lajan.silo:" + port + "/polls/upload_idphoto/";
    window.open(url, "_self");
    /*window.open("http://lajan.silo:8001/polls/upload_idphoto/","_self")*/
}
function gotoregfactory(){
	var port = window.location.port || 8000;
	var url = "http://lajan.silo:" + port + "/polls/register_factories/";
    window.open(url, "_self");	
/*window.open("http://lajan.silo:8001/polls/register_factories/","_self");*/
}

function mainloads(){
	document.getElementById("otherform").style.display = "none";
	document.getElementById("othertempform").style.display = "none";
	document.getElementById("infoform").style.display = "block";
	document.getElementById("tempform").style.display = "block";
	/*
	  document.getElementById("nationalid").required = true;
	  document.getElementById("nationalidreq").style.visibility = "visible";
      document.getElementById("firstname").required = true;
	  document.getElementById("firstnamereq").style.visibility = "visible";
      document.getElementById("lastname").required = true;
	  document.getElementById("lastnamereq").style.visibility = "visible";
      document.getElementById("mobile").required = true;
	  document.getElementById("mobilereq").style.visibility = "visible";
      document.getElementById("fathername").required = true;
	  document.getElementById("fathernamereq").style.visibility = "visible";
	  */
}

function otherloads(){
	document.getElementById("infoform").style.display = "none";
	document.getElementById("tempform").style.display = "none";
	document.getElementById("otherform").style.display = "block";
	document.getElementById("othertempform").style.display = "block";
	/*
	  document.getElementById("nationalid").required = false;
	  document.getElementById("nationalidreq").style.visibility = "hidden";
      document.getElementById("firstname").required = false;
	  document.getElementById("firstnamereq").style.visibility = "hidden";
      document.getElementById("lastname").required = false;
	  document.getElementById("lastnamereq").style.visibility = "hidden";
      document.getElementById("mobile").required = false;
	  document.getElementById("mobilereq").style.visibility = "hidden";
      document.getElementById("fathername").required = false;
	  document.getElementById("fathernamereq").style.visibility = "hidden";
	
	*/
}


function asempty(){
    var id =  $("#nationalid").val();
    var firstname =  $("#firstname").val();
    var lastname =  $("#lastname").val();
    var fathername = $("#fathername").val();
    var mobile =  $("#mobile").val();
    var bankaccount =  $("#bankaccount").val();
    var driver =  $("#drivername").val();
    var vletter =  $("#vletter").val();
    var vcode =   $("#vcode").val();
    var vid =  $("#vid").val();
	var vregion = '(' + $("#vregion").val() + ')';
    
    var e = document.getElementById("loadtype");
    var loadtype = e.options[e.selectedIndex].text;
    
    var e = document.getElementById("vtype");
    var vtype = e.options[e.selectedIndex].text;
    
    var full = $("#weightbox").val();
    var vnumber = vregion + vcode + vletter + vid;
    
    var farmlocation = $("#location").val();
	
	if (id.length != 10){
		alert("مقدار شناسه صحیح نمی باشد");
		return 0;
	}
	if (vnumber.length != 10){
		alert("پلاک خودرو صحیح نمی باشد");
		return 0;
	}
	if (firstname.length == 0){
		alert("نام نمیتواند خالی باشد");
		return 0;
	}
	if (isNaN(full)){
		alert("خطا در خواندن باسکول");
		return 0;
	}

	var port = window.location.port || 8000;
    $.ajax({
        url: 'http://lajan.silo:' + port + '/polls/temp_as_empty/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ID: $("#nationalid").val(), Fname: $("#firstname").val(), Lname: $("#lastname").val(), Faname:$("#fathername").val(), Mobile:$("#mobile").val(), Bankacc:$("#bankaccount").val(), Driver:$("#drivername").val(), Vnumber:vnumber, Ltype:loadtype, Vtype:vtype, Fweight: full, Location: farmlocation}),
        success: function (result) {
			if (result.status == "false"){
				alert(result.msg);
				return;
			}
			else
			{
				url = 'http://lajan.silo:' + port + '/polls/print/' + vnumber + '/' + id + '/' + '0';
				window.open(url,'1', "windowFeatures");
				
				location.reload();
			}

        },
        errof: function(xhr,errmsg,err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
    

	
	
};

function asfull(){
    var id =  $("#nationalid").val();
    var firstname =  $("#firstname").val();
    var lastname =  $("#lastname").val();
    var fathername = $("#fathername").val();
    var mobile =  $("#mobile").val();
    var bankaccount =  $("#bankaccount").val();
    var driver =  $("#drivername").val();
    var vletter =  $("#vletter").val();
    var vcode =   $("#vcode").val();
    var vid =  $("#vid").val();
	var vregion =  '(' + $("#vregion").val() + ')';
    
    var e = document.getElementById("loadtype");
    var loadtype = e.options[e.selectedIndex].text;
    
    var e = document.getElementById("vtype");
    var vtype = e.options[e.selectedIndex].text;
    
    var full = $("#weightbox").val();
    var vnumber = vregion + vcode + vletter + vid;
    
    var farmlocation = $("#location").val();

	if (id.length != 10){
		alert("مقدار شناسه صحیح نمی باشد");
		return 0;
	}
	if (vnumber.length != 10){
		alert("پلاک خودرو صحیح نمی باشد");
		return 0;
	}
	if (firstname.length == 0){
		alert("نام نمیتواند خالی باشد");
		return 0;
	}
	if (isNaN(full)){
		alert("خطا در خواندن باسکول");
		return 0;
	}
   var port = window.location.port || 8000;
    $.ajax({
        url: 'http://lajan.silo:' + port + '/polls/temp_as_full/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ID: $("#nationalid").val(), Fname: $("#firstname").val(), Lname: $("#lastname").val(), Faname:$("#fathername").val(), Mobile:$("#mobile").val(), Bankacc:$("#bankaccount").val(), Driver:$("#drivername").val(), Vnumber:vnumber, Ltype:loadtype, Vtype:vtype, Fweight: full, Location: farmlocation}),
        success: function (result) {
			if (result.status == "false"){
				alert(result.msg);
				return;
			}
			else
			{
				url = 'http://lajan.silo:' + port + '/polls/print/' + vnumber + '/' + id + '/' + '0';
				window.open(url,'1', "windowFeatures");
				
				location.reload();
			}

        },
        errof: function(xhr,errmsg,err){
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
    

    
};

function edit_temps(){	
    var tbl = document.getElementById("tablebody");
    var port = window.location.port || 8000;
    for (var i =0; row=tbl.rows[i]; i++)
    {
        if (row.cells[0].children[0].checked)
        {
            var vehicle = row.cells[1].innerText;
			var id = row.cells[2].innerText;
            var myEvent = {vnumber: vehicle};
			url = 'http://lajan.silo:' + port + '/polls/editloads/' + vehicle + '/' + id + '/' + '0';
			window.open(url,'1', "windowFeatures");
            
        }
    }
    

    
};

function edit_finals(){	
    var tbl = document.getElementById("recenttablebody");
	var port = window.location.port || 8000;
    for (var i =0; row=tbl.rows[i]; i++)
    {
        if (row.cells[0].children[0].checked)
        {
            var reciept = row.cells[1].innerText;
			var carid = row.cells[2].innerText;
			var id = row.cells[3].innerText;

			url = 'http://lajan.silo:' +port + '/polls/editloads/' + carid + '/' + id + '/' + reciept;
			window.open(url,'1', "windowFeatures");
            
        }
    }
    

    
};

function register(){

    var tbl = document.getElementById("tablebody");
    var full = $("#weightbox").val();
	if (isNaN(full)){
		alert("خطا در خواندن باسکول");
		return 0;
	}

    var port = window.location.port || 8000;
	for (var i =0; row=tbl.rows[i]; i++)
	{
		if (row.cells[0].children[0].checked)
		{
			var vehicle = row.cells[1].innerText;
			var myEvent = {vnumber: vehicle, weight: full};
			var reciept = "";
			var carid = "";
			var id = "";
			$.ajax({
				url: 'http://lajan.silo:' + port + '/polls/register/',
				type: 'POST',
				dataType: 'json',
				contentType:    'application/json; charset=utf-8',
				data: JSON.stringify(myEvent),
				async: false,
				success: function (result) {
					if (result.status == "false"){
						alert(result.msg)
					}
					else{
					reciept = result.reciept;
					carid = result.carid;
					id = result.id;
					url = 'http://lajan.silo:' + port + '/polls/print/' + carid + '/' + id + '/' + reciept;
					window.open(url,'1', "windowFeatures");
					}
					

				},
				errof: function(xhr,errmsg,err){
					alert(xhr.status + ": " + xhr.responseText);
				}
			});
			  
		}
	}
    

};

function temploads() {
	var port = window.location.port || 8000;
    $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/read_temp_loadings/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      var obj = JSON.parse(result)

      var i;
      for (i=0; i< obj.length; i++)
      {
          var row = $("<tr class=\"even pointer\" >");    
          row.append($("<td><input type=\"radio\" class=\"flat\" name=\"table_records\"></td>"));
          var string = "<td>" + obj[i].vnumber + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].nationalid + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].loadedweight + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].unloadedweight + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].loaddateshamsi + "</td> </tr>";
          row.append($(string));
            
          $("#tablebody").append(row);
          
      }

    }
  });
    

}

function recentloads(){
	var port = window.location.port || 8000;
    $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/read_recent_invoices/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      var obj = JSON.parse(result)

      var i;
      for (i=0; i< obj.length; i++)
      {
          var row = $("<tr class=\"even pointer\" >");    
          row.append($("<td><input type=\"radio\" class=\"flat\" name=\"table_records\"></td>"));
          var string = "<td>" + obj[i].reciept + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].name + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].vnumber + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].customerid + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].location + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].loadedweight + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].unloadedweight + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].enterdate + "</td> </tr>";
          row.append($(string));
          var string = "<td>" + obj[i].exitdate + "</td> </tr>";
          row.append($(string));
            
          $("#recenttablebody").append(row);
          
      }
	  if (obj.length > 7){
		  document.getElementById("recentloadsdiv").style.height = "500px";
		  document.getElementById("recentloadsdiv").style.overflow = "auto";
	  }

    }
  });    
    
    
}


$(document).ready(function () {
  $('#gotoreportslink').click(function(){ gotoreports(); return false; });
  $('#gotouploadlink').click(function(){ gotouploads(); return false; });
   var port = window.location.port || 8000;
   $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/dailystatistics/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      document.getElementById('inputinvoices').innerHTML = result.inputinvoices;
      document.getElementById('outputinvoices').innerHTML = result.outputinvoices;
      document.getElementById('suminweight').innerHTML = result.suminweight;
      document.getElementById('sumoutweight').innerHTML = result.sumoutweight;
    }
  });
  
   $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/initialization/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      var obj = JSON.parse(result);
      for (var i=0;i<obj.loads.length;i++){
          $("#loadtype").append("<option>" + obj.loads[i] + "</option>")
		  $("#oloadtype").append("<option>" + obj.loads[i] + "</option>")
      }
      for (var i=0;i<obj.cars.length;i++){
          $("#vtype").append("<option>" + obj.cars[i] + "</option>")
		  $("#ovtype").append("<option>" + obj.cars[i] + "</option>")
      }
    }
  });
  
  

  temploads();
  recentloads();
  
  registeredvillages = [];
   $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/initlocations/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      var obj = JSON.parse(result);
      for (var i=0;i<obj.villages.length;i++){
          registeredvillages.push(obj.villages[i])
      }

    }
  });
  
   registerednames = [];
   var port = window.location.port || 8000;
   $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/initnames/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      var obj = JSON.parse(result);
      for (var i=0;i<obj.names.length;i++){
          registerednames.push(obj.names[i])
      }

    }
  });
  
    myautocomplete(document.getElementById("location"), registeredvillages);
	myautocomplete(document.getElementById("olocation"), registeredvillages);
	myautocomplete(document.getElementById("firstname"), registerednames);
   
});


var myVar = setInterval(getStuff, 500);

function getStuff() {
  var weight = document.getElementById('weightbox').value
  var port = window.location.port || 8000;
  $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/stuff/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
		$("#weightbox").val(result.msg);
		$("#ofirstweight").val(result.msg);
		if (result.status=='true'){
			document.getElementById('weightbox').style.color = "green";
			document.getElementById('ofirstweight').style.color = "green";
			document.getElementById("emptbtn").enabled = true;
			document.getElementById("fullbtn").enabled = true;
			document.getElementById("oemptybtn").enabled = true;
			document.getElementById("ofullbtn").enabled = true;
			document.getElementById("regbtn").enabled = true;
		}
		else if(result.status=='notstable'){
			document.getElementById("emptbtn").disabled = false;
			document.getElementById("fullbtn").disabled = false;
			document.getElementById("oemptybtn").disabled = false;
			document.getElementById("ofullbtn").disabled = false;
			document.getElementById("regbtn").disabled = false;
			document.getElementById('weightbox').style.color = "red";;
			document.getElementById('ofirstweight').style.color = "red"
			var nodes = document.getElementById("registerdiv").getElementsByTagName('*');
			for(var i = 0; i < nodes.length; i++){
			nodes[i].disabled = false;
			}
		}
		else{
			document.getElementById('weightbox').style.color = "red"
			document.getElementById('ofirstweight').style.color = "red"
			var nodes = document.getElementById("registerdiv").getElementsByTagName('*');
			//for(var i = 0; i < nodes.length; i++){
			//nodes[i].disabled = false;
			//}
		}
    }
  });
};


var myVar = setInterval(lastedited, 1000);

function lastedited() {
  var weight = document.getElementById('weightbox').value
  var port = window.location.port || 8000;
  $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/lastedited/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      if (result.reload){
          location.reload();
      }
    }
  });
};

function autocarnumber(e) {
    var port = window.location.port || 8000;
    $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/autocarnumber/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      $("#vletter").val(result.char);
      $("#vcode").val(result.number);
      $("#vid").val(result.id);
	  $("#vregion").val('25')
      
    }
  });
    
    
}

function searchid() {
  var id = document.getElementById('nationalid').value
  var port = window.location.port || 8000;
  $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/searchid/'+id.toString(),
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      $("#customernumber").val(result.customernumber);
      $("#firstname").val(result.firstname);
      $("#lastname").val(result.lastname);
      $("#mobile").val(result.mobile);
      $("#bankaccount").val(result.bank);
      $("#drivername").val(result.firstname + ' ' + result.lastname);
      //$("#vletter").val(result.vletter);
      //$("#vcode").val(result.vcode);
      //$("#vid").val(result.vid);
	  //$("#vregion").val(result.vregion);
      $("#fathername").val(result.fathername);
      
    }
  });
};

function searchid1(){
	var val = $("#nationalid").val().trim();
	var port = window.location.port || 8000;
	if(val.length == 10){
		  var id = document.getElementById('nationalid').value
		  $.ajax({
			url:            'http://lajan.silo:' + port + '/polls/searchid/'+id.toString(),
			type:           'GET',
			contentType:    'application/json; charset=utf-8',
			dataType:       'json',
			success: function (result) {
			  $("#customernumber").val(result.customernumber);
			  $("#firstname").val(result.firstname);
			  $("#lastname").val(result.lastname);
			  $("#mobile").val(result.mobile);
			  $("#bankaccount").val(result.bank);
			  $("#drivername").val(result.firstname + ' ' + result.lastname);
			  //$("#vletter").val(result.vletter);
			  //$("#vcode").val(result.vcode);
			  //$("#vid").val(result.vid);
			  //$("#vregion").val(result.vregion);
			  $("#fathername").val(result.fathername);
			  
			}
		  });
	}
}

function splitname(){
	var name = $("#firstname").val().split('|');
	if (name.length > 1){
		$("#firstname").val(name[0]);
		$("#lastname").val(name[1]);
	}
}

function cancel() {
  $("#nationalid").val('');
  $("#customernumber").val('');
  $("#firstname").val('');
  $("#lastname").val('');
  $("#mobile").val('');
  $("#bankaccount").val('');
  $("#drivername").val('');
  $("#vletter").val('');
  $("#vcode").val('');
  $("#vid").val('');
  $("#vregion").val('');
  $("#fathername").val('');
  
};

function myautocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
			  if (inp.id == "firstname"){
				splitname();
			  }
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
} 

function print_temp(){

    var tbl = document.getElementById("tablebody");
    var port = window.location.port || 8000;
    for (var i =0; row=tbl.rows[i]; i++)
    {
        if (row.cells[0].children[0].checked)
        {
            var carid = row.cells[1].innerText;
            var id = row.cells[2].innerText;


			url = 'http://lajan.silo:' + port + '/polls/print/' + carid + '/' + id + '/' + '0';
			window.open(url,'1', "windowFeatures");
        
        }
    }

	
}

function printinvoice(carid, id, reciept){
    
    var tbl = document.getElementById("recenttablebody");
    var alls = '';
	var port = window.location.port || 8000;
    for (var i =0; row=tbl.rows[i]; i++)
    {
        if (row.cells[0].children[0].checked)
        {
            var reciept = row.cells[1].innerText;
            var carid = row.cells[2].innerText;
            var id = row.cells[3].innerText;

            url = 'http://lajan.silo:' + port + '/polls/print/' + carid + '/' + id + '/' + reciept;
            window.open(url,reciept,"windowFeatures");
        
        }
    }

}



function oregister(type){
    var id =  $("#onationalid").val();
	if (id.trim().length == 0){
		alert("شناسه نمیتواند خالی باشد. لطفا کدملی یا شناسه دیگری وارد کنید");
		return 0;
	}
    var firstname =  $("#ofullname").val();
    var reciept =  $("#oreciept").val();

    var vletter =  $("#ovletter").val();
    var vcode =   $("#ovcode").val();
    var vid =  $("#ovid").val();
	var vregion = '(' + $("#ovregion").val() + ')';
    
    var e = document.getElementById("oloadtype");
    var loadtype = e.options[e.selectedIndex].text;
    
    var e = document.getElementById("ovtype");
    var vtype = e.options[e.selectedIndex].text;
    
    var firstweight = $("#ofirstweight").val();
	var secondweight = $("#osecondweight").val();
	
    var vnumber = vregion + vcode + vletter + vid;
    
    var farmlocation = $("#olocation").val();
	
	if (firstweight.length>0){
		if (isNaN(firstweight)){
			alert("خطا در خواندن باسکول");
			return 0;
		}
	}
	else {
		alert("خطا در خواندن باسکول");
		return 0;	

	}
	
    var port = window.location.port || 8000;
	if (vnumber.length == 10){
    
		$.ajax({
			url: 'http://lajan.silo:' + port + '/polls/oregister/',
			type: 'POST',
			dataType: 'json',
			async: false,
			contentType: 'application/json',
			data: JSON.stringify({ID: $("#onationalid").val(), Reciept:reciept, Fname: $("#ofullname").val(), Vnumber:vnumber, Ltype:loadtype, Vtype:vtype, Fweight: firstweight, Sweight: secondweight, Location: farmlocation, Type:type}),
			success: function (json) {
				alert(json.msg);
			},
			errof: function(xhr,errmsg,err){
				alert(json.msg);
				console.log(xhr.status + ": " + xhr.responseText);
			}
		});
		
		url = 'http://lajan.silo:' + port + '/polls/print/' + vnumber + '/' + id + '/' + '1';
		window.open(url,'1', "windowFeatures");
		location.reload();
	}
	else{
		alert("شماره پلاک صحیح نمی باشد");
	}
    
};

function oempty(){
	oregister("empty");
}

function ofull(){
	oregister("full");
}

function osearchid() {
  var id = document.getElementById('onationalid').value
  var port = window.location.port || 8000;
  $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/osearchid/'+id.toString(),
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {

      var obj = JSON.parse(result)

      var i;
      for (i=0; i< obj.length; i++)
      {
          var row = $("<tr class=\"even pointer\" >");    
          row.append($("<td><input type=\"radio\" class=\"flat\" name=\"table_records\"></td>"));
          var string = "<td>" + obj[i].vnumber + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].id + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].loadedweight + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].unloadedweight + "</td>";
          row.append($(string));
          var string = "<td>" + obj[i].firstdate + "</td>";
          row.append($(string));
            
          $("#otherstablebody").append(row);
          
      }
      
    }
  });
};

function ochoose(){

    var tbl = document.getElementById("otherstablebody");
    
    for (var i =0; row=tbl.rows[i]; i++)
    {
        if (row.cells[0].children[0].checked)
        {
            var vnumber = row.cells[1].innerText;
            var id = row.cells[2].innerText;
            var loadedweight = row.cells[3].innerText;
            var unloadedweight = row.cells[4].innerText;
			
            idx1 = vnumber.indexOf('(');
            idx2 = vnumber.indexOf(')');
          
			$("#ovletter").val(vnumber.substring(idx2 + 4,idx2+5));
			$("#ovcode").val(vnumber.substring(idx2+1,idx2+4));
			$("#ovid").val(vnumber.substring(idx2+5,100));
			$("#ovregion").val(vnumber.substring(idx1+1,idx2));
			
			if (loadedweight>0){
			$("#osecondweight").val(loadedweight);
			}
			if (unloadedweight>0){
			$("#osecondweight").val(unloadedweight);				
			}
			$("#oreciept").val(id);
        
        }
    }

	
}

function oautocarnumber(e) {
    var port = window.location.port || 8000;
    $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/oautocarnumber/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      $("#ovletter").val(result.char);
      $("#ovcode").val(result.number);
      $("#ovid").val(result.id);
	  $("#ovregion").val('25')
      
    }
  });
    
    
}

