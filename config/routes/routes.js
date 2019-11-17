//var express=require('express');
var fs=require('fs');
//var https=require('https');
//var parseString = require('xml2js').parseString;

//var modelArray=[];
//var blogArray=[];

//var postTitle;
//var postDate;
//var postNoType;
//var postFull;
/*
function timeoutTest(res) {
    console.log("ready");
    res.send("Ipsum lorem");
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
*/
module.exports=function(app,logger){
    'use strict';
    //var DataSerie=require(__dirname+'/../models/data.js');
    //var rootObject={root:__dirname+'/../../public'};
    
    // STATIC
    app.get('/', function(req, res) {
	//res.redirect('/predict');
	res.render('home');
    });

    app.get('/about', function(req, res){
	res.render('about',{user:req.user});
    });
    
    var responses = {};
    
    app.post("/check_answer", function(req, res) {
        //console.log(responses);

        var id = Object.keys(req.body)[0];

        var response = responses[id];
        console.log(response);
        if (response !== undefined) {
            //res.send(response);
            res.send(response);
            console.log("Response sent");
        }
        else {
            res.send("BBnoresponse");
        }

    });
    
    app.post("/submit_question", function(req, res) {

        //var timeout_ms = 1000 * 60 * 30;

        //req.setTimeout(timeout_ms);

        var question = Object.keys(req.body)[0];
        console.log("Got question: " + question);
        if (typeof question == undefined) {
            question = "";
        }

        if (question.slice(-1) != "?") {
            question += "?";
        }

        var id = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 10);
        

        var spawn = require("child_process").spawn;
        var pythonProcess = spawn('python3',["./runQuery.py", question]);
        pythonProcess.stdout.setEncoding('utf-8');
        console.log("Waiting...")
        res.send(id);

        pythonProcess.stdout.on('data', function(data) {
            console.log("Got response! Response is:");
            console.log(data);
            console.log(typeof data);

	    var answer = data;
            if (answer[0] == " ") {
                answer = answer.substring(1);
            }
            //res.send(answer);
            responses[id] = answer


        });
        pythonProcess.stderr.on('data', function(data) {
            console.log("error");
            console.log(data.toString());
        });

    });
    /*
    app.post("/submit_question", function(req, res) {
    
        //var timeout_ms = 1000 * 60 * 30;

        //req.setTimeout(timeout_ms);

        var question = Object.keys(req.body)[0];
        console.log("Got question: " + question);

        var spawn = require("child_process").spawn;
        var pythonProcess = spawn('python3',["./runQuery.py", question]);
        pythonProcess.stdout.setEncoding('utf-8');
        console.log("Waiting...")

        pythonProcess.stdout.on('data', function(data) {
            console.log("Got response! Response is:");
            console.log(data);
            console.log(typeof data);
	    var answer = data;
            res.send(answer);
            console.log("Response sent")

        });
        pythonProcess.stderr.on('data', function(data) {
            console.log("error");
            console.log(data.toString());
        });

    });
    */
};

