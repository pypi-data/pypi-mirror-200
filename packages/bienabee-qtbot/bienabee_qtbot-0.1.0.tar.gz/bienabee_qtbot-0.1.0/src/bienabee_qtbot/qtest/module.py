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


class QTestModule:
    """
        docstring for QTestModule. https://api.qasymphony.com/#/module\
        Parent Module now used in URI path - /api/v3/projects/22/modules?parentId=2755
    """
    def __init__(self, name, description, shared=None, qtest_parent_id=None):
        
        if name is None:
            name = 'PLACEHOLDER'

        if shared is None:
            shared = False

        self.name = name
        self.description = description
        self.shared = shared
        self.qtest_parent_id = qtest_parent_id

    def get_json_data(self):
        data = {
            'name': self.name,
            'description': self.description,
            'shared': self.shared
        }

        return data
