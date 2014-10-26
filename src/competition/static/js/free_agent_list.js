(function(){
  var app = angular.module('free_agent_list', ['ngResource']);

  app.controller('FreeAgentController', function($http){
    controller = this;

    controller.free_agents = [];

    protocol = window.location.protocol;
    host = window.location.host;
    url = protocol + "//" + host + "/api/competition/" + window.competition_slug + "/freeagents/";

    $http.get(url).success(function(data, status, headers, config) {
      controller.free_agents = data;
      console.log(data);
    });

    controller.empty = function() {
      return controller.free_agents.length == 0;
    };
  });

})();
