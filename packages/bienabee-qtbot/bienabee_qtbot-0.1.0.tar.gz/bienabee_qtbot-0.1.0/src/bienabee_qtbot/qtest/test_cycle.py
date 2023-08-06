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


class QTestTestCycle:
    """
    qtest_parent_type can be "test-cycle" or "release"
    """
    def __init__(self,
                 name,
                 description,
                 qtest_parent_id=None,
                 qtest_parent_type=None):
        self.name = name
        self.description = description
        self.qtest_parent_id = qtest_parent_id
        self.qtest_parent_type = qtest_parent_type
        self.qtest_id = None

    def get_json_data(self):
        data = {
            'name': self.name,
            'description': self.description
        }

        return data
