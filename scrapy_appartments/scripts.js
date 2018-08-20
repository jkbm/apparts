$(document).ready(function () {

    $.getJSON( "appartments.json", function( data ) {
        var items = [];
        $.each( data, function( key, val ) {
          var row = "<th scrope='row'>"  + val.title + "</th>" + "<td>"  + val.price + "</td>" + "<td><a href="  + val.link + ">Ссылка</td>" + "<td>"  + val.time + "</td>" + "<td>"  + val.district + "</td>" ;
          items.push( "<tr id='" + key + "'>" + row + "</tr>" );
        });
       
        $( "<tbody/>", {
          "class": "offer",
          html: items.join( "" )
        }).appendTo( "table" );
      });
});