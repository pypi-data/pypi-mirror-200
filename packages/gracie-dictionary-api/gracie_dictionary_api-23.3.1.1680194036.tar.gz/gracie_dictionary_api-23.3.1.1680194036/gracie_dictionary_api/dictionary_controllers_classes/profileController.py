class profileController:
    """"""

    _controller_name = "profileController"
    _gracie = None

    def __init__(self, gracie):
        self._gracie = gracie

    def test(self, id, **kwargs):
        """

        Args:
            id: (string): 
            languageId: (string): 
            files: (array): 

        Consumes: multipart/form-data

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

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}, 'files': {'name': 'files', 'required': 'true', 'in': 'formData'}}
        parameters_names_map = {}
        api = '/profile/test'
        actions = ['post']
        consumes = ['multipart/form-data']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

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
                "changedSkills": {
                  "items": {
                    "$ref": "#/components/schemas/SkillPojo"
                  },
                  "type": "array"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "languages": {
                  "items": {
                    "$ref": "#/components/schemas/ProfileLanguagePojo"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Profile name",
                  "type": "string"
                },
                "profileValid": {
                  "type": "boolean"
                },
                "type": {
                  "enum": [
                    "SKILL_PLUS_PLUS",
                    "POWER_PROFILE"
                  ],
                  "type": "string"
                },
                "updatedBinary": {
                  "format": "int64",
                  "type": "integer"
                },
                "updatedData": {
                  "format": "int64",
                  "type": "integer"
                },
                "useDocumentVector": {
                  "type": "boolean"
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
        api = '/profile/retrieve'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def list(self, **kwargs):
        """

        Args:
            orderBy: (string): 
            orderAsc: (boolean): 
            type: (string): 

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
                    "$ref": "#/components/schemas/ProfilePojo"
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

        all_api_parameters = {'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}, 'type': {'name': 'type', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/list'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def edit(self, id, **kwargs):
        """

        Args:
            id: (string): 
            useDocumentVector: (boolean): 

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
                "changedSkills": {
                  "items": {
                    "$ref": "#/components/schemas/SkillPojo"
                  },
                  "type": "array"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "languages": {
                  "items": {
                    "$ref": "#/components/schemas/ProfileLanguagePojo"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Profile name",
                  "type": "string"
                },
                "profileValid": {
                  "type": "boolean"
                },
                "type": {
                  "enum": [
                    "SKILL_PLUS_PLUS",
                    "POWER_PROFILE"
                  ],
                  "type": "string"
                },
                "updatedBinary": {
                  "format": "int64",
                  "type": "integer"
                },
                "updatedData": {
                  "format": "int64",
                  "type": "integer"
                },
                "useDocumentVector": {
                  "type": "boolean"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'useDocumentVector': {'name': 'useDocumentVector', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/edit'
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
                "changedSkills": {
                  "items": {
                    "$ref": "#/components/schemas/SkillPojo"
                  },
                  "type": "array"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "languages": {
                  "items": {
                    "$ref": "#/components/schemas/ProfileLanguagePojo"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Profile name",
                  "type": "string"
                },
                "profileValid": {
                  "type": "boolean"
                },
                "type": {
                  "enum": [
                    "SKILL_PLUS_PLUS",
                    "POWER_PROFILE"
                  ],
                  "type": "string"
                },
                "updatedBinary": {
                  "format": "int64",
                  "type": "integer"
                },
                "updatedData": {
                  "format": "int64",
                  "type": "integer"
                },
                "useDocumentVector": {
                  "type": "boolean"
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
        api = '/profile/delete'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def add(self, name, **kwargs):
        """

        Args:
            name: (string): 
            useDocumentVector: (boolean): 

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
                "changedSkills": {
                  "items": {
                    "$ref": "#/components/schemas/SkillPojo"
                  },
                  "type": "array"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "languages": {
                  "items": {
                    "$ref": "#/components/schemas/ProfileLanguagePojo"
                  },
                  "type": "array"
                },
                "name": {
                  "example": "Profile name",
                  "type": "string"
                },
                "profileValid": {
                  "type": "boolean"
                },
                "type": {
                  "enum": [
                    "SKILL_PLUS_PLUS",
                    "POWER_PROFILE"
                  ],
                  "type": "string"
                },
                "updatedBinary": {
                  "format": "int64",
                  "type": "integer"
                },
                "updatedData": {
                  "format": "int64",
                  "type": "integer"
                },
                "useDocumentVector": {
                  "type": "boolean"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'name': {'name': 'name', 'required': True, 'in': 'query'}, 'useDocumentVector': {'name': 'useDocumentVector', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/add'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def accuracyTableCell(self, profileAccuracyCellId, **kwargs):
        """

        Args:
            profileAccuracyCellId: (string): 
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
                "column": {
                  "format": "int32",
                  "type": "integer"
                },
                "id": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "items": {
                  "items": {
                    "$ref": "#/components/schemas/ProfileAccuracyDocumentPojo"
                  },
                  "type": "array"
                },
                "itemsTotalCount": {
                  "format": "int32",
                  "type": "integer"
                },
                "row": {
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

        all_api_parameters = {'profileAccuracyCellId': {'name': 'profileAccuracyCellId', 'required': True, 'in': 'query'}, 'offset': {'name': 'offset', 'required': False, 'in': 'query'}, 'limit': {'name': 'limit', 'required': False, 'in': 'query'}, 'orderBy': {'name': 'orderBy', 'required': False, 'in': 'query'}, 'orderAsc': {'name': 'orderAsc', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/accuracyTableCell'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)

    def accuracyTable(self, id, **kwargs):
        """

        Args:
            id: (string): 
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
                "cells": {
                  "items": {
                    "items": {
                      "$ref": "#/components/schemas/ProfileAccuracyCellShortPojo"
                    },
                    "type": "array"
                  },
                  "type": "array"
                },
                "classes": {
                  "items": {
                    "$ref": "#/components/schemas/ProfileClassInAccuracyTableApiPojo"
                  },
                  "type": "array"
                },
                "languageId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                },
                "languageName": {
                  "example": "English",
                  "type": "string"
                },
                "profileId": {
                  "example": "EB60F9F6E79C25D2331891EEBFD43D4ABAD029E6970C55C2E388C1DE6F446D3A094059D6477C85B293F8F1CE1FB49D2AEBB089C6F7ECB5A2436821BECF24CD1A",
                  "type": "string"
                }
              },
              "status": {
                "example": true,
                "type": "boolean"
              }
            }
        """

        all_api_parameters = {'id': {'name': 'id', 'required': True, 'in': 'query'}, 'languageId': {'name': 'languageId', 'required': False, 'in': 'query'}}
        parameters_names_map = {}
        api = '/profile/accuracyTable'
        actions = ['post']
        consumes = ['[]']
        params, data = self._gracie._format_params_for_api(locals(), all_api_parameters, parameters_names_map)
        return self._gracie._process_api(self._controller_name, api, actions, params, data, consumes)
