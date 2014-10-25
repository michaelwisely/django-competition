(function(){
  var app = angular.module('free_agent_list', ['ngResource']);

  app.factory("FreeAgent", function($resource) {

    return $resource("/api/competition/" + window.competition_slug + "/freeagents/");
  })

  app.controller('FreeAgentController', function(FreeAgent){
    controller = this;

    controller.free_agents = [];

    FreeAgent.query(function(data) {
      controller.free_agents = data;
      console.log(data);
    });

    controller.empty = function() {
      return controller.free_agents.length == 0;
    };
  });

})();
