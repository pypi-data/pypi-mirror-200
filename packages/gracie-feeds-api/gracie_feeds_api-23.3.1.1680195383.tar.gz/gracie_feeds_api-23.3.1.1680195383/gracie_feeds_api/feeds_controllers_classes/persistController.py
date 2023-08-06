class persistController:
    """"""

    _controller_name = "persistController"
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
                "dbHostname": {
                  "type": "string"
                },
                "dbName": {
                  "type": "string"
                },
                "dbPassword": {
                  "type": "string"
                },
                "dbPortNumber": {
                  "format": "int32",
                  "type": "integer"
                },
                "dbType": {
                  "enum": [
                    "POSTGRES"
                  ],
                  "type": "string"
                },
                "dbUsername": {
                  "type": "string"
                },
                "enabled": {
                  "type": "boolean"
                },
                "error": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "INACTIVE",
                    "RUNNING",
                    "ERROR",
                    "DISABLED"
                  ],
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
        api = '/persist/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeFilter(self, filterId):
        """

        Args:
            filterId: (string): 

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
                "oneOf": [
                  {
                    "$ref": "#/components/schemas/FilterPojo"
                  },
                  {
                    "$ref": "#/components/schemas/AttributeFilterPojo"
                  },
                  {
                    "$ref": "#/components/schemas/MetadataFilterPojo"
                  }
                ]
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'filterId': {'name': 'filterId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/removeFilter'
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
                "dbInstances": {
                  "items": {
                    "$ref": "#/components/schemas/DbInstancePojo"
                  },
                  "type": "array"
                },
                "esInstance": {
                  "enabled": {
                    "type": "boolean"
                  },
                  "error": {
                    "type": "string"
                  },
                  "esExchangeName": {
                    "type": "string"
                  },
                  "esQueue": {
                    "type": "string"
                  },
                  "esRoutingKey": {
                    "type": "string"
                  },
                  "id": {
                    "type": "string"
                  },
                  "name": {
                    "type": "string"
                  },
                  "status": {
                    "enum": [
                      "INACTIVE",
                      "RUNNING",
                      "ERROR",
                      "DISABLED"
                    ],
                    "type": "string"
                  }
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
        api = '/persist/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def getFilters(self, id):
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
                "items": {
                  "oneOf": [
                    {
                      "$ref": "#/components/schemas/FilterPojo"
                    },
                    {
                      "$ref": "#/components/schemas/AttributeFilterPojo"
                    },
                    {
                      "$ref": "#/components/schemas/MetadataFilterPojo"
                    }
                  ]
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/getFilters'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def enableES(self, enabled):
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
                "enabled": {
                  "type": "boolean"
                },
                "error": {
                  "type": "string"
                },
                "esExchangeName": {
                  "type": "string"
                },
                "esQueue": {
                  "type": "string"
                },
                "esRoutingKey": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "INACTIVE",
                    "RUNNING",
                    "ERROR",
                    "DISABLED"
                  ],
                  "type": "string"
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
        api = '/persist/enableES'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            name: (string): 
            dbHostname: (string): 
            dbPortNumber: (integer): 
            dbName: (string): 
            dbUsername: (string): 
            dbPassword: (string): 
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
                "dbHostname": {
                  "type": "string"
                },
                "dbName": {
                  "type": "string"
                },
                "dbPassword": {
                  "type": "string"
                },
                "dbPortNumber": {
                  "format": "int32",
                  "type": "integer"
                },
                "dbType": {
                  "enum": [
                    "POSTGRES"
                  ],
                  "type": "string"
                },
                "dbUsername": {
                  "type": "string"
                },
                "enabled": {
                  "type": "boolean"
                },
                "error": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "INACTIVE",
                    "RUNNING",
                    "ERROR",
                    "DISABLED"
                  ],
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'dbHostname': {'name': 'dbHostname', 'required': False, 'in': 'query'}, 'dbPortNumber': {'name': 'dbPortNumber', 'required': False, 'in': 'query'}, 'dbName': {'name': 'dbName', 'required': False, 'in': 'query'}, 'dbUsername': {'name': 'dbUsername', 'required': False, 'in': 'query'}, 'dbPassword': {'name': 'dbPassword', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/edit'
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
                "dbHostname": {
                  "type": "string"
                },
                "dbName": {
                  "type": "string"
                },
                "dbPassword": {
                  "type": "string"
                },
                "dbPortNumber": {
                  "format": "int32",
                  "type": "integer"
                },
                "dbType": {
                  "enum": [
                    "POSTGRES"
                  ],
                  "type": "string"
                },
                "dbUsername": {
                  "type": "string"
                },
                "enabled": {
                  "type": "boolean"
                },
                "error": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "INACTIVE",
                    "RUNNING",
                    "ERROR",
                    "DISABLED"
                  ],
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
        api = '/persist/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def deleteES(self):
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
                "enabled": {
                  "type": "boolean"
                },
                "error": {
                  "type": "string"
                },
                "esExchangeName": {
                  "type": "string"
                },
                "esQueue": {
                  "type": "string"
                },
                "esRoutingKey": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "INACTIVE",
                    "RUNNING",
                    "ERROR",
                    "DISABLED"
                  ],
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
        api = '/persist/deleteES'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def deleteDocuments(self, id, **kwargs):
        """

        Args:
            id: (string): 
            projectName: (string): 
            metaName: (string): 
            metaValue: (string): 

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
                "format": "int32",
                "type": "integer"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'projectName': {'name': 'projectName', 'required': False, 'in': 'query'}, 'metaName': {'name': 'metaName', 'required': False, 'in': 'query'}, 'metaValue': {'name': 'metaValue', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/deleteDocuments'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def createMetadataFilter(self, id, includeExclude, type, metadataKey, values):
        """

        Args:
            id: (string): 
            includeExclude: (string): 
            type: (string): 
            metadataKey: (string): 
            values: (array): 

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
                "oneOf": [
                  {
                    "$ref": "#/components/schemas/FilterPojo"
                  },
                  {
                    "$ref": "#/components/schemas/AttributeFilterPojo"
                  },
                  {
                    "$ref": "#/components/schemas/MetadataFilterPojo"
                  }
                ]
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'includeExclude': {'name': 'includeExclude', 'required': True, 'in': 'query'}, 'type': {'name': 'type', 'required': True, 'in': 'query'}, 'metadataKey': {'name': 'metadataKey', 'required': True, 'in': 'query'}, 'values': {'name': 'values', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/createMetadataFilter'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def createES(self, **kwargs):
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
                "enabled": {
                  "type": "boolean"
                },
                "error": {
                  "type": "string"
                },
                "esExchangeName": {
                  "type": "string"
                },
                "esQueue": {
                  "type": "string"
                },
                "esRoutingKey": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "INACTIVE",
                    "RUNNING",
                    "ERROR",
                    "DISABLED"
                  ],
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/createES'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def createAttributeFilter(self, id, includeExclude, attribute, values):
        """

        Args:
            id: (string): 
            includeExclude: (string): 
            attribute: (string): 
            values: (array): 

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
                "oneOf": [
                  {
                    "$ref": "#/components/schemas/FilterPojo"
                  },
                  {
                    "$ref": "#/components/schemas/AttributeFilterPojo"
                  },
                  {
                    "$ref": "#/components/schemas/MetadataFilterPojo"
                  }
                ]
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'includeExclude': {'name': 'includeExclude', 'required': True, 'in': 'query'}, 'attribute': {'name': 'attribute', 'required': True, 'in': 'query'}, 'values': {'name': 'values', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/createAttributeFilter'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, name, dbType, dbHostname, dbPortNumber, dbName, dbUsername, dbPassword, **kwargs):
        """

        Args:
            name: (string): 
            dbType: (string): 
            dbHostname: (string): 
            dbPortNumber: (integer): 
            dbName: (string): 
            dbUsername: (string): 
            dbPassword: (string): 
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
                "dbHostname": {
                  "type": "string"
                },
                "dbName": {
                  "type": "string"
                },
                "dbPassword": {
                  "type": "string"
                },
                "dbPortNumber": {
                  "format": "int32",
                  "type": "integer"
                },
                "dbType": {
                  "enum": [
                    "POSTGRES"
                  ],
                  "type": "string"
                },
                "dbUsername": {
                  "type": "string"
                },
                "enabled": {
                  "type": "boolean"
                },
                "error": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "INACTIVE",
                    "RUNNING",
                    "ERROR",
                    "DISABLED"
                  ],
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'dbType': {'name': 'dbType', 'required': True, 'in': 'query'}, 'dbHostname': {'name': 'dbHostname', 'required': True, 'in': 'query'}, 'dbPortNumber': {'name': 'dbPortNumber', 'required': True, 'in': 'query'}, 'dbName': {'name': 'dbName', 'required': True, 'in': 'query'}, 'dbUsername': {'name': 'dbUsername', 'required': True, 'in': 'query'}, 'dbPassword': {'name': 'dbPassword', 'required': True, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/persist/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
