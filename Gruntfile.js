module.exports = function(grunt) {

  // load all grunt tasks
  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

  var port = 3001;

  grunt.initConfig({
    open : {
      dev: {
        path: 'http://localhost:' + port
      }
    },

    connect: {
      server: {
        options: {
          port: port,
          base: 'build/html',
          livereload: true
        }
      }
    },

    exec: {
      build_sphinx: {
        cmd: 'make html'
      },
      clean: {
        cmd: 'make clean'
      }
    },

    watch: {
      /* Changes in theme dir rebuild sphinx */
      sphinx: {
        files: ['source/**/*.rst', 'source/**/*.html', 'source/**/*.css'],
        tasks: ['exec:build_sphinx']
      },
      /* live-reload the demo_docs if sphinx re-builds */
      livereload: {
        files: ['build/html/*'],
        options: { livereload: true }
      }
    }

  });

  grunt.loadNpmTasks('grunt-exec');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-open');

  grunt.registerTask('default', ['exec:clean','exec:build_sphinx','connect','open','watch']);
  grunt.registerTask('build', ['exec:clean','exec:build_sphinx']);
}

