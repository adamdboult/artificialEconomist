"use strict";
/*jshint node:true */

//////////////////
/* DEPENDENCIES */
//////////////////

// include gulp
var gulp = require('gulp'); 

// include plug-ins
var jshint = require('gulp-jshint');
//var changed = require('gulp-changed');
//var minifyHTML = require('gulp-minify-html');
var concat = require('gulp-concat');
var stripDebug = require('gulp-strip-debug');
var uglify = require('gulp-uglify');
//var autoprefix = require('gulp-autoprefixer');
//var minifyCSS = require('gulp-minify-css');
//var sass=require('gulp-sass');
var rmdir = require('rimraf');
var fs=require('fs');
//var shell=require('gulp-shell');
var Q = require('q');
var autoprefix = require('gulp-autoprefixer');

var sass=require('gulp-sass');

var clean = require('gulp-clean');
var del = require('del');

/////////////////
/* DIRECTORIES */
/////////////////
var bowerDir = __dirname+'/bower_components';
////////////////
/* FONT FILES */
////////////////

    var fontFiles = [
        bowerDir+'/bootstrap/dist/fonts/**/*',
        bowerDir+'/flat-ui/dist/fonts/**/*',
        bowerDir+'/bootstrap-material-design/dist/fonts/**/*'
    ];

    var mathjaxprefix=bowerDir+'/MathJax';
    var mathjaxFolder=[mathjaxprefix+'/MathJax.js',
		   mathjaxprefix+'/config/**/*',
		   mathjaxprefix+'/fonts/HTML-CSS/TeX/woff/**/*',
		   mathjaxprefix+'/jax/**/*',
		   mathjaxprefix+'/extensions/**/*'
		  ];



gulp.task('emptyDestFolders', function() {
    return del([
        __dirname+'/public'
    ]);
});
    /*

function emptyDestFolders() {
    var deferred = Q.defer();
    rmdir(__dirname+'/public', function(error){
	fs.mkdirSync(__dirname+'/public');
	deferred.resolve();
    });
    return deferred.promise;
    
    //cb();
    
    return del(__dirname + 'public/**');
}
*/
function mathjax (){

    gulp.src(mathjaxFolder,{base:mathjaxprefix})
	.pipe(gulp.dest(__dirname+'/public/js/MathJax/'));

}

function datepicker () {

    var datepickerFolder=[bowerDir+'/bootstrap-datepicker/js/**/*'];

    gulp.src(datepickerFolder,{base:bowerDir+'/bootstrap-datepicker/js'})
	.pipe(gulp.dest(__dirname+'/public/js/datepicker/'));

}

function fallbackjs () {

    var jsFallBack=[bowerDir+'/jquery/dist/jquery.min.js'];

    gulp.src(jsFallBack)
	.pipe(gulp.dest(__dirname+'/public/js/'));
}

    var jsConcatFilesHeader = [
        bowerDir+'/bootstrap/dist/js/bootstrap.js',
        bowerDir+'/d3/d3.min.js',
        bowerDir+'/angular/angular.min.js'

    ];



// JS concat, strip debugging and minify

function scriptsDebug () {

    gulp.src(jsConcatFilesHeader)
	.pipe(concat('coreHeader.js'))
	.pipe(gulp.dest(__dirname+'/public/js/'));

}

function jshint () {
// JS hint task
    gulp.src(jshintFiles)
	.pipe(jshint())
	.pipe(jshint.reporter('default'));

}

gulp.task('imageMin', function() {

    var imgSrc = __dirname+'/src/img/compiled/*',
	imgDst = __dirname+'/public/img';
    
    return gulp.src(imgSrc)
	.pipe(gulp.dest(imgDst));

});

gulp.task('fonts', function() {
    return gulp.src(fontFiles)
	.pipe(gulp.dest(__dirname+'/public/fonts/'));

});

gulp.task('scripts', function () {

    return gulp.src(jsConcatFilesHeader)
	.pipe(concat('coreHeader.js'))
	.pipe(stripDebug())
	.pipe(uglify())
	.pipe(gulp.dest(__dirname+'/public/js/'));
});

gulp.task('styles',function() {

	var stylesFiles_1 = [

	];
	var stylesFiles_2 = [
	];

	var stylesFiles = [
	    bowerDir+'/bootstrap/dist/css/bootstrap.css',
	    //bowerDir+'/Bootflat/bootflat/css/bootflat.min.css',
	    //bowerDir+'/bootstrap-theme-bootswatch-flatly/css/bootstrap.min.css',
	    //bowerDir+'/bootstrap-material-design/dist/css/roboto.min.css',
	    //bowerDir+'/bootstrap-material-design/scss/bootstrap-material-design.scss',
	    //bowerDir+'/bootstrap-material-design/dist/css/ripples.min.css',
	    //bowerDir+'/flat-ui/dist/css/flat-ui.min.css',
	    __dirname+'/src/styles/core.scss'
	];
	console.log(stylesFiles);



    console.log(stylesFiles);
    return gulp.src(stylesFiles)
	.pipe(concat('styles.scss'))
        .pipe(sass())
	.pipe(autoprefix('last 2 versions'))
	//.pipe(minifyCSS({keepSpecialComments:false}))
    //	.pipe(stripDebug())
	.pipe(gulp.dest(__dirname+'/public/css/'));
});


function debugTask() {

    //emptyDestFolders();

    imageMin();
    fonts();
    mathjax();

    datepicker();

    scripts-debug();
    jshint();

    //cb();
}

exports.default = gulp.series('emptyDestFolders', 'styles', 'imageMin', 'fonts', 'scripts');

exports.debug = debugTask;

