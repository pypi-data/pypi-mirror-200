class compoundLexemeController:
    """"""

    _controller_name = "compoundLexemeController"
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
                "badReferences": {
                  "example": [],
                  "items": {
                    "example": "[]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "config": {
                  "additionalProperties": {
                    "example": "<JSON Configuration>",
                    "type": "object"
                  },
                  "example": "<JSON Configuration>",
                  "type": "object"
                },
                "enabled": {
                  "example": true,
                  "type": "boolean"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "importHints": {
                  "additionalProperties": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/RegexImportHint"
                      }
                    ]
                  },
                  "example": {},
                  "type": "object"
                },
                "labels": {
                  "example": [
                    "one",
                    "two"
                  ],
                  "items": {
                    "example": "[\"one\",\"two\"]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Name",
                  "type": "string"
                },
                "valid": {
                  "example": false,
                  "type": "boolean"
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
        api = '/compoundLexeme/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def removeLabel(self, id, label):
        """

        Args:
            id: (string): 
            label: (string): 

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
                "badReferences": {
                  "example": [],
                  "items": {
                    "example": "[]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "config": {
                  "additionalProperties": {
                    "example": "<JSON Configuration>",
                    "type": "object"
                  },
                  "example": "<JSON Configuration>",
                  "type": "object"
                },
                "enabled": {
                  "example": true,
                  "type": "boolean"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "importHints": {
                  "additionalProperties": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/RegexImportHint"
                      }
                    ]
                  },
                  "example": {},
                  "type": "object"
                },
                "labels": {
                  "example": [
                    "one",
                    "two"
                  ],
                  "items": {
                    "example": "[\"one\",\"two\"]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Name",
                  "type": "string"
                },
                "valid": {
                  "example": false,
                  "type": "boolean"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/removeLabel'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listNames(self, **kwargs):
        """Return list of compound lexeme item names.

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
                "items": {
                  "type": "string"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/listNames'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listLabels(self):
        """

        Args:

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
                  "type": "string"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/compoundLexeme/listLabels'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            label: (string): 
            offset: (integer): 
            limit: (integer): 
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
                    "$ref": "#/components/schemas/CompoundLexemePojo"
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

        all_api_parameters = {'label': {'name': 'label', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def import_(self, **kwargs):
        """

        Args:
            conflictsResolving: (string): 
            stopOnError: (boolean): 
            file: (string): 

        Consumes: multipart/form-data

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
                "error": {
                  "message": {
                    "type": "string"
                  }
                },
                "id": {
                  "type": "string"
                },
                "parameters": {
                  "$ref": "#/components/schemas/TaskParameters"
                },
                "result": {
                  "$ref": "#/components/schemas/TaskResult"
                },
                "status": {
                  "enum": [
                    "Waiting",
                    "Blocked",
                    "Running",
                    "Completed",
                    "Cancelling",
                    "Failed",
                    "Cancelled"
                  ],
                  "type": "string"
                },
                "timestamps": {
                  "completedIn": {
                    "type": "string"
                  },
                  "createdAt": {
                    "type": "string"
                  },
                  "endedAt": {
                    "type": "string"
                  },
                  "startedAt": {
                    "type": "string"
                  }
                },
                "typeId": {
                  "type": "string"
                },
                "userId": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'conflictsResolving': {'name': 'conflictsResolving', 'required': False, 'in': 'query'}, 'stopOnError': {'name': 'stopOnError', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': 'true', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/compoundLexeme/import'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportGet(self, taskId):
        """

        Args:
            taskId: (string): 

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
                "downloadToken": {
                  "type": "string"
                },
                "downloadUrl": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'taskId': {'name': 'taskId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/export'
        actions = ['get']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportPost(self, **kwargs):
        """

        Args:
            ids: (array): 

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
                "error": {
                  "message": {
                    "type": "string"
                  }
                },
                "id": {
                  "type": "string"
                },
                "parameters": {
                  "$ref": "#/components/schemas/TaskParameters"
                },
                "result": {
                  "$ref": "#/components/schemas/TaskResult"
                },
                "status": {
                  "enum": [
                    "Waiting",
                    "Blocked",
                    "Running",
                    "Completed",
                    "Cancelling",
                    "Failed",
                    "Cancelled"
                  ],
                  "type": "string"
                },
                "timestamps": {
                  "completedIn": {
                    "type": "string"
                  },
                  "createdAt": {
                    "type": "string"
                  },
                  "endedAt": {
                    "type": "string"
                  },
                  "startedAt": {
                    "type": "string"
                  }
                },
                "typeId": {
                  "type": "string"
                },
                "userId": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/export'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, enabled, **kwargs):
        """

        Args:
            id: (string): 
            name: (string): 
            enabled: (boolean): 
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
                "example": "Success",
                "type": "string"
              },
              "response": {
                "badReferences": {
                  "example": [],
                  "items": {
                    "example": "[]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "config": {
                  "additionalProperties": {
                    "example": "<JSON Configuration>",
                    "type": "object"
                  },
                  "example": "<JSON Configuration>",
                  "type": "object"
                },
                "enabled": {
                  "example": true,
                  "type": "boolean"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "importHints": {
                  "additionalProperties": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/RegexImportHint"
                      }
                    ]
                  },
                  "example": {},
                  "type": "object"
                },
                "labels": {
                  "example": [
                    "one",
                    "two"
                  ],
                  "items": {
                    "example": "[\"one\",\"two\"]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Name",
                  "type": "string"
                },
                "valid": {
                  "example": false,
                  "type": "boolean"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}, 'body': {'name': 'body', 'required': 'false', 'in': 'body'}}
        parameters_names_map = {}
        api = '/compoundLexeme/edit'
        actions = ['post']
        consumes = ['application/json']
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
                "badReferences": {
                  "example": [],
                  "items": {
                    "example": "[]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "config": {
                  "additionalProperties": {
                    "example": "<JSON Configuration>",
                    "type": "object"
                  },
                  "example": "<JSON Configuration>",
                  "type": "object"
                },
                "enabled": {
                  "example": true,
                  "type": "boolean"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "importHints": {
                  "additionalProperties": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/RegexImportHint"
                      }
                    ]
                  },
                  "example": {},
                  "type": "object"
                },
                "labels": {
                  "example": [
                    "one",
                    "two"
                  ],
                  "items": {
                    "example": "[\"one\",\"two\"]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Name",
                  "type": "string"
                },
                "valid": {
                  "example": false,
                  "type": "boolean"
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
        api = '/compoundLexeme/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def addLabel(self, id, label):
        """

        Args:
            id: (string): 
            label: (string): 

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
                "badReferences": {
                  "example": [],
                  "items": {
                    "example": "[]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "config": {
                  "additionalProperties": {
                    "example": "<JSON Configuration>",
                    "type": "object"
                  },
                  "example": "<JSON Configuration>",
                  "type": "object"
                },
                "enabled": {
                  "example": true,
                  "type": "boolean"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "importHints": {
                  "additionalProperties": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/RegexImportHint"
                      }
                    ]
                  },
                  "example": {},
                  "type": "object"
                },
                "labels": {
                  "example": [
                    "one",
                    "two"
                  ],
                  "items": {
                    "example": "[\"one\",\"two\"]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Name",
                  "type": "string"
                },
                "valid": {
                  "example": false,
                  "type": "boolean"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/compoundLexeme/addLabel'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, name, enabled):
        """

        Args:
            name: (string): 
            enabled: (boolean): 
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
                "example": "Success",
                "type": "string"
              },
              "response": {
                "badReferences": {
                  "example": [],
                  "items": {
                    "example": "[]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "config": {
                  "additionalProperties": {
                    "example": "<JSON Configuration>",
                    "type": "object"
                  },
                  "example": "<JSON Configuration>",
                  "type": "object"
                },
                "enabled": {
                  "example": true,
                  "type": "boolean"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "importHints": {
                  "additionalProperties": {
                    "oneOf": [
                      {
                        "$ref": "#/components/schemas/RegexImportHint"
                      }
                    ]
                  },
                  "example": {},
                  "type": "object"
                },
                "labels": {
                  "example": [
                    "one",
                    "two"
                  ],
                  "items": {
                    "example": "[\"one\",\"two\"]",
                    "type": "string"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Name",
                  "type": "string"
                },
                "valid": {
                  "example": false,
                  "type": "boolean"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'enabled': {'name': 'enabled', 'required': True, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/compoundLexeme/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
