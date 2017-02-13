$(document).ready(function(){
  $(".chart").hide();

  $(".hide_chart").click(function(){
      $(this).parents(".gamestats").children(".chart").hide();
      $(this).parents(".gamestats").children(".show_chart").show()
    });

  $(".show_chart").click(function(){
      $(this).parents(".gamestats").children(".chart").show()
      $(this).parents(".gamestats").children(".show_chart").hide()
    });
});
