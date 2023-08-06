class invalidateController:
    """"""

    _controller_name = "invalidateController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def invalidate(self, id):
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
                "admin": {
                  "example": true,
                  "type": "boolean"
                },
                "attributes": {
                  "dashboardsRefreshEvery": {
                    "example": "minutes",
                    "type": "string"
                  },
                  "dashboardsRefreshRate": {
                    "example": 2,
                    "format": "int32",
                    "type": "integer"
                  }
                },
                "description": {
                  "example": "Administrator of database",
                  "type": "string"
                },
                "enable": {
                  "example": true,
                  "type": "boolean"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "login": {
                  "example": "admin",
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
        api = '/invalidate'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
