// Called to periodically poll the server for a response
function waitForStatus(id) {
  let count = 0;

  const restartCheck = setInterval(() => {
    count++;
    console.log("Polling /check_answer, count =", count);

    // Build a URL-encoded body: id=someUniqueId
    const formData = new URLSearchParams();
    formData.append("id", id);

    fetch("check_answer", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    })
      .then(response => response.text())
      .then(result => {
        console.log("Result from /check_answer:", result);

        if (result !== "BBnoresponse") {
          // Replace newlines with <br> for display
          const newResult = result.replace(/\n/g, "<br/>");

          // Update the UI
          document.getElementById("questionResponse").innerHTML = newResult;
          document.getElementById("submitButton").style.display = "inline-block";
          document.getElementById("waitButton").style.display = "none";

          // Stop polling since we have a response
          clearInterval(restartCheck);
        }
      })
      .catch(error => {
        console.error("Error calling /check_answer:", error);
      });
  }, 10000); // check every 10 seconds
}

document.addEventListener("DOMContentLoaded", () => {
  // Grab references to elements
  const questionField = document.getElementById("question");
  const submitButton = document.getElementById("submitButton");
  const waitButton = document.getElementById("waitButton");
  const responseHeader = document.getElementById("questionResponseHeader");
  const responseDiv = document.getElementById("questionResponse");

  // Hide the wait button initially
  waitButton.style.display = "none";

  // When the user clicks “Submit”
  submitButton.addEventListener("click", () => {
    // Get the user’s question from the textarea
    const question = questionField.value;
    console.log("User question:", question);

    // Show the user that we’re waiting
    submitButton.style.display = "none";
    waitButton.style.display = "inline-block";

    responseHeader.textContent = question;
    responseDiv.innerHTML = "<i>Please wait...</i>";

    // Build a URL-encoded body with question=theUserQuestion
    const formData = new URLSearchParams();
    formData.append("question", question);

    // Hit the /submit_question endpoint
    fetch("submit_question", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    })
      .then(response => response.text())
      .then(id => {
        console.log("Got ID from /submit_question:", id);
        // Now poll /check_answer
        waitForStatus(id);
      })
      .catch(error => {
        console.error("Error calling /submit_question:", error);
      });
  });
});

