$(document).ready(function(){
        minDate = new Date();
        $(".datetimeinput").datepicker({
            showAnim : 'drop',
            numberOfMonth : 1,
            minDate : minDate,
        });
});


