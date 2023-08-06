class projectsController:
    """"""

    _controller_name = "projectsController"
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
                "elasticsearchIndexName": {
                  "example": "project-5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "id": {
                  "example": "5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "isRunning": {
                  "example": true,
                  "type": "boolean"
                },
                "name": {
                  "example": "ProjectName",
                  "type": "string"
                },
                "pipelineId": {
                  "example": "be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "timestamps": {
                  "createdAt": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "modifiedAt": {
                    "format": "int64",
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
        api = '/projects/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def processText(self, projectId, **kwargs):
        """

        Args:
            projectId: (string): 
            languageId: (string): 
            date: (integer): 
            privacyMode: (boolean): 
            logging: (boolean): 
            minRelevancy: (number): 
            office365Groups: (array): 
            office365MailFolder: (string): 
            office365EmailsIncludeMode: (string): 
            office365EmailType: (string): 
            fileName: (string): 
            fileExt: (string): 
            mimeType: (string): 
            filterFields: (string): 
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
                "type": "object"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'date': {'name': 'date', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'minRelevancy': {'name': 'minRelevancy', 'required': False, 'in': 'query'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'query'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'query'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'query'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'query'}, 'fileName': {'name': 'fileName', 'required': False, 'in': 'query'}, 'fileExt': {'name': 'fileExt', 'required': False, 'in': 'query'}, 'mimeType': {'name': 'mimeType', 'required': False, 'in': 'query'}, 'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/projects/processText'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def processFile(self):
        """Supported file formats: https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            file: (string): 
            projectId: (unknown): 
            languageId: (unknown): 
            performTextExtract: (unknown): 
            date: (unknown): 
            privacyMode: (unknown): 
            logging: (unknown): 
            minRelevancy: (unknown): 
            office365Groups: (unknown): 
            office365MailFolder: (unknown): 
            office365EmailsIncludeMode: (unknown): 
            office365EmailType: (unknown): 
            filterFields: (unknown): 

        Consumes: multipart/form-data

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

        all_api_parameters = {'file': {'name': 'file', 'required': 'true', 'in': 'formData'}, 'projectId': {'name': 'projectId', 'required': 'false', 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': 'false', 'in': 'formData'}, 'performTextExtract': {'name': 'performTextExtract', 'required': 'false', 'in': 'formData'}, 'date': {'name': 'date', 'required': 'false', 'in': 'formData'}, 'privacyMode': {'name': 'privacyMode', 'required': 'false', 'in': 'formData'}, 'logging': {'name': 'logging', 'required': 'false', 'in': 'formData'}, 'minRelevancy': {'name': 'minRelevancy', 'required': 'false', 'in': 'formData'}, 'office365Groups': {'name': 'office365Groups', 'required': 'false', 'in': 'formData'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': 'false', 'in': 'formData'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': 'false', 'in': 'formData'}, 'office365EmailType': {'name': 'office365EmailType', 'required': 'false', 'in': 'formData'}, 'filterFields': {'name': 'filterFields', 'required': 'false', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/projects/processFile'
        actions = ['post']
        consumes = ['multipart/form-data']
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
                    "$ref": "#/components/schemas/FeedProjectPojo"
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
        api = '/projects/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            name: (string): 
            isRunning: (boolean): 
            pipelineId: (string): 

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
                "elasticsearchIndexName": {
                  "example": "project-5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "id": {
                  "example": "5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "isRunning": {
                  "example": true,
                  "type": "boolean"
                },
                "name": {
                  "example": "ProjectName",
                  "type": "string"
                },
                "pipelineId": {
                  "example": "be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "timestamps": {
                  "createdAt": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "modifiedAt": {
                    "format": "int64",
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'pipelineId': {'name': 'pipelineId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/edit'
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
                "elasticsearchIndexName": {
                  "example": "project-5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "id": {
                  "example": "5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "isRunning": {
                  "example": true,
                  "type": "boolean"
                },
                "name": {
                  "example": "ProjectName",
                  "type": "string"
                },
                "pipelineId": {
                  "example": "be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "timestamps": {
                  "createdAt": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "modifiedAt": {
                    "format": "int64",
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
        api = '/projects/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def clone(self, id, name):
        """

        Args:
            id: (string): 
            name: (string): 

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
                "elasticsearchIndexName": {
                  "example": "project-5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "id": {
                  "example": "5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "isRunning": {
                  "example": true,
                  "type": "boolean"
                },
                "name": {
                  "example": "ProjectName",
                  "type": "string"
                },
                "pipelineId": {
                  "example": "be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "timestamps": {
                  "createdAt": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "modifiedAt": {
                    "format": "int64",
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/clone'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, name, **kwargs):
        """

        Args:
            name: (string): 
            isRunning: (boolean): 
            pipelineId: (string): 

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
                "elasticsearchIndexName": {
                  "example": "project-5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "id": {
                  "example": "5be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "isRunning": {
                  "example": true,
                  "type": "boolean"
                },
                "name": {
                  "example": "ProjectName",
                  "type": "string"
                },
                "pipelineId": {
                  "example": "be181d6d0b3d47c7554f431",
                  "type": "string"
                },
                "timestamps": {
                  "createdAt": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "modifiedAt": {
                    "format": "int64",
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

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'isRunning': {'name': 'isRunning', 'required': False, 'in': 'query'}, 'pipelineId': {'name': 'pipelineId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/projects/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
