(function () {
    'use strict';

    angular
        .module('shareMyNotesApp')
        .controller('SessionController', SessionController);

    angular
        .module('shareMyNotesApp')
        .controller('ModalInstanceCtrl', ModalInstanceCtrl);

    function SessionController($scope, $uibModal) {
        var vm = this;

        vm.openModal = openModal;
        vm.closeModal = closeModal;

        initController();

        $scope.open = function (size, parentSelector) {
          var parentElem = parentSelector ?
            angular.element($document[0].querySelector('.modal-demo ' + parentSelector)) : undefined;
          var modalInstance = $uibModal.open({
            animation: false,
            backdropClass: 'modal-backdrop',
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: 'myModalContent.html',
            controller: 'ModalInstanceCtrl',
            size: 'lg',
            resolve: {
              items: function () {
                return "Abc";//["abc", "cde"];//$ctrl.items;
              }
            }
          });

          modalInstance.result.then(function (selectedItem) {
            // $ctrl.selected = selectedItem;
          }, function () {
            // $log.info('Modal dismissed at: ' + new Date());
          });
        };

        function initController() {
            vm.bodyText = 'This text can be updated in modal 1';
        }

        function openModal(id){
            console.log("open modal");
        }

        function closeModal(id){
            console.log("close modal");
        }
    }

    function ModalInstanceCtrl($uibModalInstance, items) {
      var $ctrl = this;
      $ctrl.items = items;
      $ctrl.selected = {
        item: $ctrl.items[0]
      };

      $ctrl.ok = function () {
        $uibModalInstance.close($ctrl.selected.item);
      };

      $ctrl.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    };

})();
