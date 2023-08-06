class entitiesController:
    """"""

    _controller_name = "entitiesController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def topicRetrieve(self, entityId):
        """

        Args:
            entityId: (string): 

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
                "id": {
                  "type": "string"
                },
                "mainName": {
                  "id": {
                    "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                    "type": "string"
                  },
                  "name": {
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

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entities/topic/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def getTopicEntities(self, name, languageId, **kwargs):
        """

        Args:
            name: (string): 
            languageId: (string): 
            topicTypeId: (string): 
            maxEntitiesNumber: (integer): 
            onlyMainNames: (boolean): 
            sortByPopularity: (boolean): 

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
                  "$ref": "#/components/schemas/TopicEntityPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': True, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}, 'maxEntitiesNumber': {'name': 'maxEntitiesNumber', 'required': False, 'in': 'query'}, 'onlyMainNames': {'name': 'onlyMainNames', 'required': False, 'in': 'query'}, 'sortByPopularity': {'name': 'sortByPopularity', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entities/getTopicEntities'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
