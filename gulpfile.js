var fs = require('fs');
var gulp = require('gulp');

/**
 * This will load all js or coffee files in the gulp directory
 * in order to load all gulp tasks
 */
fs.readdirSync('./gulp/tasks').filter(function(file) {
  return (/\.(js|coffee)$/i).test(file);
}).map(function(file) {
  require('./gulp/tasks/' + file);
});

gulp.task('build', ['build_js', 'sass']);
gulp.task('default', ['build', 'watch']);
