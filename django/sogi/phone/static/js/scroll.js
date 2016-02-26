$(function(){
  $(".onetable").scroll(function(){
    var scrollVal = $(this).scrollTop();
    $("td.title").css({top:scrollVal});
  });
});