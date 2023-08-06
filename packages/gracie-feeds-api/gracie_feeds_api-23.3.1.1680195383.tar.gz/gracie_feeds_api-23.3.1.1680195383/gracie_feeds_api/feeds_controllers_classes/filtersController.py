class filtersController:
    """"""

    _controller_name = "filtersController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def setFiltersTree(self, alertRuleId, filters):
        """

        Args:
            alertRuleId: (string): 
            filters: (string): 

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
                "filters": {
                  "items": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/FilterPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterAndPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterCountryPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterGeoEntityPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterInputsGroupPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterMatchPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterNotPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterOrPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterSentimentIndexPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterSkillPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTimeIndexPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicEntityPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicTypePojo"
                      }
                    ]
                  },
                  "type": "array"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}, 'filters': {'name': 'filters', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/setFiltersTree'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeFiltersTree(self, alertRuleId):
        """

        Args:
            alertRuleId: (string): 

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
                "filters": {
                  "items": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/FilterPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterAndPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterCountryPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterGeoEntityPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterInputsGroupPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterMatchPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterNotPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterOrPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterSentimentIndexPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterSkillPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTimeIndexPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicEntityPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicTypePojo"
                      }
                    ]
                  },
                  "type": "array"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/removeFiltersTree'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def getFiltersTree(self, alertRuleId):
        """

        Args:
            alertRuleId: (string): 

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
                "filters": {
                  "items": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/FilterPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterAndPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterCountryPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterGeoEntityPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterInputsGroupPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterMatchPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterNotPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterOrPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterSentimentIndexPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterSkillPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTimeIndexPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicEntityPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicPojo"
                      },
                      {
                        "$ref": "#/components/schemas/FilterTopicTypePojo"
                      }
                    ]
                  },
                  "type": "array"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'alertRuleId': {'name': 'alertRuleId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/filters/getFiltersTree'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
