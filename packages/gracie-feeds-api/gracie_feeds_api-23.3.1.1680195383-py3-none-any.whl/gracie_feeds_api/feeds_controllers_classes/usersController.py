class usersController:
    """"""

    _controller_name = "usersController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def whoAmI(self):
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

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/users/whoAmI'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieveUserAttributes(self):
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
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/users/retrieveUserAttributes'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, id):
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
        api = '/users/remove'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self):
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
                "items": {
                  "$ref": "#/components/schemas/FeedUserPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/users/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            login: (string): 
            password: (string): 
            description: (string): 
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'login': {'name': 'login', 'required': False, 'in': 'query'}, 'password': {'name': 'password', 'required': False, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/edit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def editUserAttributes(self, **kwargs):
        """

        Args:
            dashboardsRefreshRate: (integer): 
            dashboardsRefreshEvery: (string): 

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
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'dashboardsRefreshRate': {'name': 'dashboardsRefreshRate', 'required': False, 'in': 'query'}, 'dashboardsRefreshEvery': {'name': 'dashboardsRefreshEvery', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/editUserAttributes'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, login, password, **kwargs):
        """

        Args:
            login: (string): 
            password: (string): 
            description: (string): 
            enabled: (boolean): 
            languageId: (string): 

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

        all_api_parameters = {'login': {'name': 'login', 'required': True, 'in': 'query'}, 'password': {'name': 'password', 'required': True, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/users/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
