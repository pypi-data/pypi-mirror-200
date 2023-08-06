class engineAppInfoController:
    """"""

    _controller_name = "engineAppInfoController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def system(self):
        """

        Args:

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
                "currentTime": {
                  "example": "timestamp",
                  "type": "string"
                },
                "freeMemory": {
                  "format": "int64",
                  "type": "integer"
                },
                "offheapFreeMemory": {
                  "format": "int64",
                  "type": "integer"
                },
                "offheapTotalMemory": {
                  "format": "int64",
                  "type": "integer"
                },
                "offheapUsedMemory": {
                  "format": "int64",
                  "type": "integer"
                },
                "totalMemory": {
                  "format": "int64",
                  "type": "integer"
                },
                "usedMemory": {
                  "format": "int64",
                  "type": "integer"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/engine-app/system'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def searchParameters(self):
        """

        Args:

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
                "maxSearchTasks": {
                  "example": 5,
                  "format": "int32",
                  "type": "integer"
                },
                "maxTextLength": {
                  "example": 10000,
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

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/engine-app/searchParameters'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self):
        """

        Args:

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
                "buildCommit": {
                  "example": "fe73932c6f0b57b60486e462bf05e3a9378a15f6",
                  "type": "string"
                },
                "buildDate": {
                  "format": "date-time",
                  "type": "string"
                },
                "buildScmBranch": {
                  "example": "pre-release",
                  "type": "string"
                },
                "serverId": {
                  "example": "sm1",
                  "type": "string"
                },
                "version": {
                  "example": "1.0.1",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/engine-app/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
