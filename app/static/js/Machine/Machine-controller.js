'use strict';

angular.module('prodmgmt')
  .controller('MachineController', ['$scope', '$modal', 'resolvedMachine', 'Machine',
    function ($scope, $modal, resolvedMachine, Machine) {

      $scope.Machines = resolvedMachine;

      $scope.create = function () {
        $scope.clear();
        $scope.open();
      };

      $scope.update = function (id) {
        $scope.Machine = Machine.get({id: id});
        $scope.open(id);
      };

      $scope.delete = function (id) {
        Machine.delete({id: id},
          function () {
            $scope.Machines = Machine.query();
          });
      };

      $scope.save = function (id) {
        if (id) {
          Machine.update({id: id}, $scope.Machine,
            function () {
              $scope.Machines = Machine.query();
              $scope.clear();
            });
        } else {
          Machine.save($scope.Machine,
            function () {
              $scope.Machines = Machine.query();
              $scope.clear();
            });
        }
      };

      $scope.clear = function () {
        $scope.Machine = {
          
          "name": "",
          
          "supported_mold_type": "",
          
          "installed_mold_id": "",
          
          "status": "",
          
          "downtime_start": "",
          
          "downtime_end": "",
          
          "total_downtime": "",
          
          "created_at": "",
          
          "modified_at": "",
          
          "id": ""
        };
      };

      $scope.open = function (id) {
        var MachineSave = $modal.open({
          templateUrl: 'Machine-save.html',
          controller: 'MachineSaveController',
          resolve: {
            Machine: function () {
              return $scope.Machine;
            }
          }
        });

        MachineSave.result.then(function (entity) {
          $scope.Machine = entity;
          $scope.save(id);
        });
      };
    }])
  .controller('MachineSaveController', ['$scope', '$modalInstance', 'Machine',
    function ($scope, $modalInstance, Machine) {
      $scope.Machine = Machine;

      
      $scope.downtime_startDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.downtime_endDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.created_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };
      $scope.modified_atDateOptions = {
        dateFormat: 'yy-mm-dd',
        
        
      };

      $scope.ok = function () {
        $modalInstance.close($scope.Machine);
      };

      $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
      };
    }]);
