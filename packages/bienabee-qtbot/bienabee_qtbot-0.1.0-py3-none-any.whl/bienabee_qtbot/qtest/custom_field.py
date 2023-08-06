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

# Text box
# Text area
# Combo box
# Date picker
# User list
# Rich text editor
# Number
# Checkbox
# Date and time picker
# URL
# Multiple selection combo box
# releases, builds, requirements, test-cases, defects, test-suites and test-runs


class QTestField:
    """docstring for QTestField."""
    def __init__(self,
                 name,
                 description,
                 parent_id=None,
                 shared=False):
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.shared = shared
        self.id = None
        self.project_id = None

    def get_json_data(self):
        data = {
            'name': self.name,
            'description': self.description
        }

        if self.shared:
            data['shared'] = self.shared

        return data

