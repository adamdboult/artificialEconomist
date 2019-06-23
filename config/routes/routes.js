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

    app.post("/submit_question", function(req, res) {
        var question = Object.keys(req.body)[0];
        console.log("Got question: " + question);
        var spawn = require("child_process").spawn;
        console.log("Spawning...")
        var pythonProcess = spawn('python3',["./test2.py", question]);
        pythonProcess.stdout.setEncoding('utf-8');
        console.log("Waiting...")
        pythonProcess.stdout.on('data', function(data) {
            console.log(data);
            console.log(typeof data);
	    var answer = data;
            //var answer = data.toString();
            //console.log("hi");
            //console.log(typeof answer);
            //console.log(answer);
            //console.log(btoa(answer));
            //var answer2 = data.decode("utf-8");
            //console.log("hi2");
            //console.log(typeof answer2);
            //console.log(answer2);
            //var answer3=encodeURIComponent(answer);
            //console.log("hi3");
            //console.log(typeof answer3);
            //console.log(answer3);
	    //var answer4=answer
            //var answer=answer.replace(/\\n/g,"\n");
            //var answer=answer.replace(/\\'/g,"\'");
            //console.log("hi4");
            //console.log(typeof answer4);
            //console.log(answer4);
	    //console.log(answer.split(""));
            //console.log(data);
            //console.log(typeof data)
            res.send(answer);

        });
        pythonProcess.stderr.on('data', function(data) {
            console.log("error");
            console.log(data.toString());
        });

    });

};

