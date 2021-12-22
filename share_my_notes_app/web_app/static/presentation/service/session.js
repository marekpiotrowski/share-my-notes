angular.module('shareMyNotesApp').factory('sessionService', ['$http', function($http) {
  function createSession(sessionName, sessionPassword) {
    return $http({
      method: "POST",
      url: "/session",
      headers: {
        'Content-Type': 'application/json'
      },
      data: {
        name: sessionName,
        password: sessionPassword
      }
    });
  }

  function getAllSessions() {
    return $http({
      method: "GET",
      url: "/sessions"
    });
  }

  function getSessionByName(sessionName, sessionPassword) {
    return $http({
      method: "GET",
      url: "/session?name=" + sessionName + "&password=" + sessionPassword,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  function getSessionNotes(sessionId, password) {
    return $http({
      method: "GET",
      url: "/notes/session/" + sessionId + "?password=" + password,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  return {
    createSession: createSession,
    getAllSessions: getAllSessions,
    getSessionByName: getSessionByName,
    getSessionNotes: getSessionNotes
  };
}]);
