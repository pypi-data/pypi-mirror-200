class countryController:
    """"""

    _controller_name = "countryController"
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
                "capital": {
                  "example": "London",
                  "type": "string"
                },
                "code": {
                  "example": "--",
                  "type": "string"
                },
                "continentId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "currencyCode": {
                  "example": "EU",
                  "type": "string"
                },
                "currencyName": {
                  "example": "Euro",
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "name": {
                  "example": "no-country",
                  "type": "string"
                },
                "phoneCode": {
                  "example": "38",
                  "type": "string"
                },
                "postalCodeFormat": {
                  "example": "65000",
                  "type": "string"
                },
                "postalCodeRegExp": {
                  "example": "65000",
                  "type": "string"
                },
                "topLevelDomain": {
                  "example": "null",
                  "type": "string"
                },
                "updatedBinary": {
                  "format": "int64",
                  "type": "integer"
                },
                "updatedData": {
                  "format": "int64",
                  "type": "integer"
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
        api = '/country/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            continentId: (string): 
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
                    "$ref": "#/components/schemas/CountryPojo"
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

        all_api_parameters = {'continentId': {'name': 'continentId', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/country/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            name: (string): 
            continentId: (string): 
            capital: (string): 
            topLevelDomain: (string): 
            currencyCode: (string): 
            currencyName: (string): 
            phoneCode: (string): 
            postalCodeFormat: (string): 
            postalCodeRegExp: (string): 

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
                "capital": {
                  "example": "London",
                  "type": "string"
                },
                "code": {
                  "example": "--",
                  "type": "string"
                },
                "continentId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "currencyCode": {
                  "example": "EU",
                  "type": "string"
                },
                "currencyName": {
                  "example": "Euro",
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "name": {
                  "example": "no-country",
                  "type": "string"
                },
                "phoneCode": {
                  "example": "38",
                  "type": "string"
                },
                "postalCodeFormat": {
                  "example": "65000",
                  "type": "string"
                },
                "postalCodeRegExp": {
                  "example": "65000",
                  "type": "string"
                },
                "topLevelDomain": {
                  "example": "null",
                  "type": "string"
                },
                "updatedBinary": {
                  "format": "int64",
                  "type": "integer"
                },
                "updatedData": {
                  "format": "int64",
                  "type": "integer"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': False, 'in': 'query'}, 'continentId': {'name': 'continentId', 'required': False, 'in': 'query'}, 'capital': {'name': 'capital', 'required': False, 'in': 'query'}, 'topLevelDomain': {'name': 'top-level-domain', 'required': False, 'in': 'query'}, 'currencyCode': {'name': 'currency-code', 'required': False, 'in': 'query'}, 'currencyName': {'name': 'currency-name', 'required': False, 'in': 'query'}, 'phoneCode': {'name': 'phone-code', 'required': False, 'in': 'query'}, 'postalCodeFormat': {'name': 'postal-code-format', 'required': False, 'in': 'query'}, 'postalCodeRegExp': {'name': 'postal-code-reg-exp', 'required': False, 'in': 'query'}}
        parameters_names_map = {'topLevelDomain': 'top-level-domain', 'currencyCode': 'currency-code', 'currencyName': 'currency-name', 'phoneCode': 'phone-code', 'postalCodeFormat': 'postal-code-format', 'postalCodeRegExp': 'postal-code-reg-exp'}
        api = '/country/edit'
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
                "capital": {
                  "example": "London",
                  "type": "string"
                },
                "code": {
                  "example": "--",
                  "type": "string"
                },
                "continentId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "currencyCode": {
                  "example": "EU",
                  "type": "string"
                },
                "currencyName": {
                  "example": "Euro",
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "name": {
                  "example": "no-country",
                  "type": "string"
                },
                "phoneCode": {
                  "example": "38",
                  "type": "string"
                },
                "postalCodeFormat": {
                  "example": "65000",
                  "type": "string"
                },
                "postalCodeRegExp": {
                  "example": "65000",
                  "type": "string"
                },
                "topLevelDomain": {
                  "example": "null",
                  "type": "string"
                },
                "updatedBinary": {
                  "format": "int64",
                  "type": "integer"
                },
                "updatedData": {
                  "format": "int64",
                  "type": "integer"
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
        api = '/country/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, code, name, **kwargs):
        """

        Args:
            code: (string): 
            name: (string): 
            continentId: (string): 
            capital: (string): 
            topLevelDomain: (string): 
            currencyCode: (string): 
            currencyName: (string): 
            phoneCode: (string): 
            postalCodeFormat: (string): 
            postalCodeRegExp: (string): 

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
                "capital": {
                  "example": "London",
                  "type": "string"
                },
                "code": {
                  "example": "--",
                  "type": "string"
                },
                "continentId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "currencyCode": {
                  "example": "EU",
                  "type": "string"
                },
                "currencyName": {
                  "example": "Euro",
                  "type": "string"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "name": {
                  "example": "no-country",
                  "type": "string"
                },
                "phoneCode": {
                  "example": "38",
                  "type": "string"
                },
                "postalCodeFormat": {
                  "example": "65000",
                  "type": "string"
                },
                "postalCodeRegExp": {
                  "example": "65000",
                  "type": "string"
                },
                "topLevelDomain": {
                  "example": "null",
                  "type": "string"
                },
                "updatedBinary": {
                  "format": "int64",
                  "type": "integer"
                },
                "updatedData": {
                  "format": "int64",
                  "type": "integer"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'code': {'name': 'code', 'required': True, 'in': 'query'}, 'name': {'name': 'name', 'required': True, 'in': 'query'}, 'continentId': {'name': 'continentId', 'required': False, 'in': 'query'}, 'capital': {'name': 'capital', 'required': False, 'in': 'query'}, 'topLevelDomain': {'name': 'top-level-domain', 'required': False, 'in': 'query'}, 'currencyCode': {'name': 'currency-code', 'required': False, 'in': 'query'}, 'currencyName': {'name': 'currency-name', 'required': False, 'in': 'query'}, 'phoneCode': {'name': 'phone-code', 'required': False, 'in': 'query'}, 'postalCodeFormat': {'name': 'postal-code-format', 'required': False, 'in': 'query'}, 'postalCodeRegExp': {'name': 'postal-code-reg-exp', 'required': False, 'in': 'query'}}
        parameters_names_map = {'topLevelDomain': 'top-level-domain', 'currencyCode': 'currency-code', 'currencyName': 'currency-name', 'phoneCode': 'phone-code', 'postalCodeFormat': 'postal-code-format', 'postalCodeRegExp': 'postal-code-reg-exp'}
        api = '/country/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
