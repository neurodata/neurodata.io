goog.provide('scaffold');

goog.require('scaffold.controllers.DemoController');


/** @export */
scaffold.main = function() {
  angular.module('scaffold', [])
      .controller('DemoController', scaffold.controllers.DemoController)
  angular.bootstrap(document, ['scaffold']);
};
