class skillsetController:
    """"""

    _controller_name = "skillsetController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def visualize(self, skillsetId, **kwargs):
        """

        Args:
            languageId: (string): 
            skillsetId: (string): 

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
                "primaryClusters": {
                  "items": {
                    "$ref": "#/components/schemas/PrimaryClusterPojo"
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

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'skillsetId': {'name': 'skillsetId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillset/visualize'
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
                "example": "Success",
                "type": "string"
              },
              "response": {
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "averageProximity": {
                    "format": "double",
                    "type": "number"
                  },
                  "blacklistKeywordsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "itemsLanguages": {
                    "items": {
                      "$ref": "#/components/schemas/LanguagePojo"
                    },
                    "type": "array"
                  },
                  "keywordsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "skillsCount": {
                    "format": "int32",
                    "type": "integer"
                  }
                },
                "name": {
                  "example": "Skillset name",
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
        api = '/skillset/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            orderBy: (string): 
            orderAsc: (boolean): 
            filter: (string): 

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
                    "$ref": "#/components/schemas/SkillsetPojo"
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

        all_api_parameters = {'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'filter': {'name': 'filter', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillset/list'
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
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "averageProximity": {
                    "format": "double",
                    "type": "number"
                  },
                  "blacklistKeywordsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "itemsLanguages": {
                    "items": {
                      "$ref": "#/components/schemas/LanguagePojo"
                    },
                    "type": "array"
                  },
                  "keywordsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "skillsCount": {
                    "format": "int32",
                    "type": "integer"
                  }
                },
                "name": {
                  "example": "Skillset name",
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
        api = '/skillset/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, name):
        """

        Args:
            name: (string): 

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
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "averageProximity": {
                    "format": "double",
                    "type": "number"
                  },
                  "blacklistKeywordsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "itemsLanguages": {
                    "items": {
                      "$ref": "#/components/schemas/LanguagePojo"
                    },
                    "type": "array"
                  },
                  "keywordsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "skillsCount": {
                    "format": "int32",
                    "type": "integer"
                  }
                },
                "name": {
                  "example": "Skillset name",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/skillset/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
