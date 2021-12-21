angular.module('shareMyNotesApp').factory('noteService', ['$http', function($http) {
  function createNote(sessionId) {
    return $http({
        method: "POST",
        url: "/note",
        headers: {
            'Content-Type': 'application/json'
        },
        data: {
            title: "Example title",
            content: "Example content",
            sessionId: sessionId
        }
    });
  }

  return {
    createNote: createNote
  };
}]);
