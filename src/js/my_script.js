function waitForStatus(id) {
	var count = 0;
	var restartCheck = setInterval(function() {
		count++;
		$.ajax({
			url: "check_answer",
			type: "POST",
			data: { id: id },
			success: function(result) {
				console.log(count);
				console.log(result);
				if (result != "BBnoresponse") {
					newResult = result.replace(/\n/g, '<br/>')
					$("#questionResponse").html(newResult);
					$("#submitButton").show();
					$("#waitButton").hide();
					clearInterval(restartCheck);					
				}	
			}
		});
      }, 10000);
}

$(document).ready(function(){
	$("#waitButton").hide()
	$("#submitButton").click(function(){
  		var question = document.getElementById("question").value;
		console.log(question);
		$("#submitButton").hide();
		$("#waitButton").show();
		$("#questionResponseHeader").html(question)
		$.ajax({
		    type: "POST",
		    url: "submit_question",
		    data: { question: question },
		    success: function(result){
			    console.log("Got initial response!");
			    console.log(result);
			    waitForStatus(result);
			}
		});
		$("#questionResponse").html("<i>Please wait...</i>");
	});
});

