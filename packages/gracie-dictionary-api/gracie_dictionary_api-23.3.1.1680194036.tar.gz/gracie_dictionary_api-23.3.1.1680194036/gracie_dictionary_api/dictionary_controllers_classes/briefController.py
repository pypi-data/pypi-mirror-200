class briefController:
    """"""

    _controller_name = "briefController"
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
                "id": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "languageId": {
                  "example": "FA6DFB6D6B6807B84DC9811814452EC7B0712AD31C6DF6AF3819723B2495BE97C0C1BAA32CBD867F4869020B34E54E67D0114A733C0D164F58B992DB4435DE37",
                  "type": "string"
                },
                "proximity": {
                  "addends": {
                    "items": {
                      "$ref": "#/components/schemas/ProximityAddendPojo"
                    },
                    "type": "array"
                  },
                  "timestamps": {
                    "updatedAt": {
                      "format": "int64",
                      "type": "integer"
                    }
                  },
                  "value": {
                    "format": "double",
                    "type": "number"
                  }
                },
                "text": {
                  "example": "Short brief.",
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
        api = '/brief/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, entityId, **kwargs):
        """

        Args:
            entityId: (string): 
            orderBy: (string): 
            orderAsc: (boolean): 
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
                "items": {
                  "items": {
                    "$ref": "#/components/schemas/BriefExtraPojo"
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

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': True, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/brief/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, text):
        """

        Args:
            id: (string): 
            text: (string): 

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
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "languageId": {
                  "example": "FA6DFB6D6B6807B84DC9811814452EC7B0712AD31C6DF6AF3819723B2495BE97C0C1BAA32CBD867F4869020B34E54E67D0114A733C0D164F58B992DB4435DE37",
                  "type": "string"
                },
                "proximity": {
                  "addends": {
                    "items": {
                      "$ref": "#/components/schemas/ProximityAddendPojo"
                    },
                    "type": "array"
                  },
                  "timestamps": {
                    "updatedAt": {
                      "format": "int64",
                      "type": "integer"
                    }
                  },
                  "value": {
                    "format": "double",
                    "type": "number"
                  }
                },
                "text": {
                  "example": "Short brief.",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/brief/edit'
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
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "languageId": {
                  "example": "FA6DFB6D6B6807B84DC9811814452EC7B0712AD31C6DF6AF3819723B2495BE97C0C1BAA32CBD867F4869020B34E54E67D0114A733C0D164F58B992DB4435DE37",
                  "type": "string"
                },
                "proximity": {
                  "addends": {
                    "items": {
                      "$ref": "#/components/schemas/ProximityAddendPojo"
                    },
                    "type": "array"
                  },
                  "timestamps": {
                    "updatedAt": {
                      "format": "int64",
                      "type": "integer"
                    }
                  },
                  "value": {
                    "format": "double",
                    "type": "number"
                  }
                },
                "text": {
                  "example": "Short brief.",
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
        api = '/brief/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, entityId, text, **kwargs):
        """

        Args:
            entityId: (string): 
            text: (string): 
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
                "id": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "languageId": {
                  "example": "FA6DFB6D6B6807B84DC9811814452EC7B0712AD31C6DF6AF3819723B2495BE97C0C1BAA32CBD867F4869020B34E54E67D0114A733C0D164F58B992DB4435DE37",
                  "type": "string"
                },
                "proximity": {
                  "addends": {
                    "items": {
                      "$ref": "#/components/schemas/ProximityAddendPojo"
                    },
                    "type": "array"
                  },
                  "timestamps": {
                    "updatedAt": {
                      "format": "int64",
                      "type": "integer"
                    }
                  },
                  "value": {
                    "format": "double",
                    "type": "number"
                  }
                },
                "text": {
                  "example": "Short brief.",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'entityId': {'name': 'entityId', 'required': True, 'in': 'query'}, 'text': {'name': 'text', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/brief/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
