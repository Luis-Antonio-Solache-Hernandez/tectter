$(function() {
  $('img').load(function(){
    $ancho = $('img').width();
    $
    if($(this).width() < $(this).height()){
      $(this).addClass('tomawidth');
      $(this).css('top', -($(this).height() - $(this).parent().height()) / 2);
    } else{
      $(this).addClass('tomaheight');
      $(this).css('left', -($(this).width() - $(this).parent().width()) / 2);
    }
  });
});