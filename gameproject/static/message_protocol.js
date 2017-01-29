$(document).ready(function () {
  'use strict';
  $("#testing").text("loaded");
  $(window).on('message', function(evt) {
    var data = evt.originalEvent.data;
    if (data.messageType == "SCORE"){
      var score = data.score;
      $("#testing").text(score);
      $.ajax({
        url: '/addscore/',
        data: { 'score': score, 'game': game,
          'user': user},
        success: function(data){
          $(".highscores").html(data)
        }
      });
    } else if (data.messageType == "SAVE"){
      var game_state = data.gameState;
      game_state = JSON.stringify(game_state);
      $.ajax({
        url: '/savegame/',
        data: { 'game_state': game_state, 'game': game,
          'user': user},
        success: function(data){
          $("#last_saved").text(data);
        }
      });
    }
  });
});
