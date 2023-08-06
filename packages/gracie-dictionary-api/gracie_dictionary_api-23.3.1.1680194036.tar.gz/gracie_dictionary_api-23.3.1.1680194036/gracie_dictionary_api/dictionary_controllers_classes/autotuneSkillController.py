class autotuneSkillController:
    """"""

    _controller_name = "autotuneSkillController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def list(self, autotuneRunId, **kwargs):
        """

        Args:
            autotuneRunId: (string): 
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
                    "$ref": "#/components/schemas/AutotuneSkillRefPojo"
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

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def delete(self, autotuneRunId, skillId):
        """

        Args:
            autotuneRunId: (string): 
            skillId: (string): 

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
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "name": {
                  "example": "Skill name",
                  "type": "string"
                },
                "skillsetId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "skillsetName": {
                  "example": "Skillset name",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}, 'skillId': {'name': 'skillId', 'required': True, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def bulkAdd(self, autotuneRunId, **kwargs):
        """

        Args:
            autotuneRunId: (string): 
            skillIds: (array): 
            skillsetIds: (array): 

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
                  "$ref": "#/components/schemas/AutotuneSkillRefPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}, 'skillIds': {'name': 'skillIds', 'required': False, 'in': 'query'}, 'skillsetIds': {'name': 'skillsetIds', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/bulkAdd'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def addSkills(self, autotuneRunId, **kwargs):
        """

        Args:
            autotuneRunId: (string): 
            classId: (string): 

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
                  "$ref": "#/components/schemas/AutotuneSkillRefPojo"
                },
                "type": "array"
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'autotuneRunId': {'name': 'autotuneRunId', 'required': True, 'in': 'query'}, 'classId': {'name': 'classId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/autotuneSkill/addSkills'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
