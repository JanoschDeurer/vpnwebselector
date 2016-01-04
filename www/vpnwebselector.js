/*
 * This file is the javascript part of the VpnWebSelector
 * Copyright © 2016 Janosch Deurer
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * 
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

(function(){
  angular.module('VpnWebSelector', ['ngMaterial']).controller('QuerryController', function($http, $timeout, $q, $log, $scope, $interval) {
    var vm = this;
    // list of `state` value/display objects
    vm.querySearch = querySearch;
    vm.selectedItemChange = selectedItemChange;
    vm.searchTextChange   = searchTextChange;
    vm.shellOutput = "";
    getSelectedConfig();
    getShellOutput();
    bla = $interval(getShellOutput, 500);
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
      vm.selectedConfig = "loading ..."
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
      vm.selectedConfig = "loading ..."
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
      vm.selectedConfig = "loading ..."
      $http({
        method: 'GET',
        url: '/closeConnection' 
      }).then(function successCallback(response) {
        getSelectedConfig();
      }, function errorCallback(response) {
        vm.selectedConfig = "Could not get selected config from server";
      });
    }

    function getShellOutput() {
      $http({
        method: 'GET',
        url: '/output.txt', 
      }).then(function successCallback(response) {
        vm.shellOutput = response.data;
      }, function errorCallback(response) {
        vm.shellOutput = "Error while getting shell output";
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
