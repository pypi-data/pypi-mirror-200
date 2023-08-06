class tasksController:
    """"""

    _controller_name = "tasksController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def retrieve(self, id):
        """

        Args:
            id: (string): 

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
                "type": "object"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeAllCompletedTasks(self, **kwargs):
        """

        Args:
            taskTypeId: (string): 

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
                  "$ref": "#/components/schemas/FeedTaskPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'taskTypeId': {'name': 'taskTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/removeAllCompletedTasks'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            taskTypeId: (string): 
            maxNumber: (integer): 
            offset: (integer): 
            includeParameters: (boolean): 
            includeMessage: (boolean): 

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
                "tasksList": {
                  "items": {
                    "type": "object"
                  },
                  "type": "array"
                },
                "totalTasksNumber": {
                  "example": 123,
                  "format": "int32",
                  "type": "integer"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'taskTypeId': {'name': 'taskTypeId', 'required': False, 'in': 'query'}, 'maxNumber': {'name': 'maxNumber', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'includeParameters': {'name': 'includeParameters', 'required': False, 'in': 'query'}, 'includeMessage': {'name': 'includeMessage', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, id):
        """

        Args:
            id: (string): 

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
                "createTime": {
                  "example": "yyyy.MM.dd.HH.mm.ss.",
                  "type": "string"
                },
                "createTimeMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "endTime": {
                  "example": "yyyy.MM.dd.HH.mm.ss.",
                  "type": "string"
                },
                "endTimeMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "errorMessage": {
                  "example": "Error",
                  "type": "string"
                },
                "id": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "parameters": {
                  "oneOf": [
                    {
                      "$ref": "#/components/schemas/FeedProcessTextTaskParametersPojo"
                    }
                  ]
                },
                "result": {
                  "oneOf": [
                    {
                      "$ref": "#/components/schemas/FeedSearchTaskResultPojo"
                    }
                  ]
                },
                "runTime": {
                  "example": "HH.mm.ss.",
                  "type": "string"
                },
                "runTimeMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "startTime": {
                  "example": "yyyy.MM.dd.HH.mm.ss.",
                  "type": "string"
                },
                "startTimeMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "status": {
                  "example": "Running",
                  "type": "string"
                },
                "type": {
                  "description": {
                    "example": "Backup databases",
                    "type": "string"
                  },
                  "name": {
                    "example": "BackupDatabases",
                    "type": "string"
                  },
                  "typeId": {
                    "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                    "type": "string"
                  }
                },
                "userId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def cancel(self, id):
        """

        Args:
            id: (string): 

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
                "createTime": {
                  "example": "yyyy.MM.dd.HH.mm.ss.",
                  "type": "string"
                },
                "createTimeMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "endTime": {
                  "example": "yyyy.MM.dd.HH.mm.ss.",
                  "type": "string"
                },
                "endTimeMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "errorMessage": {
                  "example": "Error",
                  "type": "string"
                },
                "id": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "parameters": {
                  "oneOf": [
                    {
                      "$ref": "#/components/schemas/FeedProcessTextTaskParametersPojo"
                    }
                  ]
                },
                "result": {
                  "oneOf": [
                    {
                      "$ref": "#/components/schemas/FeedSearchTaskResultPojo"
                    }
                  ]
                },
                "runTime": {
                  "example": "HH.mm.ss.",
                  "type": "string"
                },
                "runTimeMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "startTime": {
                  "example": "yyyy.MM.dd.HH.mm.ss.",
                  "type": "string"
                },
                "startTimeMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "status": {
                  "example": "Running",
                  "type": "string"
                },
                "type": {
                  "description": {
                    "example": "Backup databases",
                    "type": "string"
                  },
                  "name": {
                    "example": "BackupDatabases",
                    "type": "string"
                  },
                  "typeId": {
                    "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                    "type": "string"
                  }
                },
                "userId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tasks/cancel'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
