class pipelineController:
    """"""

    _controller_name = "pipelineController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def rulesOrigin(self, **kwargs):
        """

        Args:
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
                "items": {
                  "items": {
                    "$ref": "#/components/schemas/SeRuleConfigSchema"
                  },
                  "type": "array"
                },
                "itemsTotalCount": {
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

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/pipeline/rulesOrigin'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def ruleOrigin(self, ruleId, **kwargs):
        """

        Args:
            ruleId: (string): 
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
                "type": "object"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'ruleId': {'name': 'ruleId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/pipeline/ruleOrigin'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

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
                "description": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "rules": {
                  "items": {
                    "items": {
                      "$ref": "#/components/schemas/PipelineRulePojo"
                    },
                    "type": "array"
                  },
                  "itemsTotalCount": {
                    "format": "int32",
                    "type": "integer"
                  }
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
        api = '/pipeline/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            orderBy: (string): 
            orderAsc: (boolean): 

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
                  "items": {
                    "$ref": "#/components/schemas/BasePipelinePojo"
                  },
                  "type": "array"
                },
                "itemsTotalCount": {
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

        all_api_parameters = {'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/pipeline/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, name, **kwargs):
        """

        Args:
            id: (string): 
            name: (string): 
            description: (string): 
            body: (): 

        Consumes: application/json

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
                "description": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "rules": {
                  "items": {
                    "items": {
                      "$ref": "#/components/schemas/PipelineRulePojo"
                    },
                    "type": "array"
                  },
                  "itemsTotalCount": {
                    "format": "int32",
                    "type": "integer"
                  }
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/pipeline/edit'
        actions = ['post']
        consumes = ['application/json']
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
                "description": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "rules": {
                  "items": {
                    "items": {
                      "$ref": "#/components/schemas/PipelineRulePojo"
                    },
                    "type": "array"
                  },
                  "itemsTotalCount": {
                    "format": "int32",
                    "type": "integer"
                  }
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
        api = '/pipeline/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def defaultRules(self):
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
                  "items": {
                    "$ref": "#/components/schemas/PipelineRulePojo"
                  },
                  "type": "array"
                },
                "itemsTotalCount": {
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
        api = '/pipeline/defaultRules'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, name, **kwargs):
        """

        Args:
            name: (string): 
            description: (string): 
            body: (): 

        Consumes: application/json

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
                "description": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "rules": {
                  "items": {
                    "items": {
                      "$ref": "#/components/schemas/PipelineRulePojo"
                    },
                    "type": "array"
                  },
                  "itemsTotalCount": {
                    "format": "int32",
                    "type": "integer"
                  }
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/pipeline/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
