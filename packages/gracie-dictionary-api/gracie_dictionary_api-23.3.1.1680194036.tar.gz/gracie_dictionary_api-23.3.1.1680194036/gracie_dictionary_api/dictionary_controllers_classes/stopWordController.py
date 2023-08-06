class stopWordController:
    """"""

    _controller_name = "stopWordController"
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
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "languageId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "name": {
                  "example": "And",
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
        api = '/stopWord/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            languageId: (string): 
            name: (string): 
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
                    "$ref": "#/components/schemas/StopWordPojo"
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

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/stopWord/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def import_(self, **kwargs):
        """

        Args:
            languageId: (string): 
            conflictsResolving: (string): 
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

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'conflictsResolving': {'name': 'conflictsResolving', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': 'true', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/stopWord/import'
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
        api = '/stopWord/export'
        actions = ['get']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportPost(self, **kwargs):
        """

        Args:
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

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/stopWord/export'
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
                "languageId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "name": {
                  "example": "And",
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
        api = '/stopWord/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, name, **kwargs):
        """

        Args:
            languageId: (string): 
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
                "languageId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "name": {
                  "example": "And",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/stopWord/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
