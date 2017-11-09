'use strict'
var gulp = require('gulp');
var runSequence = require('run-sequence');
var filenames = require('gulp-filenames');
var concat = require('gulp-concat');
var closureCompiler = require('gulp-closure-compiler');
var uglify = require('gulp-uglify');
var config = require('../config');

gulp.task('compile_js', function() {
  var closureOpts = {
    compilerPath: './bower_components/closure-compiler/compiler.jar',
    compilerFlags: {
        angular_pass: true,
        closure_entry_point: 'scaffold',
        compilation_level: 'SIMPLE_OPTIMIZATIONS',
        generate_exports: true,
        manage_closure_dependencies: true,
        only_closure_dependencies: true,
        output_wrapper: '(function(){%output%})();',
        js: [
            './bower_components/closure-library/closure/**.js',
            './bower_components/closure-library/third_party/**.js',
            '!**_test.js'
        ]
    },
    maxBuffer: 800000, // Set maxBuffer to .8GB
    fileName: 'build.min.js'
  };

  var externs = [];
  externs.concat(filenames.get('closure_externs'));

  closureOpts.compilerFlags.externs = externs

  return gulp.src(config.Path.JS_SOURCES)
    .pipe(closureCompiler(closureOpts))
    .pipe(gulp.dest(config.Path.JS_TEMP_DIR))
});

gulp.task('minify_js', function() {
  return gulp.src([
    config.Path.JS_TEMP_DIR + 'build.min.js'
  ])
    .pipe(concat('main.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest(config.Path.JS_OUT_DIR));
});

gulp.task('build_js', function(callback) {
  return runSequence(
    'get_closure_externs_paths',
    'compile_js',
    'minify_js',
    callback);
});

gulp.task('get_closure_externs_paths', function() {
    return gulp.src(config.Path.CLOSURE_EXTERNS)
        .pipe(filenames('closure_externs'))
})
