$('.toggle').on('click', function() {
  $('.container').stop().addClass('active');
});

$('.close').on('click', function() {
  $('.container').stop().removeClass('active');
});
$(document).ready(function(){
        $("#err").fadeOut(5000);
   
}); 

