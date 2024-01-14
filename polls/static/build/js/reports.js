function search(){
    $("#resultstablebody").empty();
    var id =  $("#nationalid").val();
    var invoice =  $("#invoiceid").val();
    var firstname =  $("#firstname").val();
    var lastname =  $("#lastname").val();
	var loc = $("#location").val();
    var driver =  $("#driver").val();
    var date1 =  $("#datestart").val();
    var date2 =  $("#datestop").val();
    var vletter =  $("#vletter").val();
    var vcode =   $("#vcode").val();
    var vid =  $("#vid").val();
	var vregion = '(' + $("#vregion").val() + ')';
    
    var e = document.getElementById("loadtype");
    var loadtype = e.options[e.selectedIndex].text;
    
    var e = document.getElementById("vtype");
    var vtype = e.options[e.selectedIndex].text;

    var e = document.getElementById("invoicetype");
    var invoicetype = e.options[e.selectedIndex].text;
    

    var vnumber = vregion + vcode + vletter + vid;
    var port = window.location.port || 8000;
	//dic = JSON.stringify({Vregion:vregion, Vid:vid, Fname: firstname, Lname: lastname, Vnumber:vnumber, Ltype:loadtype, Vtype:vtype, Date1:date1, Date2:date2});
	dic = JSON.stringify({ ID: id,Invoice: invoice, Driver:driver, Location:loc, Fname: firstname, Lname: lastname, Vnumber:vnumber, Ltype:loadtype, Vtype:vtype, InOut:invoicetype,Date1:date1, Date2:date2});
    $.ajax({
        url: 'http://lajan.silo:' + port + '/polls/report_search/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: dic,
    success: function (result) {
		if (result.status == "false"){
			alert(result.msg)
		}
		else{

		  var obj = JSON.parse(result)
		  document.getElementById("searchresultcount").value=obj.length;
		  
          if (obj.length==0){
			  var row = $("<tr class=\"even pointer\" >");
			  var string = "<td>" + 'نتیجه ای یافت نشد!' + "</td>";
			  row.append($(string));
			  $("#resultstablebody").append(row);
		  }
		  else{
			  var i;
			  var sumloaded = 0;
			  var sumunloaded = 0;
			  var sumpure = 0;
			  for (i=0; i< obj.length; i++)
			  {
				  var row = $("<tr class=\"even pointer\" >");    
				  row.append($("<td class='notrequired'><input type=\"checkbox\" class=\"flat\" name=\"table_records\"></td>"));
				  var string = "<td>" + obj[i].name + "</td>";
				  row.append($(string));
				  var string = "<td class='notrequired'>" + obj[i].reciept + "</td>";
				  row.append($(string));
				  var string = "<td>" + obj[i].vnumber + "</td>";
				  row.append($(string));
				  var string = "<td>" + obj[i].customerid + "</td>";
				  row.append($(string));
				  var string = "<td class='notrequired'>" + obj[i].driver + "</td>";
				  row.append($(string));
				  var string = "<td>" + obj[i].loadedweight + "</td> </tr>";
				  row.append($(string));
				  var string = "<td>" + obj[i].unloadedweight + "</td> </tr>";
				  row.append($(string));
				  var string = "<td>" + Math.abs(parseInt(obj[i].loadedweight) - parseInt(obj[i].unloadedweight)).toString() + "</td> </tr>";
				  row.append($(string));
				  var string = "<td>" + obj[i].enterdate + "</td> </tr>";
				  row.append($(string));
				  var string = "<td>" + obj[i].exitdate + "</td> </tr>";
				  row.append($(string));
					
				  $("#resultstablebody").append(row);
				  
				  sumloaded = sumloaded + parseInt(obj[i].loadedweight);
				  sumunloaded = sumunloaded + parseInt(obj[i].unloadedweight);
				  
			  }
		  }

          document.getElementById("searchresultsumloaded").value=sumloaded;
          document.getElementById("searchresultsumunloaded").value=sumunloaded;
          document.getElementById("searchresultsumpure").value=sumloaded-sumunloaded;
		}
		
		
	  if (obj.length > 20){
		  document.getElementById("recentloadsdiv").style.height = "1200px";
		  document.getElementById("recentloadsdiv").style.overflow = "auto";
	  }
		
    }
  });    


}

