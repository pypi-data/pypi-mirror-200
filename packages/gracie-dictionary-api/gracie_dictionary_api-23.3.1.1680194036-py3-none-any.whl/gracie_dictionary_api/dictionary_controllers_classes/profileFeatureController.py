class profileFeatureController:
    """"""

    _controller_name = "profileFeatureController"
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
                "example": "Success",
                "type": "string"
              },
              "response": {
                "classOrEntityId": {
                  "type": "string"
                },
                "description": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "profileId": {
                  "type": "string"
                },
                "type": {
                  "enum": [
                    "Skill",
                    "TopicDictionary",
                    "TopicType",
                    "TopicEntity",
                    "GeoEntity"
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
        api = '/profileFeature/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, profileId, **kwargs):
        """

        Args:
            profileId: (string): 
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
                "example": "Success",
                "type": "string"
              },
              "response": {
                "items": {
                  "items": {
                    "$ref": "#/components/schemas/ProfileFeatureVectorElementPojo"
                  },
                  "type": "array"
                },
                "itemsTotalCount": {
                  "example": 1,
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

        all_api_parameters = {'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileFeature/list'
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
                "example": "Success",
                "type": "string"
              },
              "response": {
                "classOrEntityId": {
                  "type": "string"
                },
                "description": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "profileId": {
                  "type": "string"
                },
                "type": {
                  "enum": [
                    "Skill",
                    "TopicDictionary",
                    "TopicType",
                    "TopicEntity",
                    "GeoEntity"
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
        api = '/profileFeature/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, profileId, classOrEntityId):
        """

        Args:
            profileId: (string): 
            classOrEntityId: (string): 

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
                "classOrEntityId": {
                  "type": "string"
                },
                "description": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "profileId": {
                  "type": "string"
                },
                "type": {
                  "enum": [
                    "Skill",
                    "TopicDictionary",
                    "TopicType",
                    "TopicEntity",
                    "GeoEntity"
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

        all_api_parameters = {'profileId': {'name': 'profileId', 'required': True, 'in': 'query'}, 'classOrEntityId': {'name': 'classOrEntityId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profileFeature/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
