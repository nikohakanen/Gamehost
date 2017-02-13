$(document).ready(function(){
  var msg = {};
  msg.messageType = "SETTING";
  var options = {"width": 400, "height": 300};
  msg.options = options;
  parent.postMessage(msg, "*");

  var num = 0;
  var score = 0;
  var latest_message = "Welcome to very serious quiz!";

  $("#answer0").click(function (){
    begin();

  });

  $("#save").click(function (){
    var save_msg = {};
    save_msg.messageType = "SAVE";
    var gameState = {
      score: score, num: num, questions: questions, last: latest_message
    };
    save_msg.gameState = gameState;
    parent.postMessage(save_msg, "*");
  });

  $("#load").click(function (){
    var load_msg = {};
    load_msg.messageType = "LOAD_REQUEST";
    parent.postMessage(load_msg, "*");
  });

  $(window).on('message', function(evt){
    var data = evt.originalEvent.data;
    if (data.messageType == "LOAD"){
      score = data.gameState.score;
      num = data.gameState.num;
      questions = data.gameState.questions;
      unbind_all();
      begin();
    }
  });


  var questions_ordered = [
    {question: "What's the capital of Finland?",
      answers: [
        {val: 0, text: "Stockholm"},
        {val: 1, text: "Helsinki"},
        {val: 0, text: "Oslo"},
        {val: 0, text: "Reykjavik"}
      ]
    },
    {question: "Which of these is a prime number?",
      answers: [
        {val: 1, text: "7"},
        {val: 0, text: "9"},
        {val: 0, text: "6"},
        {val: 0, text: "8"}
      ]
    },
    {question: "What is Garfield's favourite food?",
      answers: [
        {val: 1, text: "Lasagne"},
        {val: 0, text: "Pizza"},
        {val: 0, text: "Hamburgers"},
        {val: 0, text: "Spaghetti"}
      ]
    },
    {question: "Which type is the pokemon Ponyta?",
      answers: [
        {val: 1, text: "Fire"},
        {val: 0, text: "Ground"},
        {val: 0, text: "Normal"},
        {val: 0, text: "Rock"}
      ]
    },
    {question: "Which one of these has NOT been a king?",
      answers: [
        {val: 1, text: "Ratchet"},
        {val: 0, text: "Joffrey"},
        {val: 0, text: "Varian"},
        {val: 0, text: "Shepard"}
      ]
    }
  ];

  var questions = shuffle(questions_ordered);

function unbind_all(){
  $("#answer1").unbind();
  $("#answer2").unbind();
  $("#answer3").unbind();
  $("#answer4").unbind();
}

function begin(){
  ask_question(num);
  $("#answer0").addClass("remove");
  $("#answer1").removeClass("hide");
  $("#answer2").removeClass("hide");
  $("#answer3").removeClass("hide");
  $("#answer4").removeClass("hide");
}

function submit_score(){
  var msg = {};
  msg.messageType = "SCORE";
  msg.score = score;
  parent.postMessage(msg, "*");
}

function ask_question(question){
  if (num >= questions.length){
    $(".div_game_info").addClass("hide");
    $(".div_game_answers").addClass("hide");
    $("#welcome").text("Thank you for playing!");
    $("#game_question").text("Your score: " + score);
    submit_score();

  } else {

    var q = questions[question];
    var vals = [0,1,2,3];
    var shuffled = shuffle(vals);

    $("#answer1").click(function() {
      check_answer(q.answers[shuffled[0]].val);
      ask_question(num);
    });
    $("#answer2").click(function() {
      check_answer(q.answers[shuffled[1]].val);
      ask_question(num);
    });
    $("#answer3").click(function() {
      check_answer(q.answers[shuffled[2]].val);
      ask_question(num);
    });
    $("#answer4").click(function() {
      check_answer(q.answers[shuffled[3]].val);
      ask_question(num);
    });

    $("#game_question").text(q.question);
    $("#question_number").text(num);
    $("#score").text(score);
    $("#answer1").html(q.answers[shuffled[0]].text);
    $("#answer2").html(q.answers[shuffled[1]].text);
    $("#answer3").html(q.answers[shuffled[2]].text);
    $("#answer4").html(q.answers[shuffled[3]].text);
  }

}

function check_answer(value){
  num += 1;
  unbind_all();
  if(value == 1){
    score += 10;
    latest_message = "Correct! Next question:";
  } else {
    latest_message = "Wrong! Next question:"
  }
  $("#welcome").text(latest_message);

}


function shuffle(array) {
  var currentI = array.length, temp, randomI;
  while (0 !== currentI) {
    randomI = Math.floor(Math.random() * currentI);
    currentI -= 1;

    temp = array[currentI];
    array[currentI] = array[randomI];
    array[randomI] = temp;
  }
  return array;
}



});
