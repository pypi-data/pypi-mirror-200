class summarizerController:
    """"""

    _controller_name = "summarizerController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def summarize(self, maxSentences, **kwargs):
        """

        Args:
            languageId: (string): 
            maxSentences: (integer): 
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

        all_api_parameters = {'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'maxSentences': {'name': 'maxSentences', 'required': True, 'in': 'query'}, 'body': {'name': 'body', 'required': 'true', 'in': 'body'}}
        parameters_names_map = {}
        api = '/summarize'
        actions = ['post']
        consumes = ['application/json']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
