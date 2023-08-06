class bulkProcessingController:
    """"""

    _controller_name = "bulkProcessingController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def uploadZip(self):
        """Supported file formats: https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            file: (string): 
            projectId: (unknown): 
            languageId: (unknown): 
            true  extract text from file by tika, false  process file as plain text in utf8 encoding.: (unknown): 
            privacyMode: (unknown): 
            userMetadata: (unknown): 

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
                "documentId": {
                  "type": "string"
                },
                "fileName": {
                  "type": "string"
                },
                "timestamp": {
                  "format": "int64",
                  "type": "integer",
                  "writeOnly": true
                },
                "uploadTime": {
                  "format": "int64",
                  "type": "integer"
                },
                "uploadTimestamp": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'file': {'name': 'file', 'required': 'true', 'in': 'formData'}, 'projectId': {'name': 'projectId', 'required': 'false', 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': 'false', 'in': 'formData'}, 'true - Extract text from file by Tika, false - Process file as plain text in UTF-8 encoding.': {'name': 'true - Extract text from file by Tika, false - Process file as plain text in UTF-8 encoding.', 'required': 'false', 'in': 'formData'}, 'privacyMode': {'name': 'privacyMode', 'required': 'false', 'in': 'formData'}, 'userMetadata': {'name': 'userMetadata', 'required': 'false', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/bulkProcessing/uploadZip'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def uploadText(self, projectId, **kwargs):
        """

        Args:
            projectId: (string): 
            languageId: (string): 
            privacyMode: (boolean): 
            fileName: (string): 
            mimeType: (string): 
            userMetadata: (string): 
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
                "documentId": {
                  "type": "string"
                },
                "fileName": {
                  "type": "string"
                },
                "timestamp": {
                  "format": "int64",
                  "type": "integer",
                  "writeOnly": true
                },
                "uploadTime": {
                  "format": "int64",
                  "type": "integer"
                },
                "uploadTimestamp": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'fileName': {'name': 'fileName', 'required': False, 'in': 'query'}, 'mimeType': {'name': 'mimeType', 'required': False, 'in': 'query'}, 'userMetadata': {'name': 'userMetadata', 'required': False, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/bulkProcessing/uploadText'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def uploadFiles(self):
        """Supported file formats: https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            files: (array): 
            projectId: (unknown): 
            languageId: (unknown): 
            filePath: (unknown): 
            performTextExtract: (unknown): 
            privacyMode: (unknown): 
            userMetadata: (unknown): 

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
                "items": {
                  "$ref": "#/components/schemas/UploadResult"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'files': {'name': 'files', 'required': 'true', 'in': 'formData'}, 'projectId': {'name': 'projectId', 'required': 'false', 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': 'false', 'in': 'formData'}, 'filePath': {'name': 'filePath', 'required': 'false', 'in': 'formData'}, 'performTextExtract': {'name': 'performTextExtract', 'required': 'false', 'in': 'formData'}, 'privacyMode': {'name': 'privacyMode', 'required': 'false', 'in': 'formData'}, 'userMetadata': {'name': 'userMetadata', 'required': 'false', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/bulkProcessing/uploadFiles'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def stats(self):
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
                "desiredChunkSize": {
                  "format": "int32",
                  "type": "integer"
                },
                "fakeChunks": {
                  "format": "int32",
                  "type": "integer"
                },
                "maxChunks": {
                  "format": "int32",
                  "type": "integer"
                },
                "minChunkSize": {
                  "format": "int32",
                  "type": "integer"
                },
                "numThreads": {
                  "format": "int32",
                  "type": "integer"
                },
                "readStream": {
                  "type": "boolean"
                },
                "skipEngine": {
                  "type": "boolean"
                },
                "tasksError": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksQueued": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksRunning": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksWaiting": {
                  "format": "int64",
                  "type": "integer"
                },
                "totalNumTasks": {
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
        api = '/bulkProcessing/stats'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def resume(self):
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
                "desiredChunkSize": {
                  "format": "int32",
                  "type": "integer"
                },
                "fakeChunks": {
                  "format": "int32",
                  "type": "integer"
                },
                "maxChunks": {
                  "format": "int32",
                  "type": "integer"
                },
                "minChunkSize": {
                  "format": "int32",
                  "type": "integer"
                },
                "numThreads": {
                  "format": "int32",
                  "type": "integer"
                },
                "readStream": {
                  "type": "boolean"
                },
                "skipEngine": {
                  "type": "boolean"
                },
                "tasksError": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksQueued": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksRunning": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksWaiting": {
                  "format": "int64",
                  "type": "integer"
                },
                "totalNumTasks": {
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
        api = '/bulkProcessing/resume'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def performanceStats(self, **kwargs):
        """

        Args:
            reportType: (string): 
            onlySince: (string): 

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
                  "$ref": "#/components/schemas/PerformanceStats"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'reportType': {'name': 'reportType', 'required': False, 'in': 'query'}, 'onlySince': {'name': 'onlySince', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/performanceStats'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def pause(self):
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
                "desiredChunkSize": {
                  "format": "int32",
                  "type": "integer"
                },
                "fakeChunks": {
                  "format": "int32",
                  "type": "integer"
                },
                "maxChunks": {
                  "format": "int32",
                  "type": "integer"
                },
                "minChunkSize": {
                  "format": "int32",
                  "type": "integer"
                },
                "numThreads": {
                  "format": "int32",
                  "type": "integer"
                },
                "readStream": {
                  "type": "boolean"
                },
                "skipEngine": {
                  "type": "boolean"
                },
                "tasksError": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksQueued": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksRunning": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksWaiting": {
                  "format": "int64",
                  "type": "integer"
                },
                "totalNumTasks": {
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
        api = '/bulkProcessing/pause'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listUploads(self, **kwargs):
        """

        Args:
            pageSize: (integer): 
            pageNum: (integer): 

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
                  "$ref": "#/components/schemas/UploadResult"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'pageSize': {'name': 'pageSize', 'required': False, 'in': 'query'}, 'pageNum': {'name': 'pageNum', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/listUploads'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def getErrors(self, **kwargs):
        """

        Args:
            pageSize: (integer): 
            pageNum: (integer): 

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
                  "$ref": "#/components/schemas/ErrorPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'pageSize': {'name': 'pageSize', 'required': False, 'in': 'query'}, 'pageNum': {'name': 'pageNum', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/getErrors'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, **kwargs):
        """Change BulkProcessing configuration parameters

        Args:
            numThreads: (integer): 
            chunkSize: (integer): 
            minChunkSize: (integer): 
            maxChunks: (integer): 

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
                "desiredChunkSize": {
                  "format": "int32",
                  "type": "integer"
                },
                "fakeChunks": {
                  "format": "int32",
                  "type": "integer"
                },
                "maxChunks": {
                  "format": "int32",
                  "type": "integer"
                },
                "minChunkSize": {
                  "format": "int32",
                  "type": "integer"
                },
                "numThreads": {
                  "format": "int32",
                  "type": "integer"
                },
                "readStream": {
                  "type": "boolean"
                },
                "skipEngine": {
                  "type": "boolean"
                },
                "tasksError": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksQueued": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksRunning": {
                  "format": "int64",
                  "type": "integer"
                },
                "tasksWaiting": {
                  "format": "int64",
                  "type": "integer"
                },
                "totalNumTasks": {
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

        all_api_parameters = {'numThreads': {'name': 'numThreads', 'required': False, 'in': 'query'}, 'chunkSize': {'name': 'chunkSize', 'required': False, 'in': 'query'}, 'minChunkSize': {'name': 'minChunkSize', 'required': False, 'in': 'query'}, 'maxChunks': {'name': 'maxChunks', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/edit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def deletePerformanceStats(self, **kwargs):
        """

        Args:
            reportType: (string): 
            olderThan: (string): 

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
                "numDeleted": {
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

        all_api_parameters = {'reportType': {'name': 'reportType', 'required': False, 'in': 'query'}, 'olderThan': {'name': 'olderThan', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/deletePerformanceStats'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def clearErrors(self):
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
                "errorCount": {
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
        api = '/bulkProcessing/clearErrors'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def cancel(self, documentId):
        """

        Args:
            documentId: (string): 

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
                "documentId": {
                  "type": "string"
                },
                "fileName": {
                  "type": "string"
                },
                "timestamp": {
                  "format": "int64",
                  "type": "integer",
                  "writeOnly": true
                },
                "uploadTime": {
                  "format": "int64",
                  "type": "integer"
                },
                "uploadTimestamp": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'documentId': {'name': 'documentId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/bulkProcessing/cancel'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def cancelAll(self):
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
                  "$ref": "#/components/schemas/UploadResult"
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
        api = '/bulkProcessing/cancelAll'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
