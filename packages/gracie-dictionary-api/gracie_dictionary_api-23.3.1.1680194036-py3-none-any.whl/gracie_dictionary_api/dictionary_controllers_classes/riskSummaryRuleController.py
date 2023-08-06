class riskSummaryRuleController:
    """"""

    _controller_name = "riskSummaryRuleController"
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
                "excludeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "includeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "operation": {
                  "enum": [
                    "COUNT",
                    "MEAN",
                    "MEDIAN",
                    "MODE",
                    "MAX",
                    "SUM",
                    "RANGE"
                  ],
                  "type": "string"
                },
                "riskLabel": {
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
        api = '/riskSummaryRules/retrieve'
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
                "excludeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "includeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "operation": {
                  "enum": [
                    "COUNT",
                    "MEAN",
                    "MEDIAN",
                    "MODE",
                    "MAX",
                    "SUM",
                    "RANGE"
                  ],
                  "type": "string"
                },
                "riskLabel": {
                  "type": "string"
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
        api = '/riskSummaryRules/removeLabel'
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
                "excludeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "includeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "operation": {
                  "enum": [
                    "COUNT",
                    "MEAN",
                    "MEDIAN",
                    "MODE",
                    "MAX",
                    "SUM",
                    "RANGE"
                  ],
                  "type": "string"
                },
                "riskLabel": {
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
        api = '/riskSummaryRules/remove'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def listRiskLabels(self):
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
        api = '/riskSummaryRules/listRiskLabels'
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
        api = '/riskSummaryRules/listLabels'
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
                    "$ref": "#/components/schemas/RiskSummaryRulePojo"
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
        api = '/riskSummaryRules/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            riskLabel: (string): 
            operation: (string): 
            includeRefs: (array): 
            excludeRefs: (array): 

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
                "excludeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "includeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "operation": {
                  "enum": [
                    "COUNT",
                    "MEAN",
                    "MEDIAN",
                    "MODE",
                    "MAX",
                    "SUM",
                    "RANGE"
                  ],
                  "type": "string"
                },
                "riskLabel": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'riskLabel': {'name': 'riskLabel', 'required': False, 'in': 'query'}, 'operation': {'name': 'operation', 'required': False, 'in': 'query'}, 'includeRefs': {'name': 'includeRefs', 'required': False, 'in': 'query'}, 'excludeRefs': {'name': 'excludeRefs', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/edit'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def create(self, riskLabel, operation, includeRefs, excludeRefs):
        """

        Args:
            riskLabel: (string): 
            operation: (string): 
            includeRefs: (array): 
            excludeRefs: (array): 

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
                "excludeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "includeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "operation": {
                  "enum": [
                    "COUNT",
                    "MEAN",
                    "MEDIAN",
                    "MODE",
                    "MAX",
                    "SUM",
                    "RANGE"
                  ],
                  "type": "string"
                },
                "riskLabel": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'riskLabel': {'name': 'riskLabel', 'required': True, 'in': 'query'}, 'operation': {'name': 'operation', 'required': True, 'in': 'query'}, 'includeRefs': {'name': 'includeRefs', 'required': True, 'in': 'query'}, 'excludeRefs': {'name': 'excludeRefs', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/riskSummaryRules/create'
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
                "excludeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "id": {
                  "type": "string"
                },
                "includeRefs": {
                  "items": {
                    "$ref": "#/components/schemas/SummaryRuleReference"
                  },
                  "type": "array"
                },
                "labels": {
                  "items": {
                    "type": "string"
                  },
                  "type": "array"
                },
                "operation": {
                  "enum": [
                    "COUNT",
                    "MEAN",
                    "MEDIAN",
                    "MODE",
                    "MAX",
                    "SUM",
                    "RANGE"
                  ],
                  "type": "string"
                },
                "riskLabel": {
                  "type": "string"
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
        api = '/riskSummaryRules/addLabel'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
