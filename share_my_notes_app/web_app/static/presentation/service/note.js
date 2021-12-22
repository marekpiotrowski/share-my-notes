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

  function updateNote(noteData) {
    return $http({
      method: "PUT",
      url: "/note/" + noteData.id,
      headers: {
        'Content-Type': 'application/json'
      },
      data: {
        title: noteData['title'],
        content: noteData['content'],
        expiresOn: noteData.expires_on.toISOString().split('.')[0] // for some reason JS' isoformat is not python's
      }
    });
  }

  return {
    createNote: createNote,
    updateNote: updateNote
  };
}]);
