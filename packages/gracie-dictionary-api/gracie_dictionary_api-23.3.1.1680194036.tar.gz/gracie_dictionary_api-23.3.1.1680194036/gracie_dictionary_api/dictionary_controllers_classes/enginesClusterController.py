class enginesClusterController:
    """"""

    _controller_name = "enginesClusterController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def clusterWorkers(self):
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
                  "$ref": "#/components/schemas/EngineClusterWorkerBinariesBundlesStatusPojo"
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
        api = '/engines/cluster/workers'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def clusterStatus(self):
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
                "binariesBundles": {
                  "items": {
                    "$ref": "#/components/schemas/EngineClusterLeaderBinariesBundlePojo"
                  },
                  "type": "array"
                },
                "status": {
                  "enum": [
                    "green",
                    "yellow",
                    "red"
                  ],
                  "example": "green",
                  "type": "string"
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
        api = '/engines/cluster/status'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
