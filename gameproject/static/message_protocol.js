$(document).ready(function () {
  'use strict';
  $("#testing").text("loaded");
  $(window).on('message', function(evt) {
    var data = evt.originalEvent.data;
    var msg_type = data.messageType;

    switch(msg_type){

      case "SCORE":
        var score = data.score;
        $("#testing").text(score);
        $.ajax({
          url: '/addscore/',
          data: { 'score': score, 'game': game,
            'user': user},
            success: function(res){
              $(".highscores").html(res)
            }
        });
        break;

      case "SAVE":
        var game_state = data.gameState;
        game_state = JSON.stringify(game_state);
        $.ajax({
          url: '/savegame/',
          data: { 'game_state': game_state, 'game': game,
            'user': user},
            success: function(res){
              $("#last_saved").text(res);
            }
        });
        break;

      case "LOAD_REQUEST":
        $.ajax({
          url: '/loadgame/',
          data: { 'game': game, 'user': user},
          success: function(res){
            var win = document.getElementById('game').contentWindow;
            win.postMessage(res, "*");
          }
        });
        break;

      case "SETTING":
        $("#game").width(data.options.width);
        $("#game").height(data.options.height);
    }
  });
});
