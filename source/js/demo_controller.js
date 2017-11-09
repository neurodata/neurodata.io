goog.provide('scaffold.controllers.DemoController');


/** @constructor @ngInject */
scaffold.controllers.DemoController = function($element, $scope, $http) {
  this.$element = $element;
  this.$http = $http;
  this.$scope = $scope;
  this.text = null;
};


/** @export */
scaffold.controllers.DemoController.prototype.sayHello = function(value) {
  var el = this.$element[0];
  var buttonEl = el.querySelector('button');
  buttonEl.textContent = value;
};
