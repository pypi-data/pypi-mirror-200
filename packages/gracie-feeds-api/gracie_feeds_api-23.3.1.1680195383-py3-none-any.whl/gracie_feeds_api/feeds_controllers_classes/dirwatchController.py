class dirwatchController:
    """"""

    _controller_name = "dirwatchController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def retrieve(self, dirWatchId):
        """

        Args:
            dirWatchId: (string): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "id": {
                  "type": "string"
                },
                "isRunning": {
                  "type": "boolean"
                },
                "subDir": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'dirWatchId': {'name': 'dirWatchId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/dirWatches/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, dirWatchId):
        """

        Args:
            dirWatchId: (string): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "id": {
                  "type": "string"
                },
                "isRunning": {
                  "type": "boolean"
                },
                "subDir": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'dirWatchId': {'name': 'dirWatchId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/dirWatches/remove'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, projectId):
        """

        Args:
            projectId: (string): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "items": {
                  "$ref": "#/components/schemas/DirwatchBriefPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/dirWatches/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, dirWatchId, **kwargs):
        """

        Args:
            dirWatchId: (string): 
            isRunning: (boolean): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "id": {
                  "type": "string"
                },
                "isRunning": {
                  "type": "boolean"
                },
                "subDir": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'dirWatchId': {'name': 'dirWatchId', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/dirWatches/edit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, projectId, subDir, **kwargs):
        """

        Args:
            projectId: (string): 
            subDir: (string): 
            isRunning: (boolean): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "SomeMessage",
                "type": "string"
              },
              "response": {
                "id": {
                  "type": "string"
                },
                "isRunning": {
                  "type": "boolean"
                },
                "subDir": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'subDir': {'name': 'subDir', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/dirWatches/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
