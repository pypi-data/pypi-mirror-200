class entityRiskRuleController:
    """"""

    _controller_name = "entityRiskRuleController"
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
                "entityRefs": {
                  "items": {
                    "$ref": "#/components/schemas/EntityRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "minQuantity": {
                  "format": "int32",
                  "type": "integer"
                },
                "requireUnique": {
                  "type": "boolean"
                },
                "riskLabel": {
                  "type": "string"
                },
                "riskValue": {
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
        api = '/entityRiskRules/retrieve'
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
                "entityRefs": {
                  "items": {
                    "$ref": "#/components/schemas/EntityRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "minQuantity": {
                  "format": "int32",
                  "type": "integer"
                },
                "requireUnique": {
                  "type": "boolean"
                },
                "riskLabel": {
                  "type": "string"
                },
                "riskValue": {
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/removeLabel'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def remove(self, id):
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
                "entityRefs": {
                  "items": {
                    "$ref": "#/components/schemas/EntityRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "minQuantity": {
                  "format": "int32",
                  "type": "integer"
                },
                "requireUnique": {
                  "type": "boolean"
                },
                "riskLabel": {
                  "type": "string"
                },
                "riskValue": {
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
        api = '/entityRiskRules/remove'
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
        api = '/entityRiskRules/listLabels'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            label: (string): 
            offset: (string): 
            limit: (string): 
            orderBy: (string): 
            orderAsc: (string): 

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
                    "$ref": "#/components/schemas/EntityRiskRulePojo"
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
        api = '/entityRiskRules/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            riskLabel: (string): 
            minQuantity: (integer): 
            requireUnique: (boolean): 
            riskValue: (number): 
            entityRefs: (array): 

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
                "entityRefs": {
                  "items": {
                    "$ref": "#/components/schemas/EntityRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "minQuantity": {
                  "format": "int32",
                  "type": "integer"
                },
                "requireUnique": {
                  "type": "boolean"
                },
                "riskLabel": {
                  "type": "string"
                },
                "riskValue": {
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'riskLabel': {'name': 'riskLabel', 'required': False, 'in': 'query'}, 'minQuantity': {'name': 'minQuantity', 'required': False, 'in': 'query'}, 'requireUnique': {'name': 'requireUnique', 'required': False, 'in': 'query'}, 'riskValue': {'name': 'riskValue', 'required': False, 'in': 'query'}, 'entityRefs': {'name': 'entityRefs', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/edit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def create(self, riskLabel, minQuantity, requireUnique, riskValue, entityRefs):
        """

        Args:
            riskLabel: (string): 
            minQuantity: (integer): 
            requireUnique: (boolean): 
            riskValue: (number): 
            entityRefs: (array): 

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
                "entityRefs": {
                  "items": {
                    "$ref": "#/components/schemas/EntityRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "minQuantity": {
                  "format": "int32",
                  "type": "integer"
                },
                "requireUnique": {
                  "type": "boolean"
                },
                "riskLabel": {
                  "type": "string"
                },
                "riskValue": {
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

        all_api_parameters = {'riskLabel': {'name': 'riskLabel', 'required': True, 'in': 'query'}, 'minQuantity': {'name': 'minQuantity', 'required': True, 'in': 'query'}, 'requireUnique': {'name': 'requireUnique', 'required': True, 'in': 'query'}, 'riskValue': {'name': 'riskValue', 'required': True, 'in': 'query'}, 'entityRefs': {'name': 'entityRefs', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/create'
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
                "entityRefs": {
                  "items": {
                    "$ref": "#/components/schemas/EntityRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "minQuantity": {
                  "format": "int32",
                  "type": "integer"
                },
                "requireUnique": {
                  "type": "boolean"
                },
                "riskLabel": {
                  "type": "string"
                },
                "riskValue": {
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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'label': {'name': 'label', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/entityRiskRules/addLabel'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
