class infoController:
    """"""

    _controller_name = "infoController"
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
        api = '/info/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
