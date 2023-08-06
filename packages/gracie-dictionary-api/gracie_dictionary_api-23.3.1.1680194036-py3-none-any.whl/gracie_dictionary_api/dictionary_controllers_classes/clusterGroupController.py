class clusterGroupController:
    """"""

    _controller_name = "clusterGroupController"
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
                "clusterSetId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "clustersCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  }
                },
                "name": {
                  "example": "Cluster group name",
                  "type": "string"
                },
                "parameters": {
                  "error": {
                    "type": "string"
                  },
                  "groupName": {
                    "type": "string"
                  },
                  "language": {
                    "type": "string"
                  },
                  "maxClusters": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "maxKeywords": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "minClusters": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "numIterations": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "seed": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "status": {
                    "type": "string"
                  },
                  "timestamps": {
                    "completedIn": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "createdAt": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "endedAt": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "startedAt": {
                      "format": "int64",
                      "type": "integer"
                    }
                  },
                  "username": {
                    "type": "string"
                  }
                },
                "taskId": {
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
        api = '/clusterGroup/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, clusterSetId, **kwargs):
        """

        Args:
            clusterSetId: (string): 
            orderBy: (string): 
            orderAsc: (boolean): 
            limit: (integer): 
            offset: (integer): 

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
                    "$ref": "#/components/schemas/ClusterGroupPojo"
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

        all_api_parameters = {'clusterSetId': {'name': 'clusterSetId', 'required': True, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/clusterGroup/list'
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
                "clusterSetId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "clustersCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  }
                },
                "name": {
                  "example": "Cluster group name",
                  "type": "string"
                },
                "parameters": {
                  "error": {
                    "type": "string"
                  },
                  "groupName": {
                    "type": "string"
                  },
                  "language": {
                    "type": "string"
                  },
                  "maxClusters": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "maxKeywords": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "minClusters": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "numIterations": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "seed": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "status": {
                    "type": "string"
                  },
                  "timestamps": {
                    "completedIn": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "createdAt": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "endedAt": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "startedAt": {
                      "format": "int64",
                      "type": "integer"
                    }
                  },
                  "username": {
                    "type": "string"
                  }
                },
                "taskId": {
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
        api = '/clusterGroup/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def clusterize(self, id, **kwargs):
        """

        Args:
            id: (string): 
            languageId: (string): 
            minClusters: (integer): 
            maxClusters: (integer): 
            iterations: (integer): 
            seed: (integer): 
            maxKeywords: (integer): 

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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'minClusters': {'name': 'minClusters', 'required': False, 'in': 'query'}, 'maxClusters': {'name': 'maxClusters', 'required': False, 'in': 'query'}, 'iterations': {'name': 'iterations', 'required': False, 'in': 'query'}, 'seed': {'name': 'seed', 'required': False, 'in': 'query'}, 'maxKeywords': {'name': 'maxKeywords', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/clusterGroup/clusterize'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, clusterSetId, name, **kwargs):
        """

        Args:
            clusterSetId: (string): 
            name: (string): 
            languageId: (string): 
            minClusters: (integer): 
            maxClusters: (integer): 
            iterations: (integer): 
            seed: (integer): 
            maxKeywords: (integer): 

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
                "clusterSetId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "metaInfo": {
                  "clustersCount": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "corpusDocumentsCount": {
                    "format": "int32",
                    "type": "integer"
                  }
                },
                "name": {
                  "example": "Cluster group name",
                  "type": "string"
                },
                "parameters": {
                  "error": {
                    "type": "string"
                  },
                  "groupName": {
                    "type": "string"
                  },
                  "language": {
                    "type": "string"
                  },
                  "maxClusters": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "maxKeywords": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "minClusters": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "numIterations": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "seed": {
                    "format": "int64",
                    "type": "integer"
                  },
                  "status": {
                    "type": "string"
                  },
                  "timestamps": {
                    "completedIn": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "createdAt": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "endedAt": {
                      "format": "int64",
                      "type": "integer"
                    },
                    "startedAt": {
                      "format": "int64",
                      "type": "integer"
                    }
                  },
                  "username": {
                    "type": "string"
                  }
                },
                "taskId": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'clusterSetId': {'name': 'clusterSetId', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'minClusters': {'name': 'minClusters', 'required': False, 'in': 'query'}, 'maxClusters': {'name': 'maxClusters', 'required': False, 'in': 'query'}, 'iterations': {'name': 'iterations', 'required': False, 'in': 'query'}, 'seed': {'name': 'seed', 'required': False, 'in': 'query'}, 'maxKeywords': {'name': 'maxKeywords', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/clusterGroup/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
