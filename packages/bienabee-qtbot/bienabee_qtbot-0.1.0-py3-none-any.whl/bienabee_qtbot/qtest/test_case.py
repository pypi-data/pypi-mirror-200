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


# https://support.qasymphony.com/hc/en-us/articles/205610505#Create A Test Case
# Name	        Required	Type	    Description
# name	        True	    String	    Test case name
# description	False	    String	    Test case description
# properties	True	    JSONArray	An array of field-value pairs.
# test_steps	False	    JSONArray	The JSONArray of TestStep objects
# parent_id	    False	    String	    ID of the parent module.


class QTestTestCase:
    """docstring for qtest_testcase."""
    def __init__(self,
                 name,
                 qtest_parent_id,
                 description=None,
                 properties=None,
                 test_steps=None,
                 precondition=None
                 ):

        self.name = name
        self.description = description
        self.precondition = precondition
        self.properties = [] if properties is None else properties
        self.test_steps = [] if test_steps is None else test_steps
        self.qtest_parent_id = qtest_parent_id
        self.project_id = None
        self.id = None

    def get_json_data(self):

        if self.description is not None:
            description = self.description
        else:
            description = ""

        data = {
             'name': self.name,
             'description': description,
             'properties': self.properties
        }

        if self.test_steps is not None:
            data['test_steps'] = self.test_steps

        if self.qtest_parent_id is not None:
            data['parent_id'] = self.qtest_parent_id

        if self.precondition is not None:
            data["precondition"] = self.precondition

        return data


