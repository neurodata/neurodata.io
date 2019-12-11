var gulp = require("gulp");

gulp.task("css", function () {
    const postcss = require("gulp-postcss");

    return (
        gulp
        .src("source/css/cv.css")
        // ...
        .pipe(
            postcss([
                // ...
                require("tailwindcss"),
                require("autoprefixer")
                // ...
            ])
        )
        // ...
        .pipe(gulp.dest("source/css-gulp/"))
    );
});