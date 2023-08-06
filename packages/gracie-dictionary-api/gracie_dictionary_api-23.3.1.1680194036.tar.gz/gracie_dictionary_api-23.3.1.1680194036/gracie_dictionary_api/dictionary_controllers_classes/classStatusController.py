class classStatusController:
    """"""

    _controller_name = "classStatusController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def retrieve(self, classId, **kwargs):
        """

        Args:
            classId: (string): 
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
                "classId": {
                  "type": "string"
                },
                "className": {
                  "type": "string"
                },
                "classStatus": {
                  "error": {
                    "type": "string"
                  },
                  "lastUpdated": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "warnings": {
                    "items": {
                      "type": "string"
                    },
                    "type": "array"
                  }
                },
                "classType": {
                  "enum": [
                    "Skill",
                    "GeoDictionary",
                    "TopicDictionary",
                    "TopicType",
                    "ProfileClass",
                    "Profile",
                    "Skillset",
                    "Pipeline",
                    "ClusterSet",
                    "ClusterGroup",
                    "Cluster"
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

        all_api_parameters = {'classId': {'name': 'classId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classStatus/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            scope: (string): 
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
                "classes": {
                  "items": {
                    "$ref": "#/components/schemas/ClassStatus"
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

        all_api_parameters = {'scope': {'name': 'scope', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/classStatus/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
