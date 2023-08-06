class geoEntitiesController:
    """"""

    _controller_name = "geoEntitiesController"
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
                "adminCode": {
                  "type": "string"
                },
                "alias": {
                  "type": "string"
                },
                "continentId": {
                  "type": "string"
                },
                "countryId": {
                  "type": "string"
                },
                "featureClassId": {
                  "type": "string"
                },
                "featureCodeId": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "latitude": {
                  "format": "double",
                  "type": "number"
                },
                "longitude": {
                  "format": "double",
                  "type": "number"
                },
                "mainNameId": {
                  "type": "string"
                },
                "parentId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "population": {
                  "format": "int64",
                  "type": "integer"
                },
                "status": {
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
        api = '/geoEntity/retrieve'
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
                "adminCode": {
                  "type": "string"
                },
                "alias": {
                  "type": "string"
                },
                "continentId": {
                  "type": "string"
                },
                "countryId": {
                  "type": "string"
                },
                "featureClassId": {
                  "type": "string"
                },
                "featureCodeId": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "latitude": {
                  "format": "double",
                  "type": "number"
                },
                "longitude": {
                  "format": "double",
                  "type": "number"
                },
                "mainNameId": {
                  "type": "string"
                },
                "parentId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "population": {
                  "format": "int64",
                  "type": "integer"
                },
                "status": {
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
        api = '/geoEntity/restore'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            name: (string): 
            languageId: (string): 
            parentId: (string): 
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
                    "$ref": "#/components/schemas/GeoEntitySearchResult"
                  },
                  "type": "array"
                },
                "itemsTotalCount": {
                  "format": "int32",
                  "type": "integer"
                },
                "languageId": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': False, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'onlyMainNames': {'name': 'onlyMainNames', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            adminCode: (string): 
            popularity: (integer): 
            population: (integer): 
            latitude: (number): 
            longitude: (number): 
            featureCodeId: (string): 
            parentId: (string): 

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
                "adminCode": {
                  "type": "string"
                },
                "alias": {
                  "type": "string"
                },
                "continentId": {
                  "type": "string"
                },
                "countryId": {
                  "type": "string"
                },
                "featureClassId": {
                  "type": "string"
                },
                "featureCodeId": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "latitude": {
                  "format": "double",
                  "type": "number"
                },
                "longitude": {
                  "format": "double",
                  "type": "number"
                },
                "mainNameId": {
                  "type": "string"
                },
                "parentId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "population": {
                  "format": "int64",
                  "type": "integer"
                },
                "status": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'adminCode': {'name': 'adminCode', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': False, 'in': 'query'}, 'population': {'name': 'population', 'required': False, 'in': 'query'}, 'latitude': {'name': 'latitude', 'required': False, 'in': 'query'}, 'longitude': {'name': 'longitude', 'required': False, 'in': 'query'}, 'featureCodeId': {'name': 'featureCodeId', 'required': False, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/edit'
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
                "adminCode": {
                  "type": "string"
                },
                "alias": {
                  "type": "string"
                },
                "continentId": {
                  "type": "string"
                },
                "countryId": {
                  "type": "string"
                },
                "featureClassId": {
                  "type": "string"
                },
                "featureCodeId": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "latitude": {
                  "format": "double",
                  "type": "number"
                },
                "longitude": {
                  "format": "double",
                  "type": "number"
                },
                "mainNameId": {
                  "type": "string"
                },
                "parentId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "population": {
                  "format": "int64",
                  "type": "integer"
                },
                "status": {
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
        api = '/geoEntity/delete'
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
                  "$ref": "#/components/schemas/GeoEntityPojo"
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
        api = '/geoEntity/bulkDelete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, countryId, popularity, featureCodeId, names, **kwargs):
        """

        Args:
            countryId: (string): 
            alias: (string): 
            adminCode: (string): 
            popularity: (integer): 
            population: (integer): 
            latitude: (number): 
            longitude: (number): 
            featureCodeId: (string): 
            parentId: (string): 
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
                "adminCode": {
                  "type": "string"
                },
                "alias": {
                  "type": "string"
                },
                "continentId": {
                  "type": "string"
                },
                "countryId": {
                  "type": "string"
                },
                "featureClassId": {
                  "type": "string"
                },
                "featureCodeId": {
                  "type": "string"
                },
                "id": {
                  "type": "string"
                },
                "latitude": {
                  "format": "double",
                  "type": "number"
                },
                "longitude": {
                  "format": "double",
                  "type": "number"
                },
                "mainNameId": {
                  "type": "string"
                },
                "parentId": {
                  "type": "string"
                },
                "popularity": {
                  "format": "int32",
                  "type": "integer"
                },
                "population": {
                  "format": "int64",
                  "type": "integer"
                },
                "status": {
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'countryId': {'name': 'countryId', 'required': True, 'in': 'query'}, 'alias': {'name': 'alias', 'required': False, 'in': 'query'}, 'adminCode': {'name': 'adminCode', 'required': False, 'in': 'query'}, 'popularity': {'name': 'popularity', 'required': True, 'in': 'query'}, 'population': {'name': 'population', 'required': False, 'in': 'query'}, 'latitude': {'name': 'latitude', 'required': False, 'in': 'query'}, 'longitude': {'name': 'longitude', 'required': False, 'in': 'query'}, 'featureCodeId': {'name': 'featureCodeId', 'required': True, 'in': 'query'}, 'parentId': {'name': 'parentId', 'required': False, 'in': 'query'}, 'names': {'name': 'names', 'required': True, 'in': 'query'}, 'briefs': {'name': 'briefs', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/geoEntity/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