function groupreport(type){
    $("#groupreportbody").empty();
    var date1 =  $("#groupdatestart").val();
    var date2 =  $("#groupdatestop").val();

    
    var e = document.getElementById("grouploadtype");
    var loadtype = e.options[e.selectedIndex].text;


    var e = document.getElementById("groupinvoicetype");
    var invoicetype = e.options[e.selectedIndex].text;
    
    var port = window.location.port || 8000;
    
	//dic = JSON.stringify({Vregion:vregion, Vid:vid, Fname: firstname, Lname: lastname, Vnumber:vnumber, Ltype:loadtype, Vtype:vtype, Date1:date1, Date2:date2});
	dic = JSON.stringify({ Ltype:loadtype, InOut:invoicetype,Date1:date1, Date2:date2, Type:type});
    $.ajax({
        url: 'http://lajan.silo:' + port + '/polls/group_report_search/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: dic,
    success: function (result) {
		if (result.status == "false"){
			alert(result.msg)
		}
		else{
		  var obj = JSON.parse(result)
          if (obj.length==0){
			  var row = $("<tr class=\"even pointer\" >");
			  var string = "<td>" + 'نتیجه ای یافت نشد!' + "</td>";
			  row.append($(string));
			  $("#groupreportbody").append(row);
		  }
		  else{
			  var i;
			  for (i=0; i< obj.length; i++)
			  {
				  var row = $("<tr class=\"even pointer\" >");    
				  var string = "<td>" + obj[i].group + "</td> </tr>";
				  row.append($(string));
				  var string = "<td>" + obj[i].count + "</td> </tr>";
				  row.append($(string));
				  var string = "<td>" + obj[i].sumin + "</td> </tr>";
				  row.append($(string));
				  var string = "<td>" + obj[i].sumout + "</td> </tr>";
				  row.append($(string));
				  var string = "<td>" + obj[i].sumpure + "</td> </tr>";
				  row.append($(string));
				  
				  $("#groupreportbody").append(row);
				  
			  }
		  }
		}
		
		
	  if (obj.length > 20){
		  document.getElementById("groupedresultdiv").style.height = "1200px";
		  document.getElementById("groupedresultdiv").style.overflow = "auto";
	  }
		
    }
  });    


}

function edit_report(){	
    var tbl = document.getElementById("resultstablebody");
	var port = window.location.port || 8000;
    for (var i =0; row=tbl.rows[i]; i++)
    {
        if (row.cells[0].children[0].checked)
        {
            var reciept = row.cells[2].innerText;
			var carid = row.cells[3].innerText;
			var id = row.cells[4].innerText;

			url = 'http://lajan.silo:' + port + '/polls/editloads/' + carid + '/' + id + '/' + reciept;
			window.open(url,'1', "windowFeatures");
            
        }
    }
	

    
};

function print_report(carid, id, reciept){
    
    var tbl = document.getElementById("resultstablebody");
    var alls = '';
	var port = window.location.port || 8000;
    for (var i =0; row=tbl.rows[i]; i++)
    {
        if (row.cells[0].children[0].checked)
        {
            var reciept = row.cells[2].innerText;
            var carid = row.cells[3].innerText;
            var id = row.cells[4].innerText;

            url = 'http://lajan.silo:' + port + '/polls/print/' + carid + '/' + id + '/' + reciept;
            window.open(url,reciept,"windowFeatures");
        
        }
    }

}


function gotodashboard(){
	var port = window.location.port || 8000;
window.open("http://lajan.silo:" + port + "/polls/","_self")
}

