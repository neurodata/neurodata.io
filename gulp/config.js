'use strict'

module.exports = {
  Path: {
    CSS_SOURCE_DIR: './source/sass/',
    CSS_SOURCES: './source/sass/**/*.scss',
    CSS_OUT_DIR: './dist/css/',
    JS_OUT_DIR: './dist/js/',
    JS_TEMP_DIR: './.tmp/',
    JS_SOURCES: './source/js/**/*.js',
    BOWER_FOLDER: './bower_components/',
    CLOSURE_EXTERNS: [
        './bower_components/closure-compiler-src/externs/browser/**/*.js'
    ]
  }
}
