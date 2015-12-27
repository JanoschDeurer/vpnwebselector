(function(){
  angular.module('VpnWebSelector', ['ngMaterial']).controller('QuerryController', function($http, $timeout, $q, $log, $scope) {
    var vm = this;
    // list of `state` value/display objects
    vm.querySearch = querySearch;
    vm.selectedItemChange = selectedItemChange;
    vm.searchTextChange   = searchTextChange;
    getSelectedConfig();
    // ******************************
    // Internal methods
    // ******************************
    /**
     * Search for vpn configs 
     */
    function querySearch (query) {
      return $http({
        method: 'GET',
        url: '/getConfigs?q=' + query 
      }).then(function successCallback(response) {
          return response.data;
      }, function errorCallback(response) {
        return query;
      });
    }
    vm.submit = function(){
      $log.info('Config changed to ' + vm.searchText);
      $http({
        method: 'GET',
        url: '/setConfig?q=' + vm.searchText, 
      }).then(function successCallback(response) {
        getSelectedConfig();
      }, function errorCallback(response) {
        $log.info('Error while setting config')
      });
    }

    function getSelectedConfig() {
      $http({
        method: 'GET',
        url: '/getSelectedConfig' 
      }).then(function successCallback(response) {
        vm.selectedConfig = response.data;
      }, function errorCallback(response) {
        vm.selectedConfig = "Could not get selected config from server";
      });
    }

    vm.reconnect = function() {
      $http({
        method: 'GET',
        url: '/reconnect' 
      }).then(function successCallback(response) {
        getSelectedConfig();
      }, function errorCallback(response) {
        vm.selectedConfig = "Could not get selected config from server";
      });
    }

    vm.closeConnection = function() {
      $http({
        method: 'GET',
        url: '/closeConnection' 
      }).then(function successCallback(response) {
        getSelectedConfig();
      }, function errorCallback(response) {
        vm.selectedConfig = "Could not get selected config from server";
      });
    }

    function searchTextChange(text) {
      $log.info('Text changed to ' + text);
    }
    function selectedItemChange(item) {
      $log.info('Item changed to ' + angular.toJson(item));
    }
  })

})();
