class blacklistKeywordController:
    """"""

    _controller_name = "blacklistKeywordController"
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/blacklistKeyword/retrieve'
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
        api = '/blacklistKeyword/list'
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
                  "type": "string"
                },
                "languageId": {
                  "type": "string"
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/blacklistKeyword/delete'
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
                  "$ref": "#/components/schemas/ClassifierBlacklistKeywordPojo"
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
        api = '/blacklistKeyword/bulkDelete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, folderId, name, **kwargs):
        """

        Args:
            folderId: (string): 
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
                  "type": "string"
                },
                "languageId": {
                  "type": "string"
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

        all_api_parameters = {'folderId': {'name': 'folderId', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/blacklistKeyword/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
