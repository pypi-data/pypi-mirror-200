class topicEntitiesController:
    """"""

    _controller_name = "topicEntitiesController"
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
                "alias": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "mainNameId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "sourceEntityId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "status": {
                  "type": "string"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "topicTypeId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
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
        api = '/topicEntity/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def restore(self, id):
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
                "alias": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "mainNameId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "sourceEntityId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "status": {
                  "type": "string"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "topicTypeId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
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
        api = '/topicEntity/restore'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            topicId: (string): 
            topicTypeId: (string): 
            name: (string): 
            languageId: (string): 
            orderBy: (string): 
            limit: (integer): 
            offset: (integer): 
            orderAsc: (boolean): 
            onlyMainNames: (boolean): 

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
                    "$ref": "#/components/schemas/TopicEntitySearchResult"
                  },
                  "type": "array"
                },
                "itemsTotalCount": {
                  "example": 1,
                  "format": "int32",
                  "type": "integer"
                },
                "languageId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'topicId': {'name': 'topicId', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'onlyMainNames': {'name': 'onlyMainNames', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def importTopicEntities(self, topicTypeId, **kwargs):
        """

        Args:
            topicTypeId: (string): 
            stopOnError: (boolean): 
            languageId: (string): 
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

        all_api_parameters = {'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}, 'stopOnError': {'name': 'stopOnError', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'file': {'name': 'file', 'required': 'true', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/topicEntity/importTopicEntities'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def exportTopicEntities(self, topicTypeId, **kwargs):
        """

        Args:
            topicTypeId: (string): 
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

        all_api_parameters = {'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/exportTopicEntities'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            popularity: (integer): 
            topicTypeId: (string): 

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
                "alias": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "mainNameId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "sourceEntityId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "status": {
                  "type": "string"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "topicTypeId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/edit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def downloadExportFile(self, taskId):
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
        api = '/topicEntity/downloadExportFile'
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
                "alias": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "mainNameId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "sourceEntityId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "status": {
                  "type": "string"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "topicTypeId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
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
        api = '/topicEntity/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def clone(self, id, topicTypeId, **kwargs):
        """

        Args:
            id: (string): 
            topicTypeId: (string): 
            deleteSource: (boolean): 
            popularity: (integer): 

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
                "alias": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "mainNameId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "sourceEntityId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "status": {
                  "type": "string"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "topicTypeId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}, 'deleteSource': {'name': 'deleteSource', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/clone'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkDelete(self, ids):
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
                "items": {
                  "$ref": "#/components/schemas/TopicEntityPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/bulkDelete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, popularity, topicTypeId, names, **kwargs):
        """

        Args:
            alias: (string): 
            popularity: (integer): 
            topicTypeId: (string): 
            names: (string): 
            briefs: (string): 

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
                "alias": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "mainNameId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "sourceEntityId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                },
                "status": {
                  "type": "string"
                },
                "topicId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "topicTypeId": {
                  "example": "8B148931121979DA2BC1DE7B0B5538D3B3006DA26D1C87DE4968034A55E4CFE6B1B0CBD25DCCF70E3918737A45943F16A1603B024D7C673E29C8E3AA3544AF46",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'alias': {'name': 'alias', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': True, 'in': 'query'}, 'topicTypeId': {'name': 'topicTypeId', 'required': True, 'in': 'query'}, 'names': {'name': 'names', 'required': True, 'in': 'query'}, 'briefs': {'name': 'briefs', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/topicEntity/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
