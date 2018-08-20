$(document).ready(function () {

    $('.remove').click(function(){
        console.log("Clicked!");
        $( this ).parents('tr').css("background-color", "grey"); 
        return false;
    });
    $('.offer').dblclick(function(){
        $( this ).fadeOut('slow'); 
        return false;
    });
});