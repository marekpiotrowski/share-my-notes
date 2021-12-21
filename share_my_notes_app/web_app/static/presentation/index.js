(function() {
    'use strict';

    angular
        .module('shareMyNotesApp')
        .controller('SessionController', SessionController);

    angular
        .module('shareMyNotesApp')
        .controller('ModalInstanceCtrl', ModalInstanceCtrl);

    function SessionController($scope, $uibModal, $http, noteService, sessionService) {
        $scope.openedSessions = [];

        $scope.dt = null;

        $scope.open = function(modalTitle) {
            var modalInstance = $uibModal.open({
                animation: false,
                backdropClass: 'modal-backdrop',
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: 'myModalContent.html',
                controller: 'ModalInstanceCtrl',
                controllerAs: 'ctrl',
                size: 'lg',
                resolve: {
                    modalTitle: function() {
                        return modalTitle;
                    }
                }
            });

            function createNewSession(sessionData) {
                sessionService.getAllSessions().then((response) => {
                    var alreadyExistingSession = response.data;
                    if (alreadyExistingSession.filter((s) => {
                            return s.name == sessionData['sessionName'];
                        }).length != 0) {
                        // TODO add toast
                        console.log("session already exists");
                        return;
                    }
                    // TODO add error handler
                    sessionService.createSession(sessionData['sessionName'], sessionData['sessionPassword']).then((response) => {
                        console.log("session created.", response.data);
                        noteService.createNote(response.data.id).then((notePostResponse) => {
                            console.log(notePostResponse.data);
                            response.data.notes = [notePostResponse.data];
                        });
                        $scope.openedSessions.push(response.data);
                        console.log($scope.openedSessions);
                    });
                }, (response) => {
                    console.log(response.statusText);
                });
            }


            function openSession(sessionData) {
                sessionService.getAllSessions().then((response) => {
                    var alreadyExistingSession = response.data;
                    if (alreadyExistingSession.filter((s) => {
                            return s.name == sessionData['sessionName'];
                        }).length == 0) {
                        // TODO add toast
                        console.log("session does not exist");
                        return;
                    }
                    // TODO add error handler
                    sessionService.getSessionByName(sessionData['sessionName']).then((response) => {
                        sessionService.getSessionNotes(response.data.id).then((noteResponse) => {
                            console.log(noteResponse.data);
                            response.data.notes = noteResponse.data;
                        });
                        $scope.openedSessions.push(response.data);
                        console.log($scope.openedSessions);
                    });
                }, (response) => {
                    console.log(response.statusText);
                });
            }

            modalInstance.result.then(function(sessionData) {
                if (sessionData['type'] == 'create') {
                    createNewSession(sessionData);
                } else {
                    openSession(sessionData);
                }
            }, function() {

            });
        };
    }

    function ModalInstanceCtrl($uibModalInstance, modalTitle) {
        var $ctrl = this;
        $ctrl.sessionName = "";
        $ctrl.sessionPassword = "";
        $ctrl.modalTitle = modalTitle;

        $ctrl.ok = function() {
            $uibModalInstance.close({
                'sessionName': $ctrl.sessionName,
                'sessionPassword': $ctrl.sessionPassword,
                'type': modalTitle == "Create new session" ? "create" : "open"
            });
        };

        $ctrl.cancel = function() {
            $uibModalInstance.dismiss('cancel');
        };
    };

})();
