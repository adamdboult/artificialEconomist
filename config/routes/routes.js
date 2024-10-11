var spawn = require("child_process").spawn;

module.exports = function (app, db, tf_domain, tf_port) {
  "use strict";

  // STATIC
  app.get("/", function (req, res) {
    //res.redirect('/predict');
    res.render("home");
  });

  app.get("/about", function (req, res) {
    res.render("about", { user: req.user });
  });

  app.get("/examples", function (req, res) {
    res.render("examples", { user: req.user });
  });

  //var responses = {};

  app.post("/check_answer", function (req, res) {
    var id = Object.keys(req.body)[0];
    console.log("ID is " + id);

    db.collection("posts").findOne(
      { id: id },
      "id question response",
      function (err, doc) {
        if (err) console.error("ERR" + err);
        if (doc == null) {
          res.send("BBnoresponse");
        } else {
          res.send(doc.response);
        }
        console.log("here");
        console.log(doc);
      },
    );
  });

  app.post("/submit_question", function (req, res) {
    var question = Object.keys(req.body)[0];
    console.log("Got question: " + question);
    if (typeof question == undefined) {
      question = "";
    }
    // Remove non-ascii
    question = question.replace(/[^\x00-\x7F]/g, "");

    // Remove leading and trailing whitespace
    question = question.trim();

    // Append "?" if missing from the end
    if (question.slice(-1) != "?") {
      question += "?";
    }

    // If too long, trim
    if (question.length > 100) {
      question = question.substring(0, 100);
    }

    var id = Math.random()
      .toString(36)
      .replace(/[^a-z]+/g, "")
      .substr(0, 50);

    var id_and_question = id + "|" + question;

    var pythonProcess = spawn("wget", [
      "-qO-",
      tf_domain + ":" + tf_port + "/" + id_and_question,
    ]);

    console.log("Waiting...");
    res.send(id);

    pythonProcess.stderr.on("data", function (data) {
      console.log("error");
      console.log(data.toString());
    });
  });
};
