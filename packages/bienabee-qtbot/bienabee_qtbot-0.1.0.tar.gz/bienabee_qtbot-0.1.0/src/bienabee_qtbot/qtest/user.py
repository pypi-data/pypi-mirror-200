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

# https://support.qasymphony.com/hc/en-us/articles/204964959-1-Common-APIs
# Name	        Required	Type	    Description
# name	        True	    String	    Test case name
# description	False	    String	    Test case description
# properties	True	    JSONArray	An array of field-value pairs.
# test_steps	False	    JSONArray	The JSONArray of TestStep objects
# parent_id	    False	    String	    ID of the parent module.


class QTestUser:
    """docstring for qtest_user."""
    def __init__(self,
                 username,
                 first_name,
                 last_name,
                 email,
                 password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.id = None
        self.project_ids = []

    def get_json_data(self):
        data = {
             'username': self.username,
             'first_name': self.first_name,
             'last_name': self.last_name,
             'email': self.email,
             'password': self.password
        }

        return data
