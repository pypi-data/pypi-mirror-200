class infoController:
    """"""

    _controller_name = "infoController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def retrieve(self):
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
                "search": {
                  "maxSearchTasks": {
                    "format": "int32",
                    "type": "integer"
                  },
                  "maxTextLength": {
                    "format": "int32",
                    "type": "integer"
                  }
                },
                "server": {
                  "buildCommit": {
                    "type": "string"
                  },
                  "buildScmBranch": {
                    "type": "string"
                  },
                  "builtAt": {
                    "type": "string"
                  },
                  "serverId": {
                    "type": "string"
                  },
                  "uiLanguageCode": {
                    "type": "string"
                  },
                  "version": {
                    "type": "string"
                  }
                },
                "system": {
                  "currentTime": {
                    "type": "string"
                  },
                  "freeMemory": {
                    "type": "string"
                  },
                  "offheapFreeMemory": {
                    "type": "string"
                  },
                  "offheapTotalMemory": {
                    "type": "string"
                  },
                  "offheapUsedMemory": {
                    "type": "string"
                  },
                  "totalMemory": {
                    "type": "string"
                  },
                  "usedMemory": {
                    "type": "string"
                  }
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {}
        parameters_names_map = {}
        api = '/info/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
