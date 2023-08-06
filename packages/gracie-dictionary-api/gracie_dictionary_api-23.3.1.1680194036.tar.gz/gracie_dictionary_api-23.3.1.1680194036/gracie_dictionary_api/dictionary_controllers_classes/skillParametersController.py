class skillParametersController:
    """"""

    _controller_name = "skillParametersController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def retrieve(self, skillId, **kwargs):
        """

        Args:
            skillId: (string): 
            languageId: (string): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "Success",
                "type": "string"
              },
              "response": {
                "confidenceCurve": {
                  "bhattacharyyaDistance": {
                    "format": "double",
                    "type": "number"
                  },
                  "confidenceNormalizationCurve": {
                    "items": {
                      "format": "double",
                      "type": "number"
                    },
                    "type": "array"
                  },
                  "defined": {
                    "type": "boolean"
                  },
                  "updated": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "validationSetQuality": {
                    "format": "double",
                    "type": "number"
                  }
                },
                "normalizationHigherThreshold": {
                  "format": "double",
                  "type": "number"
                },
                "normalizationLowerThreshold": {
                  "format": "double",
                  "type": "number"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillParameters/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, skillId, **kwargs):
        """

        Args:
            skillId: (string): 
            languageId: (string): 
            normalizationLowerThreshold: (number): 
            normalizationHigherThreshold: (number): 
            confidenceCurve: (string): 

        Returns:
            {
              "code": {
                "example": 200,
                "format": "int32",
                "type": "integer"
              },
              "message": {
                "example": "Success",
                "type": "string"
              },
              "response": {
                "confidenceCurve": {
                  "bhattacharyyaDistance": {
                    "format": "double",
                    "type": "number"
                  },
                  "confidenceNormalizationCurve": {
                    "items": {
                      "format": "double",
                      "type": "number"
                    },
                    "type": "array"
                  },
                  "defined": {
                    "type": "boolean"
                  },
                  "updated": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "validationSetQuality": {
                    "format": "double",
                    "type": "number"
                  }
                },
                "normalizationHigherThreshold": {
                  "format": "double",
                  "type": "number"
                },
                "normalizationLowerThreshold": {
                  "format": "double",
                  "type": "number"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'normalizationLowerThreshold': {'name': 'normalizationLowerThreshold', 'required': False, 'in': 'query'}, 'normalizationHigherThreshold': {'name': 'normalizationHigherThreshold', 'required': False, 'in': 'query'}, 'confidenceCurve': {'name': 'confidenceCurve', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillParameters/edit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
