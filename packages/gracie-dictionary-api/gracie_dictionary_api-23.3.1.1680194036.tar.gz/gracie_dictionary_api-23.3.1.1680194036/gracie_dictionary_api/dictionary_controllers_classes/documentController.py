class documentController:
    """"""

    _controller_name = "documentController"
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
                  "type": "string"
                },
                "languageId": {
                  "type": "string"
                },
                "languageName": {
                  "type": "string"
                },
                "name": {
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
                  "type": "string"
                },
                "weight": {
                  "format": "double",
                  "type": "number"
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
        api = '/document/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            folderId: (string): 
            languageId: (string): 
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
                "hasBlacklistKeywords": {
                  "type": "boolean"
                },
                "hasDocuments": {
                  "type": "boolean"
                },
                "hasFolders": {
                  "type": "boolean"
                },
                "hasKeywords": {
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
                },
                "type": {
                  "enum": [
                    "Root",
                    "Topics",
                    "Topic",
                    "TopicType",
                    "Skillsets",
                    "Skillset",
                    "Skill",
                    "ClusterSets",
                    "ClusterSet",
                    "ClusterSetDocuments",
                    "ClusterGroups",
                    "ClusterGroup",
                    "Cluster",
                    "Profiles",
                    "Profile",
                    "ProfileClass"
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

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            name: (string): 
            weight: (number): 
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
                "id": {
                  "type": "string"
                },
                "languageId": {
                  "type": "string"
                },
                "languageName": {
                  "type": "string"
                },
                "name": {
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
                  "type": "string"
                },
                "weight": {
                  "format": "double",
                  "type": "number"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'weight': {'name': 'weight', 'required': False, 'in': 'query'}, 'body': {'name': 'body', 'required': 'false', 'in': 'body'}}
        parameters_names_map = {}
        api = '/document/edit'
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
                "id": {
                  "type": "string"
                },
                "languageId": {
                  "type": "string"
                },
                "languageName": {
                  "type": "string"
                },
                "name": {
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
                  "type": "string"
                },
                "weight": {
                  "format": "double",
                  "type": "number"
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
        api = '/document/delete'
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
                "type": "boolean"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'ids': {'name': 'ids', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/document/bulkDelete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def addFile(self, folderId, **kwargs):
        """Supported file formats: https://tika.apache.org/1.13/formats.html

        Args:
            folderId: (string): 
            languageId: (string): 
            splitByLines: (boolean): 
            files: (array): 

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

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'splitByLines': {'name': 'splitByLines', 'required': False, 'in': 'query'}, 'files': {'name': 'files', 'required': 'true', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/document/addFile'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, folderId, **kwargs):
        """

        Args:
            folderId: (string): 
            name: (string): 
            languageId: (string): 
            weight: (number): 
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
                "id": {
                  "type": "string"
                },
                "languageId": {
                  "type": "string"
                },
                "languageName": {
                  "type": "string"
                },
                "name": {
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
                  "type": "string"
                },
                "weight": {
                  "format": "double",
                  "type": "number"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'weight': {'name': 'weight', 'required': False, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/document/add'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
