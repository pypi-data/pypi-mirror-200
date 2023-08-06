class processFilesTasksController:
    """"""

    _controller_name = "processFilesTasksController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def submit(self):
        """Process the text from file. Supported file formats:  - https://tika.apache.org/1.13/formats.html - .tif, .bmp, .jpg, .png

        Args:
            file: (string): 
            projectId: (unknown): 
            languageId: (unknown): 
            performTextExtract: (unknown): 
            date: (unknown): 
            privacyMode: (unknown): 
            stopAfterChunkNum: (unknown): 
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

        all_api_parameters = {'file': {'name': 'file', 'required': 'true', 'in': 'formData'}, 'projectId': {'name': 'projectId', 'required': 'false', 'in': 'formData'}, 'languageId': {'name': 'languageId', 'required': 'false', 'in': 'formData'}, 'performTextExtract': {'name': 'performTextExtract', 'required': 'false', 'in': 'formData'}, 'date': {'name': 'date', 'required': 'false', 'in': 'formData'}, 'privacyMode': {'name': 'privacyMode', 'required': 'false', 'in': 'formData'}, 'stopAfterChunkNum': {'name': 'stopAfterChunkNum', 'required': 'false', 'in': 'formData'}, 'logging': {'name': 'logging', 'required': 'false', 'in': 'formData'}, 'minRelevancy': {'name': 'minRelevancy', 'required': 'false', 'in': 'formData'}, 'office365Groups': {'name': 'office365Groups', 'required': 'false', 'in': 'formData'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': 'false', 'in': 'formData'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': 'false', 'in': 'formData'}, 'office365EmailType': {'name': 'office365EmailType', 'required': 'false', 'in': 'formData'}, 'filterFields': {'name': 'filterFields', 'required': 'false', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/process-file-tasks/submit'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
