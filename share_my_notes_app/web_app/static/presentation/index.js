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

    $scope.openDatepicker = (note) => {
      note.popupOpened = true;
    }

    $scope.dateOptions = {
      minDate: new Date()
    };

    $scope.addNote = (sessionId) => {
      noteService.createNote(sessionId).then((notePostResponse) => {
        var editedSession = $scope.openedSessions.filter((os) => {
          return os.id == sessionId;
        })[0];
        var createdNote = notePostResponse.data;
        createdNote['expires_on'] = new Date(createdNote['expires_on']);
        editedSession.notes.push(createdNote);
        toastr.success("Note created!");
      });
    }

    $scope.updateNote = (note) => {
      noteService.updateNote(note).then(() => {
        toastr.success("Note updated!");
      });
    }

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
          },
          sessionService: function() {
            return sessionService;
          }
        }
      });

      function createNewSession(sessionData) {
        sessionService.getAllSessions().then((response) => {
          var alreadyExistingSession = response.data;
          if (alreadyExistingSession.filter((s) => {
              return s.name == sessionData['sessionName'];
            }).length != 0) {
            toastr.fail("Session with the given name already exists!");
            return;
          }
          sessionService.createSession(sessionData['sessionName'], sessionData['sessionPassword']).then((response) => {
            noteService.createNote(response.data.id).then((notePostResponse) => {
              var createdNote = notePostResponse.data;
              createdNote['expires_on'] = new Date(createdNote['expires_on']);
              response.data.notes = [createdNote];
            });
            $scope.openedSessions.push(response.data);
            toastr.success("Session created!");
          });
        }, (response) => {
          // TODO add error handler
        });
      }


      function openSession(sessionData) {
        sessionService.getAllSessions().then((response) => {
          var alreadyExistingSession = response.data;
          if (alreadyExistingSession.filter((s) => {
              return s.name == sessionData['sessionName'];
            }).length == 0) {
            toastr.fail("Session does not exist.");
            return;
          }
          sessionService.getSessionByName(sessionData['sessionName'],
              sessionData['sessionPassword']).then((response) => {
            sessionService.getSessionNotes(response.data.id, sessionData['sessionPassword']).then((noteResponse) => {
              console.log(noteResponse.data);
              var sessionNotes = noteResponse.data;
              sessionNotes.map((e) => {
                e['expires_on'] = new Date(e['expires_on']);
              });
              response.data.notes = sessionNotes;
            });
            $scope.openedSessions.push(response.data);
          });
        }, (response) => {
          // TODO add error handler
        });
      }

      modalInstance.result.then(function(sessionData) {
        if (sessionData['type'] == 'create') {
          createNewSession(sessionData);
        } else {
          openSession(sessionData);
        }
      }, function() {
        // no-op on cancel
      });
    };
  }

  function ModalInstanceCtrl($uibModalInstance, modalTitle, sessionService) {
    var $ctrl = this;
    $ctrl.sessionName = "";
    $ctrl.sessionPassword = "";
    $ctrl.modalTitle = modalTitle;

    $ctrl.ok = function() {
      var type = modalTitle == "Create new session" ? "create" : "open";
      sessionService.getAllSessions().then((response) => {
        var alreadyExistingSessions = response.data;
        var sessionsWithGivenNameCount = alreadyExistingSessions.filter((s) => {
          return s.name == $ctrl.sessionName;
        }).length;

        if (type == "open" && sessionsWithGivenNameCount == 0) {
          toastr.error("Session does not exist.");
          return;
        } else if (type == "create" && sessionsWithGivenNameCount != 0) {
          toastr.error("Session with the given name already exists.");
          return;
        }

        if (type == "open") {
          sessionService.getSessionByName($ctrl.sessionName, $ctrl.sessionPassword).then(() => {
            $uibModalInstance.close({
              'sessionName': $ctrl.sessionName,
              'sessionPassword': $ctrl.sessionPassword,
              'type': type
            });
          }, (errResponse) => {
            if (errResponse.status == 401) {
              toastr.error("Incorrect password.");
              return;
            }
          });
        } else {
          $uibModalInstance.close({
            'sessionName': $ctrl.sessionName,
            'sessionPassword': $ctrl.sessionPassword,
            'type': type
          });
        }
      });
    };

    $ctrl.cancel = function() {
      $uibModalInstance.dismiss('cancel');
    };
  };

})();
