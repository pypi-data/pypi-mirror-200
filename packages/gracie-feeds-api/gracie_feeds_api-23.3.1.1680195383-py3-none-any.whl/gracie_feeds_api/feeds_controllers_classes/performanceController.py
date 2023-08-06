class performanceController:
    """"""

    _controller_name = "performanceController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

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
                "averageProcessingMsPerText": {
                  "format": "int64",
                  "type": "integer"
                },
                "enabled": {
                  "type": "boolean"
                },
                "maxProcessingMsPerText": {
                  "format": "int64",
                  "type": "integer"
                },
                "parallelSymbolsPerSecond": {
                  "format": "int64",
                  "type": "integer"
                },
                "rules": {
                  "items": {
                    "$ref": "#/components/schemas/SeRuleStatistics"
                  },
                  "type": "array"
                },
                "sumProcessingMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "sumSymbols": {
                  "format": "int64",
                  "type": "integer"
                },
                "textsNumber": {
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
        api = '/performance/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def enable(self, enabled):
        """

        Args:
            enabled: (boolean): 

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
                "averageProcessingMsPerText": {
                  "format": "int64",
                  "type": "integer"
                },
                "enabled": {
                  "type": "boolean"
                },
                "maxProcessingMsPerText": {
                  "format": "int64",
                  "type": "integer"
                },
                "parallelSymbolsPerSecond": {
                  "format": "int64",
                  "type": "integer"
                },
                "rules": {
                  "items": {
                    "$ref": "#/components/schemas/SeRuleStatistics"
                  },
                  "type": "array"
                },
                "sumProcessingMs": {
                  "format": "int64",
                  "type": "integer"
                },
                "sumSymbols": {
                  "format": "int64",
                  "type": "integer"
                },
                "textsNumber": {
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

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/performance/enable'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
