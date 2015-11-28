/**
 * Created by nico on 28/11/15.
 */
var usedDates=undefined;
var lastUpdated=0;

function loadDates (url) {
    console.log(url);
    $.ajax({
        url: url,
        type: 'GET',
        timeout: 5000,
        dataType: 'json',
        error: function(){
            alert("Error loading dates");
        },
        success: function(data){
            usedDates=data.used;
            console.log("data: "+ usedDates);
            lastUpdated=new Date().getTime();
            $(document).ready(function() {
                $('.datepicker').datepicker({
                    beforeShowDay:test
                });
            });
        }
    });
}

function test(date){
    var now=new Date();
    var yearFromNow=new Date(new Date().setFullYear(now.getFullYear()+1));
    if (date<now){
        return [false,"","day already passed"];
    }
    if (date>yearFromNow){
        return [false,"","day too much ahead"];
    }
    console.log(date);
    var sDate=$.datepicker.formatDate('yy-mm-dd', date);
    console.log(sDate);
    var ocuped=usedDates != undefined && $.inArray(sDate, usedDates) > -1;
    if (ocuped){
        return [false,"","occuped"];
    } else {
        return [true,"","free"];
    }

}
