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


class QTestSSOUser:
    """docstring for qtest sso user."""
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 email: str,
                 external_user_name: str,
                 user_group_ids: list,
                 external_auth_config_id: int):
        self.username = email
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_group_ids = user_group_ids
        self.external_user_name = external_user_name
        self.external_auth_config_id = external_auth_config_id

    def get_json_data(self):
        data = {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": "",
            "user_group_ids": self.user_group_ids,
            "external_user_name": self.external_user_name,
            "external_auth_config_id": self.external_auth_config_id,
            "send_activation_email": False,
            "include_default_groups": False
        }

        return data
