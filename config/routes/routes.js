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
    /*
    app.post("/submit_question", function(req, res) {
        var question = Object.keys(req.body)[0];
        console.log("Got question: " + question);
        var spawn = require("child_process").spawn;
        console.log("Spawning...")
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

    app.post("/submit_question", function(req, res) {
        var question = Object.keys(req.body)[0];
        console.log("Got question: " + question);
        var spawn = require("child_process").spawn;
        console.log("Spawning...")
        var pythonProcess = spawn('python3',["./runQuery.py", question]);
        pythonProcess.stdout.setEncoding('utf-8');
        res.send("Ipsum lorem")

    });

};

