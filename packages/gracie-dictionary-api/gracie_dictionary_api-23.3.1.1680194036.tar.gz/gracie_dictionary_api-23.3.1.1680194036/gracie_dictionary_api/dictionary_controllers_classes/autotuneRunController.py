class autotuneRunController:
    """"""

    _controller_name = "autotuneRunController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def run(self, id, maxIterations, **kwargs):
        """

        Args:
            id: (string): 
            maxIterations: (integer): 
            firstIterationUpdatesSkills: (boolean): 

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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'maxIterations': {'name': 'maxIterations', 'required': True, 'in': 'query'}, 'firstIterationUpdatesSkills': {'name': 'firstIterationUpdatesSkills', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/run'
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
                "languageId": {
                  "example": "FA6DFB6D6B6807B84DC9811814452EC7B0712AD31C6DF6AF3819723B2495BE97C0C1BAA32CBD867F4869020B34E54E67D0114A733C0D164F58B992DB4435DE37",
                  "type": "string"
                },
                "name": {
                  "example": "Autotune-run name",
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "hasNeverBeenRun",
                    "hasBeenRun",
                    "isRunning"
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
        api = '/autotuneRun/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
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
                    "$ref": "#/components/schemas/AutotuneRunPojo"
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

        all_api_parameters = {'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/list'
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
                  "example": "FA6DFB6D6B6807B84DC9811814452EC7B0712AD31C6DF6AF3819723B2495BE97C0C1BAA32CBD867F4869020B34E54E67D0114A733C0D164F58B992DB4435DE37",
                  "type": "string"
                },
                "name": {
                  "example": "Autotune-run name",
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "hasNeverBeenRun",
                    "hasBeenRun",
                    "isRunning"
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
        api = '/autotuneRun/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def autofit(self, id, **kwargs):
        """

        Args:
            id: (string): 
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/autofit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, name, **kwargs):
        """

        Args:
            name: (string): 
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
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "languageId": {
                  "example": "FA6DFB6D6B6807B84DC9811814452EC7B0712AD31C6DF6AF3819723B2495BE97C0C1BAA32CBD867F4869020B34E54E67D0114A733C0D164F58B992DB4435DE37",
                  "type": "string"
                },
                "name": {
                  "example": "Autotune-run name",
                  "type": "string"
                },
                "status": {
                  "enum": [
                    "hasNeverBeenRun",
                    "hasBeenRun",
                    "isRunning"
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

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneRun/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
