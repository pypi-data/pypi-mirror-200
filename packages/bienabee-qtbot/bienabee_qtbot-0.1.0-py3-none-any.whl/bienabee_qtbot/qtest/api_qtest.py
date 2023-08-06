"""
Copyright 2017-2023 Bienabee, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import sys
import pprint
import logging
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from ..utilities.data_utils import DataUtils
from ..utilities.error_handling import ErrorHandler

# Disable InsecureRequestWarning from disabling SSL cert verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class QTestAPI:
    """
    docstring for QTestAPI.

    INPUT PARAM Example Payload - qtest_config_data

    qtest_config_data = {
        "BASE_URL": "<qTest URL>",
        "USERNAME": "<qTest User Name>",
        "PASSWORD": "b64-encoded-PW",
        "SCV_ACCT_USER_ID": 12345,
        "USER_PROFILE_ID": 78910
    }

    """

    def __init__(self, qtest_config_data: dict):

        self.BASE_URL = None
        self.working_project_id = None
        self.__qtest_config_data = qtest_config_data
        self.__auth_header = None

        self.error_handler = ErrorHandler()

    ###############################################################################
    # This is a nested decorator class which will be used to decorate API calls with error handlers
    # https://gist.github.com/Zearin/2f40b7b9cfc51132851a
    class Decorators:

        @staticmethod
        def validate_svc_account_access(func):
            """
            This decorator function will take a aTest API function that returns response, error_detected as an argument
            and then will evaluate the response code and if 403 validate the error message to see if service account
            does not have project access and then call add service account function and then recall the function

            :param func: a qTest API function that returns response, error_detected
            :return: called function response of response, error_detected
            """

            err_msgs = ["User need to be assigned to project to performs this action!", "No permission"]

            def wrapper(api, *args, **kwargs):
                response, error_detected = func(api, *args, **kwargs)

                if response.status_code == 403:
                    for err_msg in err_msgs:
                        if err_msg in response.text:
                            svc_response, svc_error_detected = api.add_service_account_to_project()
                            if svc_error_detected is True:
                                logging.error(f"DECORATORS LOGGING - Error adding service account to qTest project.")
                                return svc_response, svc_error_detected
                            else:
                                logging.info(f"DECORATORS LOGGING - Successfully added service account to project.")
                                return func(api, *args, **kwargs)
                return response, error_detected
            return wrapper

###############################################################################
    @staticmethod
    def __set_auth_token(token):

        auth_header = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        return auth_header

###############################################################################
    def __login(self, config_data: dict):

        login_path = '/oauth/token'
        username = config_data["USERNAME"]

        login_data = {
            'grant_type': 'password',
            'username': username,
            'password': DataUtils.b64_decoder(config_data["PASSWORD"])
        }

        login_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(self.BASE_URL + login_path,
                                 data=login_data,
                                 verify=False,
                                 auth=HTTPBasicAuth(username, ''),
                                 headers=login_headers)

        error_details = "Failed to authenticate to the qTest REST API at URL '" + str(self.BASE_URL) + login_path + \
                        "' with user account '" + username + "'"

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - login",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text,
                                                                         optional_details=error_details)

        if error_detected is True:
            logging.error(f"FATAL ERROR: {error_details} exiting program now.")
            sys.exit(-1)
        else:
            return self.__set_auth_token(response.json()['access_token'])

###############################################################################
    def authenticate(self) -> bool:

        authentication_success = True

        # Setup the environment variables
        try:
            self.BASE_URL = self.__qtest_config_data["BASE_URL"]
        except Exception as err:
            logging.error(f"Error setting up the config data... ERROR: {err}")
            sys.exit(1)

        # Authenticate to the qTest environment
        try:
            self.__auth_header = self.__login(config_data=self.__qtest_config_data)
            success_auth_msg = f"Successfully established connection to qTest environment {self.BASE_URL} REST API..."
            logging.info(success_auth_msg)
        except Exception as err:
            logging.error(f"Error establishing qTest environment {self.BASE_URL} REST API connection... "
                          f"\nERROR:  {err}")
            sys.exit(1)

        return authentication_success

###############################################################################
    def post(self, path, json_data=None):

        if json_data is None:
            response = requests.post(self.BASE_URL + path,
                                     headers=self.__auth_header,
                                     verify=False)
        else:
            response = requests.post(self.BASE_URL + path,
                                     json=json_data,
                                     headers=self.__auth_header,
                                     verify=False)
        return response

###############################################################################
    def put(self, path, json_data=None):

        if json_data is None:
            response = requests.put(self.BASE_URL + path,
                                    headers=self.__auth_header,
                                    verify=False)
        else:
            response = requests.put(self.BASE_URL + path,
                                    json=json_data,
                                    headers=self.__auth_header,
                                    verify=False)
        return response

###############################################################################
    def get(self, path):
        return requests.get(self.BASE_URL + path,
                            headers=self.__auth_header,
                            verify=False)

###############################################################################
    def delete(self, path, json_data=None):

        if json_data is None:
            response = requests.delete(self.BASE_URL + path,
                                       headers=self.__auth_header,
                                       verify=False)
        else:
            response = requests.delete(self.BASE_URL + path,
                                       json=json_data,
                                       headers=self.__auth_header,
                                       verify=False)
        return response

###############################################################################
    def set_working_project_id(self, project_id):
        self.working_project_id = str(project_id)

# -----------------------------------------------------------------------------
#   START -- GET PATH functions
#   The get path functions will help us keep a consistent paths when working
#   with different qTest items
# -----------------------------------------------------------------------------

    def get_project_path(self):
        return '/api/v3/projects/' + self.working_project_id

    def get_fields_path(self, obj_type):
        return self.get_project_path() + '/settings/' + obj_type + '/fields'

    def get_test_case_path(self):
        return self.get_project_path() + '/test-cases'

    def get_requirement_path(self):
        return self.get_project_path() + '/requirements'

    def get_module_path(self):
        return self.get_project_path() + '/modules'

    def get_release_path(self):
        return self.get_project_path() + '/releases'

    def get_test_cycle_path(self):
        return self.get_project_path() + '/test-cycles'

    def get_test_suite_path(self):
        return self.get_project_path() + '/test-suites'

    def get_test_run_path(self):
        return self.get_project_path() + '/test-runs'

    def get_search_path(self):
        return self.get_project_path() + '/search'

    def get_link_path(self, source_object_type, source_object_id, linked_object_type):
        return self.get_project_path() + '/' + source_object_type + '/' + str(source_object_id) + '/link?type=' + \
               linked_object_type

    def get_project_integrations_path(self):
        return self.get_project_path() + "/settings/integration/connections"

    def get_project_integration_object_mappings_path(self, integration_id: int, integration_object_type: str):
        return self.get_project_integrations_path() + f"/{integration_id}/{integration_object_type}/mappings"

    def get_linked_artifacts_path(self, artifact_type: str, artifact_id: int):
        return self.get_project_path() + f"/linked-artifacts?type={artifact_type}&ids={artifact_id}"

    @staticmethod
    def get_site_templates_path():
        return "/api/v3/site-templates"

    @staticmethod
    def get_projects_path():
        return "/api/v3/projects"

    @staticmethod
    def get_users_path():
        return '/api/v3/users'

    @staticmethod
    def get_add_users_path(user_id):
        return f"/api/v3/users/{user_id}/projects"

    @staticmethod
    def get_add_miltiple_users_path():
        return "/api/v3/users/projects"

    @staticmethod
    def get_user_profiles_path():
        return "/api/v3/user-profiles"

    @staticmethod
    def get_search_users_path(return_inactive=None):
        inactive = "false"
        if return_inactive is True:
            inactive = "true"
        return f"/api/v3/search/user?inactive={inactive}&pagination=false"

# -----------------------------------------------------------------------------
#   END -- GET PATH functions
# -----------------------------------------------------------------------------

###############################################################################
    def get_all_users(self, return_inactive=None):

        response = self.get(path=self.get_search_users_path(return_inactive=return_inactive))

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - get_all_users",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_user_profiles(self):

        response = self.get(path=self.get_user_profiles_path())

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - get_user_roles",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

###############################################################################
    def create_sso_user(self, sso_user):

        response = self.post(path=self.get_users_path(), json_data=sso_user.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - create_sso_user",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

###############################################################################
    def add_user_to_project(self, user_id, profile_id, role, read_only, is_admin, mock_mode=False):

        payload = {"project_id": self.working_project_id,
                   "profile": {
                       "id": profile_id,
                       "name": role,
                       "is_readonly": read_only,
                       "is_admin": is_admin
                    }
                   }

        if mock_mode is True:
            response = payload
            error_detected = False
        else:
            response = self.post(path=self.get_add_users_path(user_id=user_id), json_data=payload)
            error_detected = self.error_handler.evaluate_response_log_errors(
                logger_module="qTest API - add_user_to_project",
                http_status_code=response.status_code,
                response_text=response.text)

        return response, error_detected

###############################################################################
    def add_service_account_to_project(self):
        """
        This function is called by the decorator function when the SVC account doesn't have access

        :return:
        """

        response = None
        error_detected = False

        user_id = self.__qtest_config_data["SCV_ACCT_USER_ID"]
        profile_id = self.__qtest_config_data["USER_PROFILE_ID"]

        # These values are currently set in the config file, we can programatically find them in a future update

        payload = {
                       "project_id": self.working_project_id,
                       "profile": {
                            "id": profile_id
                       },
                       "user_ids": [user_id]
                   }

        response = self.post(path=self.get_add_users_path(user_id=user_id), json_data=payload)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - add_service_account_to_project",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

###############################################################################
    def add_multiple_users_to_project(self, user_ids: list, profile_id: int, role: str):

        payload = {"project_id": self.working_project_id,
                   "profile": {
                       "id": profile_id,
                       "name": role
                   },
                   "user_ids": user_ids
                   }

        response = self.post(path=self.get_add_miltiple_users_path(), json_data=payload)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - add_multiple_users_to_project",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

###############################################################################
    def get_site_templates(self):

        request_path = self.get_site_templates_path()

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - get_site_templates",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def create_project(self, project):

        request_path = self.get_projects_path()

        response = self.post(path=request_path,
                             json_data=project.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - create_project",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def update_project(self, qtest_project_id: int, project):

        request_path = self.get_projects_path() + f"/{qtest_project_id}"

        if type(project) is dict:
            payload = project
        else:
            payload = project.get_json_data()

        response = self.put(path=request_path,
                            json_data=payload)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - create_project",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_all_projects(self, only_search_assigned=False):
        """
        This is a wrapper for the https://api.qasymphony.com/#/project/getProjects API

        :param only_search_assigned: assigned=true - default value. Only the projects which the requested user has access to
                                assigned=false - Users with admin profile can use this value to retrieve all projects,
                                regardless of having access
        :return:
        """
        if only_search_assigned is True:
            request_path = '/api/v3/projects?assigned=true'
        else:
            request_path = '/api/v3/projects?assigned=false'

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - get_all_projects",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)
        # logging.info(f"HTTP CODE: {response.status_code}  RESPONSE TEXT: {response.text}")

        return response, error_detected

###############################################################################
    def get_project_by_id(self, project_id):

        request_path = '/api/v3/projects/' + str(project_id)

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - get_project_by_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def create_test_case(self, test_case, auto_approve=None):

        response = self.post(self.get_test_case_path(),
                             test_case.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - create_test_case",
            http_status_code=response.status_code,
            response_text=response.text,
            optional_details=f"TEST DETAILS: {test_case.get_json_data()}")

        if error_detected is True:
            return response, error_detected
        else:
            test_case.id = response.json()['id']
            if auto_approve is True:
                self.approve_test_case(test_case.id)
            return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def delete_test_case(self, test_id: int):

        test_path = self.get_test_case_path() + f"/{test_id}"
        response = self.delete(path=test_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - delete_test_case",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def approve_test_case(self, qtest_id):

        request_path = str(self.get_test_case_path()) + "/" + str(qtest_id) + "/approve"

        response = self.put(path=request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "approve_test_case_by_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def update_test_case(self, test_case, test_case_id):

        response = self.put(self.get_test_case_path() + "/" + str(test_case_id),
                            test_case.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - update_test_case",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def update_test_case_description(self, test_case_id: int, new_description: str):

        description = {
            "description": new_description
        }

        response = self.put(self.get_test_case_path() + "/" + str(test_case_id),
                            description)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - update_test_case",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def update_test_case_fields(self, qtest_id, field_id, field_name, field_value, field_val_name):

        request_path = str(self.get_test_case_path()) + "/" + str(qtest_id)

        payload = {
                    "properties": [
                        {
                            "field_id": field_id,
                            "field_name": field_name,
                            "field_value": field_value,
                            "field_value_name": field_val_name
                        }
                    ]
        }

        response = self.put(path=request_path,
                            json_data=payload)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "update_test_case_fields",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_test_case_by_id(self, test_case_id):

        request_path = self.get_test_case_path() + '/' + str(test_case_id)

        response = self.get(request_path)

        additional_error_details = "Error performing search for test case with ID " + str(test_case_id)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_test_case_by_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text,
                                                                         optional_details=additional_error_details)

        return response, error_detected

###############################################################################
    def get_test_steps_by_tc_id(self, test_case_id):

        request_path = self.get_test_case_path() + '/' + str(test_case_id) + '/test-steps'

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_test_steps_by_tc_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def update_test_steps_by_tc_id(self, test_case_id, new_steps):

        request_path = self.get_test_case_path() + '/' + str(test_case_id)

        payload = {
                "test_steps": new_steps
        }

        pprint.pprint(payload)

        response = self.put(path=request_path,
                            json_data=payload)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_test_steps_by_tc_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def search_component_test_case_by_qc_id(self, qc_component_id):

        request_path = self.get_search_path()

        payload = {
                    "object_type": "test-cases",
                    "fields": [
                        "id",
                        "name"
                    ],
                    "query": "'QC Record ID' = '" + str(qc_component_id) + "' and 'QC Component' = 'Y'"
                  }

        response = self.post(path=request_path,
                             json_data=payload)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "search_test_case_by_qc_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_all_test_cases(self):

        params = '?expandProps=false&expandSteps=false&size=10000'

        request_path = self.get_test_case_path() + params

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - get_all_test_cases",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def create_module(self, module):

        request_path = self.get_module_path()

        if module.qtest_parent_id is not None:
            request_path += '?parentId=' + str(module.qtest_parent_id)

        module.project_id = self.working_project_id

        response = self.post(request_path,
                             module.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - create_module",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def update_module(self, module, module_id):

        request_path = self.get_module_path() + f"/{module_id}"

        response = self.put(request_path,
                            module.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - update_module",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_module_by_id(self, module_id):

        request_path = self.get_module_path() + '/' + str(module_id)

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - get_module_by_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_all_root_modules(self):

        response = self.get(self.get_module_path())

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - get_all_root_modules",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_all_child_modules_by_root_id(self, root_module_id: int):

        request_path = self.get_module_path() + f'/{str(root_module_id)}?expand=descendants'

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - get_all_child_modules",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def update_release(self, release_id: int, payload: dict):

        request_path = self.get_release_path() + f"/{release_id}"

        response = self.put(request_path,
                            payload)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - update_release",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def create_release(self, release):

        request_path = self.get_release_path()

        response = self.post(request_path,
                             release.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - create_release",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_all_releases(self, return_closed=True):

        if return_closed is False:
            request_path = self.get_release_path()
        else:
            request_path = self.get_release_path() + "?includeClosed=true"

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - get_all_releases",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_release_by_id(self, release_id):

        request_path = self.get_release_path() + '/' + str(release_id)

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - get_release_by_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def create_test_cycle(self, test_cycle):

        request_path = self.get_test_cycle_path()

        if test_cycle.qtest_parent_id is not None:
            request_path = f'{request_path}?parentId=' \
                           f'{test_cycle.qtest_parent_id}' \
                           f'&parentType={test_cycle.qtest_parent_type}'

        response = self.post(request_path,
                             test_cycle.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - create_test_cycle",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_all_test_cycles(self):

        request_path = self.get_test_cycle_path()

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_all_test_cycles",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_direct_child_test_cycles(self, parent_type: str, parent_id: int):
        """
        :param parent_type: can be "release" or "test-cycle"
        :param parent_id:
        :return:
        """

        request_path = self.get_test_cycle_path() + f"?parentId={parent_id}&parentType={parent_type}"

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_direct_child_test_cycles",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_all_child_test_cycles(self, parent_type: str, parent_id: int):
        """
        :param parent_type: can be "release" or "test-cycle"
        :param parent_id:
        :return:
        """

        request_path = self.get_test_cycle_path() + f"?parentId={parent_id}&parentType={parent_type}&expand=descendants"

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_all_child_test_cycles",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_test_cycle_by_id(self, test_cycle_id):

        request_path = self.get_test_cycle_path() + '/' + str(test_cycle_id)

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_test_cycle_by_id",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def create_test_suite(self, test_suite):

        request_path = self.get_test_suite_path()

        if test_suite.qtest_parent_id is not None:
            request_path = f'{request_path}?parentId=' \
                f'{test_suite.qtest_parent_id}' \
                f'&parentType=test-cycle'

        response = self.post(request_path,
                             test_suite.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - create_test_suite",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def update_test_suite(self, test_suite, test_suite_id: int):

        request_path = self.get_test_suite_path() + f"/{test_suite_id}"

        if test_suite.qtest_parent_id is not None:
            request_path = f'{request_path}?parentId=' \
                           f'{test_suite.qtest_parent_id}' \
                           f'&parentType=test-cycle'

        response = self.put(request_path,
                            test_suite.get_json_data())

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - update_test_suite",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def get_direct_child_test_suites(self, parent_type: str, parent_id: int):
        """
        :param parent_type: can be "release" or "test-cycle"
        :param parent_id:
        :return:
        """

        request_path = self.get_test_suite_path() + f"?parentId={parent_id}&parentType={parent_type}"

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_direct_child_test_suites",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_all_test_case_fields(self):

        request_path = self.get_fields_path('test-cases')

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_all_test_case_fields",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_all_test_suite_fields(self):

        request_path = self.get_fields_path('test-suites')

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_all_test_suite_fields",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    def get_all_test_run_fields(self):

        request_path = self.get_fields_path('test-runs')

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_all_test_run_fields",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_all_release_fields(self):

        request_path = self.get_fields_path('releases')

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_all_release_fields",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def create_object_links(self,
                            source_object_type: str,
                            source_object_id: int,
                            linked_object_type: str,
                            ids_to_link: list):

        path = self.get_link_path(source_object_type=source_object_type,
                                  source_object_id=source_object_id,
                                  linked_object_type=linked_object_type)

        response = self.post(path,
                             ids_to_link)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "create_object_links",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def search_qtest_objects(self, qtest_object, fields, query, page=None, page_size=None):
        """
        Wrapper function for qTest Data Query. This API mimics the Data Query function of qTest Manager web app.
        It provides the capability to query Requirements, Test Cases, Test Runs and internal Defects

        qTest API Docs:
            https://api.qasymphony.com/#/search/search3

        Args:
            qtest_object (str): The qtest object you wish to query, available options are
                                requirements, test-cases, test-runs, or defects
            fields (list): A double quoted comma delimited list of field names of field ID's you wish to return for
                           the queried objects
            query (str): A validly formatted query string for the desired data, check API docs for details

        Optional Args:
            page (int): The page number of the paginated results to return

            page_size (int): The number of records to return on a paginated results page

        :return: JSON for queried data
        """

        if page is None:
            page = 1

        if page_size is None:
            page_size = 100

        request_path = self.get_search_path() + "?page=" + str(page) + "&pageSize=" + str(page_size)

        payload = {
                    "object_type": qtest_object,
                    "fields": fields,
                    "query": query
                  }

        response = self.post(path=request_path,
                             json_data=payload)

        # print(response.text)
        # print(str(response.status_code))

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "search_qtest_objects",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def update_requirement(self, requirement_id: int, requirement_payload: dict):

        path = self.get_requirement_path() + f"/{requirement_id}"

        response = self.put(path, requirement_payload)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - update_requirement",
            http_status_code=response.status_code,
            response_text=response.text,
            optional_details=f"API PATH: {path}\n"
                             f"    REQUIREMENT DETAILS: {requirement_payload}")

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def get_requirements_fields(self):

        request_path = self.get_fields_path('requirements')

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - " +
                                                                                       "get_requirements_fields",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def get_project_integrations(self):

        request_path = self.get_project_integrations_path()

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(logger_module="qTest API - "
                                                                                       "get_project_integrations",
                                                                         http_status_code=response.status_code,
                                                                         response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def get_project_object_integrations(self, integration_id: int, integration_object_type: str):

        request_path = self.get_project_integration_object_mappings_path(
            integration_id=integration_id,
            integration_object_type=integration_object_type)

        response = self.get(request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - get_project_object_integrations",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

###############################################################################
    @Decorators.validate_svc_account_access
    def create_jira_requirement_integration(self, integration_id: int,
                                            jira_project_id: int,
                                            jira_issue_type_id: int):

        request_path = self.get_project_integration_object_mappings_path(
            integration_id=integration_id,
            integration_object_type="requirement")

        request_path = request_path + f"?externalProjectId={jira_project_id}&externalIssueTypeId={jira_issue_type_id}"

        response = self.post(path=request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - create_jira_requirement_integration",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def update_jira_requirement_integration(self, integration_id: int,
                                            jira_project_id: int,
                                            jira_issue_type_id: int,
                                            integration_config_payload: dict):

        request_path = self.get_project_integration_object_mappings_path(
            integration_id=integration_id,
            integration_object_type="requirement")

        request_path = request_path + f"?externalProjectId={jira_project_id}&externalIssueTypeId={jira_issue_type_id}"

        response = self.put(path=request_path, json_data=integration_config_payload)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - update_jira_requirement_integration",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def create_jira_defect_integration(self, integration_id: int,
                                       jira_project_id: int,
                                       jira_issue_type_id: int):
        request_path = self.get_project_integration_object_mappings_path(
            integration_id=integration_id,
            integration_object_type="defect")

        request_path = request_path + f"?externalProjectId={jira_project_id}&externalIssueTypeId={jira_issue_type_id}"

        response = self.post(path=request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - create_jira_defect_integration",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def update_jira_defect_integration(self, integration_id: int,
                                       jira_project_id: int,
                                       jira_issue_type_id: int,
                                       integration_config_payload: dict):
        request_path = self.get_project_integration_object_mappings_path(
            integration_id=integration_id,
            integration_object_type="defect")

        request_path = request_path + f"?externalProjectId={jira_project_id}&externalIssueTypeId={jira_issue_type_id}"

        response = self.put(path=request_path, json_data=integration_config_payload)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - update_jira_defect_integration",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

    ###############################################################################
    @Decorators.validate_svc_account_access
    def get_linked_artifacts(self, artifact_type: str, artifact_id: int):

        request_path = self.get_linked_artifacts_path(artifact_type=artifact_type, artifact_id=artifact_id)

        response = self.get(path=request_path)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - get_linked_artifacts",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected

    ###############################################################################
    def delete_tc_to_req_links(self, requirement_id: int, linked_tc_list: list):

        request_path = self.get_requirement_path() + f"/{requirement_id}/link?type=test-cases"
        print(request_path)

        response = self.delete(path=request_path, json_data=linked_tc_list)

        error_detected = self.error_handler.evaluate_response_log_errors(
            logger_module="qTest API - delete_tc_to_req_links",
            http_status_code=response.status_code,
            response_text=response.text)

        return response, error_detected