function gotouploads(){
	var port = window.location.port || 8000;
window.open("http://lajan.silo:" + port + "/polls/upload_idphoto/","_self")
}

function gotoregfactory(){
	var port = window.location.port || 8000;
window.open("http://lajan.silo:" + port + "/polls/register_factories/","_self");
}

$(document).ready(function () {
var port = window.location.port || 8000;
   $.ajax({
    url:            'http://lajan.silo:' + port + '/polls/initialization/',
    type:           'GET',
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success: function (result) {
      var obj = JSON.parse(result);
      for (var i=0;i<obj.loads.length;i++){
          $("#loadtype").append("<option>" + obj.loads[i] + "</option>")
          $("#grouploadtype").append("<option>" + obj.loads[i] + "</option>")
      }
      for (var i=0;i<obj.cars.length;i++){
          $("#vtype").append("<option>" + obj.cars[i] + "</option>")
      }
    }
  });
  

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
  
              
    myautocomplete(document.getElementById("location"), registeredvillages);

  
})


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





function cancel() {
  $("#nationalid").val('');
  $("#invoiceid").val('');
  $("#firstname").val('');
  $("#lastname").val('');
  $("#driver").val('');
  $("#vletter").val('');
  $("#vcode").val('');
  $("#vid").val('');
  $("#vregion").val('');
  $("#datestart").val('');
  $("#datestop").val('');

  
};


function clearresults() {
  //$("#resultstablebody").empty();
     location.reload();

};

function cleargroupresults() {
  //$("#groupreportbody").empty();
  location.reload();
  
};



function exportExcel(tableText, filename, worksheetName) {
        let downloadLink = document.createElement("a");
        let uri = 'data:application/vnd.ms-excel;base64,'
            , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><meta http-equiv="content-type" content="application/vnd.ms-excel; charset=UTF-8"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body>' + tableText + '</body></html>'
            , base64 = function (s) { return window.btoa(unescape(encodeURIComponent(s))) }
            , format = function (s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }

        let ctx = { worksheet: worksheetName || 'Worksheet', table: tableText }
        // window.location.href = uri + base64(format(template, ctx));
        downloadLink.href = uri + base64(format(template, ctx));
        downloadLink.download = (filename||"exportedTable") + ".xls";

        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    }

function fnExcelReport(tableid){	
    var tab_text="<table border='2px'><tr bgcolor='#87AFC6'>";
    var textRange; var j=0;
    tab = document.getElementById(tableid); // id of table

    for(j = 0 ; j < tab.rows.length ; j++) 
    {     
        tab_text=tab_text+tab.rows[j].innerHTML+"</tr>";
        //tab_text=tab_text+"</tr>";
    }

    tab_text=tab_text+"</table>";
    tab_text= tab_text.replace(/<A[^>]*>|<\/A>/g, "");//remove if u want links in your table
    tab_text= tab_text.replace(/<img[^>]*>/gi,""); // remove if u want images in your table
    tab_text= tab_text.replace(/<input[^>]*>|<\/input>/gi, ""); // reomves input params
    exportExcel(tab_text, 'results', '0')

}

