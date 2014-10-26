(function(){
  var app = angular.module('team_list', ['ngResource']);

  app.factory("Team", function($resource) {

    return $resource("/api/competition/" + window.competition_slug + "/teams/");
  })

  app.controller('TeamListController', function(Team){
    controller = this;

    controller.teams = [];

    Team.query(function(data) {
      controller.teams = data;
      console.log(data);
    });

    controller.empty = function() {
      return controller.teams.length == 0;
    };
  });

})();
