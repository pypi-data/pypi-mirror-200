class tagController:
    """"""

    _controller_name = "tagController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def search(self, **kwargs):
        """

        Args:
            folderId: (string): 
            keyName: (string): 
            offset: (integer): 
            limit: (integer): 
            orderBy: (string): 
            orderAsc: (boolean): 
            systemFilter: (string): 

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
                    "$ref": "#/components/schemas/TagPojo"
                  },
                  "type": "array"
                },
                "itemsTotalCount": {
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

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'keyName': {'name': 'keyName', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'systemFilter': {'name': 'systemFilter', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/search'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def retrieve(self, key, **kwargs):
        """

        Args:
            folderId: (string): 
            key: (string): 

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
                "editable": {
                  "type": "boolean"
                },
                "folderId": {
                  "type": "string"
                },
                "included": {
                  "type": "boolean"
                },
                "key": {
                  "type": "string"
                },
                "system": {
                  "type": "boolean"
                },
                "type": {
                  "enum": [
                    "StringsList",
                    "BooleansList",
                    "IntsList",
                    "DoublesList"
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

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'key': {'name': 'key', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listValues(self, **kwargs):
        """

        Args:
            keyName: (string): 
            type: (string): 

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
                    "$ref": "#/components/schemas/TagValuePojo"
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

        all_api_parameters = {'keyName': {'name': 'keyName', 'required': False, 'in': 'query'}, 'type': {'name': 'type', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/listValues'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            folderId: (string): 
            offset: (integer): 
            limit: (integer): 
            orderBy: (string): 
            orderAsc: (boolean): 
            systemFilter: (string): 

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
                "hasFolders": {
                  "type": "boolean"
                },
                "hasTags": {
                  "type": "boolean"
                },
                "id": {
                  "type": "string"
                },
                "itemsTotalCount": {
                  "format": "int32",
                  "type": "integer"
                },
                "name": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'systemFilter': {'name': 'systemFilter', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, key, **kwargs):
        """

        Args:
            folderId: (string): 
            key: (string): 
            value: (string): 
            included: (boolean): 

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
                "editable": {
                  "type": "boolean"
                },
                "folderId": {
                  "type": "string"
                },
                "included": {
                  "type": "boolean"
                },
                "key": {
                  "type": "string"
                },
                "system": {
                  "type": "boolean"
                },
                "type": {
                  "enum": [
                    "StringsList",
                    "BooleansList",
                    "IntsList",
                    "DoublesList"
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

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'key': {'name': 'key', 'required': True, 'in': 'query'}, 'value': {'name': 'value', 'required': False, 'in': 'query'}, 'included': {'name': 'included', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/edit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, key, **kwargs):
        """

        Args:
            folderId: (string): 
            key: (string): 

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
                "editable": {
                  "type": "boolean"
                },
                "folderId": {
                  "type": "string"
                },
                "included": {
                  "type": "boolean"
                },
                "key": {
                  "type": "string"
                },
                "system": {
                  "type": "boolean"
                },
                "type": {
                  "enum": [
                    "StringsList",
                    "BooleansList",
                    "IntsList",
                    "DoublesList"
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

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'key': {'name': 'key', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkDelete(self, keys, **kwargs):
        """

        Args:
            folderId: (string): 
            keys: (array): 

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
                "type": "boolean"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'keys': {'name': 'keys', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/bulkDelete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, key, type, **kwargs):
        """

        Args:
            folderId: (string): 
            key: (string): 
            type: (string): 
            value: (string): 
            included: (boolean): 

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
                "editable": {
                  "type": "boolean"
                },
                "folderId": {
                  "type": "string"
                },
                "included": {
                  "type": "boolean"
                },
                "key": {
                  "type": "string"
                },
                "system": {
                  "type": "boolean"
                },
                "type": {
                  "enum": [
                    "StringsList",
                    "BooleansList",
                    "IntsList",
                    "DoublesList"
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

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'key': {'name': 'key', 'required': True, 'in': 'query'}, 'type': {'name': 'type', 'required': True, 'in': 'query'}, 'value': {'name': 'value', 'required': False, 'in': 'query'}, 'included': {'name': 'included', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/tag/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
