"use strict";
/*jshint node:true */

//WINSTON
var logger = require(__dirname + '/config/winston');

//DEPENDENCIES, 'jade' not included but referenced later
var express  = require('express'),
    http = require('http'),
    https = require('https'),
    fs=require('fs'),
    forceDomain = require("forcedomain"),
    favicon = require('serve-favicon'),
    spawn = require('child_process').spawn;

// config
var configObj = JSON.parse(fs.readFileSync('private/config.json' , 'utf8'));

//START EXPRESS
var app = express();
/*
app.use(forceDomain({
    hostname: configObj.siteName,
    //  port: 443,
    protocol: 'https'
}));
*/
//forward http to https
/*
function requireHTTPS(req, res, next) {
    if (!req.secure) {
        //FYI this should work for local development as well
        return res.redirect('https://' + req.get('host') + req.url);
    }
    next();
}

app.use(requireHTTPS);
*/
app.set('trust proxy', 1);

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

//FAVICON
app.use(favicon(__dirname + configObj.favicon));

//ROUTES
app.use(express.static(__dirname + '/public'));// set the static files location /public/img will be /img for users

app.locals.pretty=true;
app.set('views',__dirname+'/src/jade/');
app.set('view engine', 'jade');

require(__dirname+'/config/routes/routes')(app, logger);

// Since this is the last non-error-handling
// middleware used, we assume 404, as nothing else
// responded.
app.use(function(req, res, next){
    res.status(404);

    // respond with html page
    if (req.accepts('html')) {
	res.render('404', { url: req.url });
	return;
    }

    // respond with json
    if (req.accepts('json')) {
	res.send({ error: 'Not found' });
	return;
    }
    
    // default to plain-text. send()
    res.type('txt').send('Not found');
});

//HTTP
var HTTPportnum=configObj.ports.http;
var HTTPport = process.env.PORT || HTTPportnum;
//app.listen(HTTPport);

//HTTPS setup
/*
var HTTPSportnum = configObj.ports.https;
var privateKey = fs.readFileSync(configObj.keys.privateKey);
var certificate = fs.readFileSync(configObj.keys.certificate);
//var certAuth = fs.readFileSync(configObj.keys.certAuth);
var options = {key: privateKey,
	       cert: certificate,
//	       ca: certAuth
	      };

var httpsPort = process.env.PORT || HTTPSportnum;
*/
// LISTEN
var httpServer=http.createServer(app);
httpServer.listen(HTTPport);

logger.debug("App listening on port " + HTTPport);

//var httpsServer=https.createServer(options,app);
//httpsServer.listen(httpsPort);
//logger.debug("HTTPS on port "+httpsPort);
