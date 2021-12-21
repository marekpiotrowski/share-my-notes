(function() {
    'use strict';

    angular
        .module('shareMyNotesApp')
        .controller('SessionController', SessionController);

    angular
        .module('shareMyNotesApp')
        .controller('ModalInstanceCtrl', ModalInstanceCtrl);

    function SessionController($scope, $uibModal, $http) {
        $scope.openedSessions = [];

        $scope.dt = null;

        $scope.open = function() {
            var modalInstance = $uibModal.open({
                animation: false,
                backdropClass: 'modal-backdrop',
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: 'myModalContent.html',
                controller: 'ModalInstanceCtrl',
                controllerAs: 'ctrl',
                size: 'lg'
            });

            modalInstance.result.then(function(sessionData) {
                $http({
                    method: "GET",
                    url: "/sessions"
                }).then(function mySuccess(response) {
                    var alreadyExistingSession = response.data;
                    if (alreadyExistingSession.filter((s) => {
                            return s.name == sessionData['sessionName'];
                        }).length != 0) {
                        // TODO add toast
                        console.log("session already exists");
                        return;
                    }
                    // TODO add error handler
                    $http({
                        method: "POST",
                        url: "/session",
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        data: {
                            name: sessionData['sessionName'],
                            password: sessionData['sessionPassword']
                        }
                    }).then((response) => {
                        console.log("session created.", response.data);
                        $scope.openedSessions.push(response.data);
                        console.log($scope.openedSessions);
                    });
                }, function myError(response) {
                    console.log(response.statusText);
                });
            }, function() {

            });
        };
    }

    function ModalInstanceCtrl($uibModalInstance) {
        var $ctrl = this;
        $ctrl.sessionName = "";
        $ctrl.sessionPassword = "";

        $ctrl.ok = function() {
            $uibModalInstance.close({
                'sessionName': $ctrl.sessionName,
                'sessionPassword': $ctrl.sessionPassword
            });
        };

        $ctrl.cancel = function() {
            $uibModalInstance.dismiss('cancel');
        };
    };

})();
