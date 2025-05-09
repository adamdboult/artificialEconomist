// Dependencies
var express = require("express");
var http = require("http");
var mongoose = require("mongoose");

////////////////////////////////////
/* Process command line arguments */
////////////////////////////////////

var http_port = 8080;
if (process.argv[2] != null) {
  http_port = process.argv[2];
}

var mongo_domain = "127.0.0.1";
if (process.argv[3] != null) {
  mongo_domain = process.argv[3];
}

var mongo_port = 27017;
if (process.argv[4] != null) {
  mongo_port = process.argv[4];
}

var tf_domain = "artificialeconomist_tensorflow";
if (process.argv[5] != null) {
  tf_domain = process.argv[5];
}

var tf_port = 8008;
if (process.argv[6] != null) {
  tf_port = process.argv[6];
}

console.log("HTTP port is: " + http_port);

console.log("Mongo domain is: " + mongo_domain);
console.log("Mongo port is: " + mongo_port);

console.log("Tensorflow domain is: " + tf_domain);
console.log("Tensorflow port is: " + tf_port);

///////////
/* Mongo */
///////////
var database_name = "pymongo_test";

mongoose
  .connect(`mongodb://${mongo_domain}:${mongo_port}/${database_name}`, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log("Connected to MongoDB!");
  })
  .catch((err) => {
    console.error("Database connection error:", err);
  });

var db = mongoose.connection;

db.collection("posts").findOne(
  { id: "mjcdaxb" },
  "id question resonse",
  function (err, doc) {
    if (err) console.error("ERR" + err);

    if (doc == null) {
      console.log("None");
    }

    console.log("here");
    console.log(doc);
  },
);

console.log("starting dump");
db.collection("posts").find(function (err, doc) {
  if (err) console.error("ERR" + err);

  if (doc == null) {
    console.log("None");
  }

  console.log("here");
  console.log(doc);
});
console.log("finished dump");

////////////////////////
/* Express and routes */
////////////////////////

//START EXPRESS
var app = express();

app.use(express.urlencoded({ extended: true }));

//ROUTES
app.use(express.static(__dirname + "/public")); // set the static files location /public/img will be /img for users

//pretty makes the html not just 1 line, and so is readable
app.locals.pretty = true;
app.set("views", __dirname + "/src/pug/");
app.set("view engine", "pug");

require(__dirname + "/config/routes/routes")(app, db, tf_domain, tf_port);

// Since this is the last non-error-handling
// middleware used, we assume 404, as nothing else
// responded.
app.use(function (req, res) {
  res.status(404);

  // respond with html page
  if (req.accepts("html")) {
    res.render("404", { url: req.url });
    return;
  }

  // respond with json
  if (req.accepts("json")) {
    res.send({ error: "Not found" });
    return;
  }

  // default to plain-text. send()
  res.type("txt").send("Not found");
});

/////////////////
/* HTTP server */
/////////////////
var httpServer = http.createServer(app);
var HTTPport = http_port;
httpServer.listen(HTTPport);

console.log("App listening on port " + http_port);
