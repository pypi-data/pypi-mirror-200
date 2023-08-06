class topicTypeController:
    """"""

    _controller_name = "topicTypeController"
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
                "description": {
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "averageProximity": {
                    "format": "double",
                    "type": "number"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entitiesCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entityBriefsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entityNamesCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "itemsLanguages": {
                    "items": {
                      "$ref": "#/components/schemas/LanguagePojo"
                    },
                    "type": "array"
                  }
                },
                "name": {
                  "example": "Some description.",
                  "type": "string"
                },
                "proximities": {
                  "items": {
                    "$ref": "#/components/schemas/TopicLanguagePojo"
                  },
                  "type": "array"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
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
        api = '/topicType/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            topicId: (string): 
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
                    "$ref": "#/components/schemas/TopicTypeMetaPojo"
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

        all_api_parameters = {'topicId': {'name': 'topicId', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'filter': {'name': 'filter', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicType/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            description: (string): 

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
                "description": {
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "averageProximity": {
                    "format": "double",
                    "type": "number"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entitiesCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entityBriefsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entityNamesCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "itemsLanguages": {
                    "items": {
                      "$ref": "#/components/schemas/LanguagePojo"
                    },
                    "type": "array"
                  }
                },
                "name": {
                  "example": "Some description.",
                  "type": "string"
                },
                "proximities": {
                  "items": {
                    "$ref": "#/components/schemas/TopicLanguagePojo"
                  },
                  "type": "array"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicType/edit'
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
                "description": {
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "averageProximity": {
                    "format": "double",
                    "type": "number"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entitiesCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entityBriefsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entityNamesCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "itemsLanguages": {
                    "items": {
                      "$ref": "#/components/schemas/LanguagePojo"
                    },
                    "type": "array"
                  }
                },
                "name": {
                  "example": "Some description.",
                  "type": "string"
                },
                "proximities": {
                  "items": {
                    "$ref": "#/components/schemas/TopicLanguagePojo"
                  },
                  "type": "array"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
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
        api = '/topicType/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, topicId, name, **kwargs):
        """

        Args:
            topicId: (string): 
            name: (string): 
            description: (string): 

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
                "description": {
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "averageProximity": {
                    "format": "double",
                    "type": "number"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entitiesCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entityBriefsCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "entityNamesCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "itemsLanguages": {
                    "items": {
                      "$ref": "#/components/schemas/LanguagePojo"
                    },
                    "type": "array"
                  }
                },
                "name": {
                  "example": "Some description.",
                  "type": "string"
                },
                "proximities": {
                  "items": {
                    "$ref": "#/components/schemas/TopicLanguagePojo"
                  },
                  "type": "array"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'topicId': {'name': 'topicId', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'description': {'name': 'description', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicType/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
