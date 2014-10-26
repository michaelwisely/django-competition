(function(){
  var app = angular.module('team_list', ['ngResource']);

  app.controller('TeamListController', function($http){
    controller = this;

    controller.teams = [];

    protocol = window.location.protocol;
    host = window.location.host;
    url = protocol + "//" + host + "/api/competition/" + window.competition_slug + "/teams/";

    $http.get(url).success(function(data, status, headers, config) {
      controller.teams = data;
      console.log(data);
    });

    controller.empty = function() {
      return controller.teams.length == 0;
    };
  });

})();
