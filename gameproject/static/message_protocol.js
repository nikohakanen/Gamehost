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
          window.location.reload();
        }
      });
    }
  });
});
