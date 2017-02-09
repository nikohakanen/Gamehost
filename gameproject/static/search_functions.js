$(document).ready(function(){
  // Setting up the search filters.
  $("#all_filter").click(function(){
    filter_all("all");
  });
  $("#strategy_filter").click(function(){
    filter_all("strategy");
  });
  $("#shooting_filter").click(function(){
    filter_all("shooting");
  });
  $("#arcade_filter").click(function(){
    filter_all("arcade");
  });
  $("#adventure_filter").click(function(){
    filter_all("adventure");
  });
  // The initial load will display all games.
  $.ajax({
    url: '/games/',
    data: {'genre': "all"},
    success: function(res){
      $("#games_div").html(res);
    }
  });
});
// The function used for receiving games of the given genre.
function filter_all(genre){

  $.ajax({
    url: '/games/',
    data: {'genre': genre},
    success: function(res){
      $("#games_div").html(res);
    }
  });
}