function printresults() {
	var divToPrint=document.getElementById("recentloadsdiv");
	var htmlToPrint = '' +
	'<style type="text/css">' +
	'table th, table td {' +
	'border:0.5px solid #000;' +
	'padding;0.5em;' +
	'}' +
    'body {font: normal 8px;}'
	'</style>';
	newWin= window.open();
	newWin.document.write('<html><head></head><body dir="rtl">');
	newWin.document.write('<h2 style="width:100%;text-align:center;margin-top:0;margin-buttom:0">گزارش موردی</h2>');
	newWin.document.write('<h5 style="width:100%;text-align:center;margin-top:0;;margin-buttom:0">شرکت سیلوی خوشه طلای لاجان</h5>');

	newWin.document.write('<table id="datatable-checkbox" style="width:100%; text-align:center;" cellspacing="0"> ');
	newWin.document.write('<thead><tr>');
	newWin.document.write('<th>نام</th>');

	newWin.document.write('<th>شماره پلاک</th>');
	newWin.document.write('<th>کد ملی</th>');
	newWin.document.write('<th>وزن پر</th>');
	newWin.document.write('<th>وزن خالی</th>');
	newWin.document.write('<th>خالص</th>');
	newWin.document.write('<th>تاریخ ورود</th>');
	newWin.document.write('<th>تاریخ خروج</th>');
	newWin.document.write('</tr></thead>');

	divobj = document.getElementById('resultstablebody').outerHTML;
	newWin.document.write(divobj);
	newWin.document.getElementById('resultstablebody').style.height="auto";
	
	newWin.document.write('</table>');
	
	var count = document.getElementById("searchresultcount").value;
	var sumloaded = document.getElementById("searchresultsumloaded").value;
	var sumunloaded = document.getElementById("searchresultsumunloaded").value;
	var sumpure = document.getElementById("searchresultsumpure").value;
	
	
	newWin.document.write('<table style="width:100%; text-align:center;" cellspacing="0">')
	newWin.document.write('<thead><tr><th>تعداد</th><th>جمع وزن پر</th><th>جمع وزن خالی</th><th>جمع خالص</th></tr></thead>')
	newWin.document.write('<div style="height:20px; width:100%; clear:both;"></div>')
	newWin.document.write('<tbody><tr>')
	newWin.document.write('<td>' + count + '</td>')
	newWin.document.write('<td>' + sumloaded + '</td>')
	newWin.document.write('<td>' + sumunloaded + '</td>')

	newWin.document.write('<td>' + sumpure + '</td>')
	newWin.document.write('</tr></tbody>')
	
	
	newWin.document.write(htmlToPrint)
	newWin.document.write('</body></html>');
	const elements = newWin.document.getElementsByClassName('notrequired');
	while(elements.length > 0){
		elements[0].parentNode.removeChild(elements[0]);
	}


	//newWin.document.write(divToPrint.outerHTML);

	newWin.print();
	newWin.document.close();
	newWin.close();
}

function groupprintresults() {
   var divToPrint=document.getElementById("groupreportbody");
      var htmlToPrint = '' +
        '<style type="text/css">' +
        'table th, table td {' +
        'border:0.5px solid #000;' +
        'padding;0.5em;' +
        '}' +
        '</style>';
   newWin= window.open();
   newWin.document.write('<html><head>');
  
   newWin.document.write('</head><body dir="rtl" >');
   newWin.document.write('<h2 style="width:100%;text-align:center;margin-top:0;margin-buttom:0">تفکیکی</h2>');
   newWin.document.write('<h5 style="width:100%;text-align:center;margin-top:0;;margin-buttom:0">شرکت سیلوی خوشه طلای لاجان</h5>');

	newWin.document.write('<table style="width:80%; text-align:center;" cellspacing="0">')
   newWin.document.write('<thead><tr>')
	newWin.document.write('<th>روز/ماه</th>')
	newWin.document.write('<th>تعداد فاکتور</th>')
newWin.document.write('<th>مجموع پر بار</th>')
newWin.document.write('<th>مجموع خالی بار</th>')
	newWin.document.write('<th>خالص</th>')

newWin.document.write('</tr></thead>')

 
   
   divobj = document.getElementById('groupreportbody').outerHTML;
   newWin.document.write(divobj);
   newWin.document.getElementById('groupreportbody').style.height="auto";
      newWin.document.write(htmlToPrint)
    newWin.document.write('</table>')


 newWin.document.write('</body></html>');
    
   //newWin.document.write(divToPrint.outerHTML);

	newWin.print();
	newWin.document.close();
	newWin.close();
}