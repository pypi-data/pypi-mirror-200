class processTextsTasksController:
    """"""

    _controller_name = "processTextsTasksController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def submit(self, projectId, **kwargs):
        """

        Args:
            projectId: (string): 
            languageId: (string): 
            date: (integer): 
            privacyMode: (boolean): 
            stopAfterChunkNum: (integer): 
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

        all_api_parameters = {'projectId': {'name': 'projectId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'date': {'name': 'date', 'required': False, 'in': 'query'}, 'privacyMode': {'name': 'privacyMode', 'required': False, 'in': 'query'}, 'stopAfterChunkNum': {'name': 'stopAfterChunkNum', 'required': False, 'in': 'query'}, 'logging': {'name': 'logging', 'required': False, 'in': 'query'}, 'minRelevancy': {'name': 'minRelevancy', 'required': False, 'in': 'query'}, 'office365Groups': {'name': 'office365Groups', 'required': False, 'in': 'query'}, 'office365MailFolder': {'name': 'office365MailFolder', 'required': False, 'in': 'query'}, 'office365EmailsIncludeMode': {'name': 'office365EmailsIncludeMode', 'required': False, 'in': 'query'}, 'office365EmailType': {'name': 'office365EmailType', 'required': False, 'in': 'query'}, 'fileName': {'name': 'fileName', 'required': False, 'in': 'query'}, 'fileExt': {'name': 'fileExt', 'required': False, 'in': 'query'}, 'mimeType': {'name': 'mimeType', 'required': False, 'in': 'query'}, 'filterFields': {'name': 'filterFields', 'required': False, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/process-text-tasks/submit'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
